from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from auth import get_current_user, TokenData
from utils.payment_processor import PaymentMethod, PaymentProcessor
from utils.receipt_generator import ReceiptGenerator
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

multi_payment_router = APIRouter(prefix="/api/payments-multi", tags=["payments-multi"])

# Paiement packages
PAYMENT_PACKAGES = {
    "cv_analysis": {"name": "Analyse de CV", "amount": 2500, "currency": "XOF", "credits": 1, "description": "1 analyse complète de CV"},
    "matching_premium": {"name": "Matching Premium", "amount": 5000, "currency": "XOF", "credits": 5, "description": "5 analyses de compatibilité"},
    "monthly_subscription": {"name": "Abonnement Mensuel", "amount": 10000, "currency": "XOF", "credits": 20, "description": "20 analyses + support prioritaire"}
}

class PaymentInitiateRequest(BaseModel):
    package_id: str
    payment_method: PaymentMethod
    phone_number: Optional[str] = None

class PaymentConfirmRequest(BaseModel):
    transaction_id: str
    payment_proof: Optional[str] = None  # Pour Mobile Money, photo du SMS

@multi_payment_router.get("/methods")
async def get_payment_methods():
    """Retourne les méthodes de paiement disponibles"""
    return {
        "methods": [
            {
                "id": "stripe",
                "name": "Carte Bancaire (Visa/Mastercard)",
                "icon": "credit-card",
                "type": "card",
                "available": True
            },
            {
                "id": "orange_money",
                "name": "Orange Money",
                "icon": "smartphone",
                "type": "mobile_money",
                "available": True,
                "ussd_code": "*144#"
            },
            {
                "id": "mtn_money",
                "name": "MTN Money",
                "icon": "smartphone",
                "type": "mobile_money",
                "available": True,
                "ussd_code": "*133#"
            },
            {
                "id": "moov_money",
                "name": "Moov Money",
                "icon": "smartphone",
                "type": "mobile_money",
                "available": True,
                "ussd_code": "*155#"
            },
            {
                "id": "wave_ci",
                "name": "Wave CI",
                "icon": "smartphone",
                "type": "mobile_money",
                "available": True,
                "app_required": True
            },
            {
                "id": "tresor_money",
                "name": "Trésor Money (Poste)",
                "icon": "building",
                "type": "offline",
                "available": True
            },
            {
                "id": "bank_transfer",
                "name": "Virement Bancaire",
                "icon": "bank",
                "type": "offline",
                "available": True
            }
        ]
    }

@multi_payment_router.get("/packages")
async def get_packages():
    """Retourne les packages disponibles"""
    return {
        "packages": [
            {
                "id": "cv_analysis",
                **PAYMENT_PACKAGES["cv_analysis"]
            },
            {
                "id": "matching_premium",
                **PAYMENT_PACKAGES["matching_premium"],
                "popular": True
            },
            {
                "id": "monthly_subscription",
                **PAYMENT_PACKAGES["monthly_subscription"]
            }
        ]
    }

@multi_payment_router.post("/initiate")
async def initiate_payment(
    request: PaymentInitiateRequest,
    token_data: TokenData = Depends(get_current_user)
):
    """Initie un paiement avec la méthode choisie"""
    
    # Validate package
    if request.package_id not in PAYMENT_PACKAGES:
        raise HTTPException(status_code=400, detail="Package invalide")
    
    package = PAYMENT_PACKAGES[request.package_id]
    
    # Get user
    user = await db.users.find_one({"email": token_data.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Si Stripe, rediriger vers l'ancien endpoint
    if request.payment_method == PaymentMethod.STRIPE:
        from candidate_routes import create_checkout_session
        # TODO: Call stripe endpoint
        raise HTTPException(status_code=400, detail="Utilisez /api/payments/checkout/session pour Stripe")
    
    # Traiter avec le nouveau système
    processor = PaymentProcessor()
    
    try:
        payment_result = await processor.initiate_payment(
            method=request.payment_method,
            amount=package["amount"],
            currency=package["currency"],
            user_data={
                "id": user["id"],
                "email": user["email"],
                "nom": user["nom"],
                "prenom": user["prenom"],
                "sexe": user.get("sexe", "N/A"),
                "code_inscription": user.get("code_inscription", "N/A")
            },
            package_data=package,
            phone_number=request.phone_number
        )
        
        # Enregistrer la transaction
        transaction_doc = {
            "transaction_id": payment_result["transaction_id"],
            "user_id": user["id"],
            "package_id": request.package_id,
            "amount": package["amount"],
            "currency": package["currency"],
            "credits": package["credits"],
            "payment_method": request.payment_method,
            "payment_status": "pending",
            "payment_data": payment_result,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.payment_transactions.insert_one(transaction_doc)
        
        return {
            "status": "initiated",
            "transaction_id": payment_result["transaction_id"],
            "payment_data": payment_result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@multi_payment_router.post("/confirm")
async def confirm_payment(
    request: PaymentConfirmRequest,
    token_data: TokenData = Depends(get_current_user)
):
    """Confirme un paiement (pour Mobile Money et méthodes offline)"""
    
    # Get transaction
    transaction = await db.payment_transactions.find_one(
        {"transaction_id": request.transaction_id},
        {"_id": 0}
    )
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")
    
    # Get user
    user = await db.users.find_one({"email": token_data.email}, {"_id": 0})
    if not user or user["id"] != transaction["user_id"]:
        raise HTTPException(status_code=403, detail="Non autorisé")
    
    # Update transaction status (en attente de validation admin pour Mobile Money)
    await db.payment_transactions.update_one(
        {"transaction_id": request.transaction_id},
        {
            "$set": {
                "payment_status": "pending_validation",
                "payment_proof": request.payment_proof,
                "confirmed_at": datetime.now(timezone.utc).isoformat()
            }
        }
    )
    
    return {
        "status": "pending_validation",
        "message": "Votre paiement est en cours de vérification. Vous serez notifié par email dans les 24h."
    }

@multi_payment_router.post("/admin/validate/{transaction_id}")
async def validate_payment_admin(transaction_id: str):
    """Endpoint admin pour valider un paiement Mobile Money"""
    
    transaction = await db.payment_transactions.find_one(
        {"transaction_id": transaction_id},
        {"_id": 0}
    )
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")
    
    # Update transaction
    await db.payment_transactions.update_one(
        {"transaction_id": transaction_id},
        {
            "$set": {
                "payment_status": "paid",
                "validated_at": datetime.now(timezone.utc).isoformat()
            }
        }
    )
    
    # Add credits
    await db.users.update_one(
        {"id": transaction["user_id"]},
        {"$inc": {"credits": transaction["credits"]}}
    )
    
    # Get updated user
    user = await db.users.find_one({"id": transaction["user_id"]}, {"_id": 0})
    
    # Generate receipt
    package = PAYMENT_PACKAGES.get(transaction["package_id"], {})
    
    receipt_gen = ReceiptGenerator()
    receipt_path = receipt_gen.generate_receipt(
        user_data={
            "nom": user["nom"],
            "prenom": user["prenom"],
            "sexe": user.get("sexe", "N/A"),
            "email": user["email"],
            "code_inscription": user.get("code_inscription", "N/A"),
            "date_inscription": user.get("created_at", "N/A")
        },
        payment_data={
            "transaction_id": transaction_id,
            "amount": transaction["amount"],
            "currency": transaction["currency"],
            "payment_method": transaction["payment_method"],
            "date": datetime.now(timezone.utc)
        },
        package_data={
            "name": package.get("name", "Package"),
            "credits": transaction["credits"],
            "description": package.get("description", "")
        }
    )
    
    # Save receipt path in transaction
    await db.payment_transactions.update_one(
        {"transaction_id": transaction_id},
        {"$set": {"receipt_path": receipt_path}}
    )
    
    return {
        "status": "validated",
        "credits_added": transaction["credits"],
        "receipt_path": receipt_path
    }

@multi_payment_router.get("/receipt/{transaction_id}")
async def get_receipt(
    transaction_id: str,
    token_data: TokenData = Depends(get_current_user)
):
    """Télécharge le reçu PDF d'une transaction"""
    
    from fastapi.responses import FileResponse
    
    transaction = await db.payment_transactions.find_one(
        {"transaction_id": transaction_id},
        {"_id": 0}
    )
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")
    
    user = await db.users.find_one({"email": token_data.email}, {"_id": 0})
    if not user or user["id"] != transaction["user_id"]:
        raise HTTPException(status_code=403, detail="Non autorisé")
    
    if "receipt_path" not in transaction:
        raise HTTPException(status_code=404, detail="Reçu non disponible")
    
    receipt_path = transaction["receipt_path"]
    
    if not os.path.exists(receipt_path):
        raise HTTPException(status_code=404, detail="Fichier reçu introuvable")
    
    return FileResponse(
        path=receipt_path,
        media_type="application/pdf",
        filename=f"recu_{transaction_id}.pdf"
    )
