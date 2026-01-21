from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Request
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid
import os
import shutil
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

from auth import get_current_user, TokenData, get_password_hash, verify_password, create_access_token
from cv_parser import CVParser
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionRequest, CheckoutSessionResponse
from notification_routes import send_welcome_notification

load_dotenv()

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize router
candidate_router = APIRouter(prefix="/api/candidate", tags=["candidate"])
payment_router = APIRouter(prefix="/api/payments", tags=["payments"])

# Initialize CV Parser
cv_parser = CVParser()

# Stripe API Key
stripe_api_key = os.environ.get('STRIPE_API_KEY', 'sk_test_emergent')

# Payment packages
PAYMENT_PACKAGES = {
    "cv_analysis": {"name": "Analyse de CV", "amount": 5.00, "credits": 1},
    "matching_premium": {"name": "Matching Premium", "amount": 10.00, "credits": 5},
    "monthly_subscription": {"name": "Abonnement Mensuel", "amount": 20.00, "credits": 20}
}

# Models
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    nom: str
    prenom: str
    sexe: str  # "M" ou "F"
    telephone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    email: str
    nom: str
    prenom: str
    sexe: str
    telephone: Optional[str]
    code_inscription: str
    credits: int
    created_at: datetime

class CVUploadResponse(BaseModel):
    cv_id: str
    filename: str
    parsed_data: Dict[str, Any]
    message: str

class CVAnalysisRequest(BaseModel):
    job_id: str

class CVAnalysisResponse(BaseModel):
    score: int
    points_forts: List[str]
    points_a_ameliorer: List[str]
    suggestions: List[str]
    resume_analyse: str

class JobMatchingResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    job_id: str
    job_title: str
    entreprise: str
    score: int
    resume_analyse: str

class PaymentPackageRequest(BaseModel):
    package_id: str
    origin_url: str

class PaymentStatusResponse(BaseModel):
    status: str
    payment_status: str
    credits_added: int
    message: str

# Helper functions
def serialize_doc(doc):
    if 'created_at' in doc and isinstance(doc['created_at'], datetime):
        doc['created_at'] = doc['created_at'].isoformat()
    if 'updated_at' in doc and isinstance(doc['updated_at'], datetime):
        doc['updated_at'] = doc['updated_at'].isoformat()
    if 'date_expiration' in doc and doc['date_expiration'] and isinstance(doc['date_expiration'], datetime):
        doc['date_expiration'] = doc['date_expiration'].isoformat()
    return doc

def deserialize_doc(doc):
    if 'created_at' in doc and isinstance(doc['created_at'], str):
        doc['created_at'] = datetime.fromisoformat(doc['created_at'])
    if 'updated_at' in doc and isinstance(doc['updated_at'], str):
        doc['updated_at'] = datetime.fromisoformat(doc['updated_at'])
    if 'date_expiration' in doc and doc['date_expiration'] and isinstance(doc['date_expiration'], str):
        doc['date_expiration'] = datetime.fromisoformat(doc['date_expiration'])
    return doc

# Authentication Endpoints
@candidate_router.post("/register")
async def register(user: UserRegister):
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email}, {"_id": 0})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    
    # Generate code d'inscription unique
    code_inscription = f"OSN{datetime.now(timezone.utc).strftime('%Y%m')}{str(uuid.uuid4())[:6].upper()}"
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    user_doc = {
        "id": str(uuid.uuid4()),
        "email": user.email,
        "hashed_password": hashed_password,
        "nom": user.nom,
        "prenom": user.prenom,
        "sexe": user.sexe,
        "telephone": user.telephone,
        "code_inscription": code_inscription,
        "credits": 0,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.users.insert_one(user_doc)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_doc["id"],
            "email": user_doc["email"],
            "nom": user_doc["nom"],
            "prenom": user_doc["prenom"],
            "sexe": user_doc["sexe"],
            "code_inscription": user_doc["code_inscription"],
            "credits": user_doc["credits"]
        }
    }

@candidate_router.post("/login")
async def login(credentials: UserLogin):
    # Find user
    user = await db.users.find_one({"email": credentials.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    # Verify password
    if not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    # Create access token
    access_token = create_access_token(data={"sub": user["email"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "nom": user["nom"],
            "prenom": user["prenom"],
            "credits": user["credits"]
        }
    }

@candidate_router.get("/me", response_model=UserResponse)
async def get_current_user_info(token_data: TokenData = Depends(get_current_user)):
    user = await db.users.find_one({"email": token_data.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return deserialize_doc(user)

# CV Management Endpoints
@candidate_router.post("/cv/upload", response_model=CVUploadResponse)
async def upload_cv(
    file: UploadFile = File(...),
    token_data: TokenData = Depends(get_current_user)
):
    # Validate file type
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Seuls les fichiers PDF et DOCX sont acceptés")
    
    # Get user
    user = await db.users.find_one({"email": token_data.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Create upload directory if it doesn't exist
    upload_dir = Path("/app/uploads/cvs")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Save file
    cv_id = str(uuid.uuid4())
    file_extension = file.filename.split('.')[-1]
    file_path = upload_dir / f"{cv_id}.{file_extension}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extract text based on file type
    try:
        if file_extension == 'pdf':
            cv_text = cv_parser.extract_text_from_pdf(str(file_path))
        else:
            cv_text = cv_parser.extract_text_from_docx(str(file_path))
        
        # Parse CV with AI
        parsed_data = await cv_parser.parse_cv(cv_text)
        
        # Save CV record to database
        cv_doc = {
            "id": cv_id,
            "user_id": user["id"],
            "filename": file.filename,
            "file_path": str(file_path),
            "parsed_data": parsed_data,
            "raw_text": cv_text,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.cvs.insert_one(cv_doc)
        
        return {
            "cv_id": cv_id,
            "filename": file.filename,
            "parsed_data": parsed_data,
            "message": "CV uploadé et analysé avec succès"
        }
    
    except Exception as e:
        # Clean up file if parsing fails
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse du CV: {str(e)}")

@candidate_router.get("/cv/my-cv")
async def get_my_cv(token_data: TokenData = Depends(get_current_user)):
    user = await db.users.find_one({"email": token_data.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    cv = await db.cvs.find_one({"user_id": user["id"]}, {"_id": 0})
    if not cv:
        raise HTTPException(status_code=404, detail="Aucun CV trouvé")
    
    return deserialize_doc(cv)

# Job Matching Endpoints
@candidate_router.post("/cv/analyze-for-job", response_model=CVAnalysisResponse)
async def analyze_cv_for_job(
    request: CVAnalysisRequest,
    token_data: TokenData = Depends(get_current_user)
):
    # Get user
    user = await db.users.find_one({"email": token_data.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Check credits
    if user["credits"] <= 0:
        raise HTTPException(status_code=402, detail="Crédits insuffisants. Veuillez recharger votre compte.")
    
    # Get user's CV
    cv = await db.cvs.find_one({"user_id": user["id"]}, {"_id": 0})
    if not cv:
        raise HTTPException(status_code=404, detail="Veuillez d'abord uploader votre CV")
    
    # Get job offer
    job = await db.emplois.find_one({"id": request.job_id}, {"_id": 0})
    if not job:
        raise HTTPException(status_code=404, detail="Offre d'emploi non trouvée")
    
    # Prepare job description
    job_description = f"""
    Titre: {job['titre']}
    Entreprise: {job['entreprise']}
    Secteur: {job['secteur']}
    Description: {job['description']}
    Exigences: {', '.join(job['exigences'])}
    """
    
    # Analyze with AI
    try:
        analysis = await cv_parser.analyze_cv_for_job(cv['parsed_data'], job_description)
        
        # Deduct credit
        await db.users.update_one(
            {"id": user["id"]},
            {"$inc": {"credits": -1}}
        )
        
        # Save analysis
        analysis_doc = {
            "id": str(uuid.uuid4()),
            "user_id": user["id"],
            "cv_id": cv["id"],
            "job_id": request.job_id,
            "analysis": analysis,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.cv_analyses.insert_one(analysis_doc)
        
        return analysis
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse: {str(e)}")

@candidate_router.get("/jobs/matching", response_model=List[JobMatchingResponse])
async def get_matching_jobs(token_data: TokenData = Depends(get_current_user)):
    # Get user
    user = await db.users.find_one({"email": token_data.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Get user's CV
    cv = await db.cvs.find_one({"user_id": user["id"]}, {"_id": 0})
    if not cv:
        raise HTTPException(status_code=404, detail="Veuillez d'abord uploader votre CV")
    
    # Get existing analyses
    analyses = await db.cv_analyses.find({"user_id": user["id"]}, {"_id": 0}).to_list(100)
    
    # Create matching results
    matching_jobs = []
    for analysis in analyses:
        job = await db.emplois.find_one({"id": analysis["job_id"]}, {"_id": 0})
        if job and 'analysis' in analysis and 'score' in analysis['analysis']:
            matching_jobs.append({
                "job_id": job["id"],
                "job_title": job["titre"],
                "entreprise": job["entreprise"],
                "score": analysis['analysis']['score'],
                "resume_analyse": analysis['analysis'].get('resume_analyse', '')
            })
    
    # Sort by score descending
    matching_jobs.sort(key=lambda x: x['score'], reverse=True)
    
    return matching_jobs

# Payment Endpoints
@payment_router.post("/checkout/session", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    request: PaymentPackageRequest,
    token_data: TokenData = Depends(get_current_user)
):
    # Validate package
    if request.package_id not in PAYMENT_PACKAGES:
        raise HTTPException(status_code=400, detail="Package invalide")
    
    package = PAYMENT_PACKAGES[request.package_id]
    
    # Get user
    user = await db.users.find_one({"email": token_data.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Create Stripe checkout
    webhook_url = f"{request.origin_url}/api/webhook/stripe"
    stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url=webhook_url)
    
    success_url = f"{request.origin_url}/candidate/payment-success?session_id={{{{CHECKOUT_SESSION_ID}}}}"
    cancel_url = f"{request.origin_url}/candidate/payment"
    
    checkout_request = CheckoutSessionRequest(
        amount=package["amount"],
        currency="eur",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "user_id": user["id"],
            "package_id": request.package_id,
            "credits": str(package["credits"])
        }
    )
    
    session = await stripe_checkout.create_checkout_session(checkout_request)
    
    # Save transaction as pending
    transaction_doc = {
        "id": str(uuid.uuid4()),
        "session_id": session.session_id,
        "user_id": user["id"],
        "package_id": request.package_id,
        "amount": package["amount"],
        "currency": "eur",
        "credits": package["credits"],
        "payment_status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.payment_transactions.insert_one(transaction_doc)
    
    return session

@payment_router.get("/checkout/status/{session_id}", response_model=PaymentStatusResponse)
async def get_payment_status(
    session_id: str,
    request: Request,
    token_data: TokenData = Depends(get_current_user)
):
    # Get transaction
    transaction = await db.payment_transactions.find_one({"session_id": session_id}, {"_id": 0})
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")
    
    # Check if already processed
    if transaction["payment_status"] == "paid":
        return {
            "status": "complete",
            "payment_status": "paid",
            "credits_added": transaction["credits"],
            "message": "Paiement déjà traité"
        }
    
    # Check with Stripe
    origin_url = str(request.base_url).rstrip('/')
    webhook_url = f"{origin_url}/api/webhook/stripe"
    stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url=webhook_url)
    
    try:
        checkout_status = await stripe_checkout.get_checkout_status(session_id)
        
        if checkout_status.payment_status == "paid" and transaction["payment_status"] != "paid":
            # Update transaction
            await db.payment_transactions.update_one(
                {"session_id": session_id},
                {"$set": {"payment_status": "paid", "updated_at": datetime.now(timezone.utc).isoformat()}}
            )
            
            # Add credits to user
            await db.users.update_one(
                {"id": transaction["user_id"]},
                {"$inc": {"credits": transaction["credits"]}}
            )
            
            return {
                "status": checkout_status.status,
                "payment_status": "paid",
                "credits_added": transaction["credits"],
                "message": "Paiement réussi ! Crédits ajoutés."
            }
        
        return {
            "status": checkout_status.status,
            "payment_status": checkout_status.payment_status,
            "credits_added": 0,
            "message": "Paiement en cours"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la vérification: {str(e)}")

@payment_router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("Stripe-Signature")
    
    stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url="")
    
    try:
        webhook_response = await stripe_checkout.handle_webhook(body, signature)
        
        if webhook_response.payment_status == "paid":
            # Update transaction
            transaction = await db.payment_transactions.find_one(
                {"session_id": webhook_response.session_id},
                {"_id": 0}
            )
            
            if transaction and transaction["payment_status"] != "paid":
                await db.payment_transactions.update_one(
                    {"session_id": webhook_response.session_id},
                    {"$set": {"payment_status": "paid"}}
                )
                
                # Add credits
                await db.users.update_one(
                    {"id": transaction["user_id"]},
                    {"$inc": {"credits": transaction["credits"]}}
                )
        
        return {"status": "success"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))