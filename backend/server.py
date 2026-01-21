from fastapi import FastAPI, APIRouter, HTTPException, Query, Request
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
from enum import Enum

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

# Import new routers
from candidate_routes import candidate_router, payment_router
from aggregation_routes import aggregation_router

# Enums
class ArticleCategory(str, Enum):
    SOCIETE = "Société"
    ECONOMIE = "Économie"
    EDUCATION = "Éducation"
    TECHNOLOGIE = "Technologie"
    EMPLOI = "Emploi"
    ANALYSES = "Analyses / Opinions"

class FormationLevel(str, Enum):
    DEBUTANT = "Débutant"
    INTERMEDIAIRE = "Intermédiaire"
    AVANCE = "Avancé"

class JobType(str, Enum):
    EMPLOI = "Emploi"
    STAGE = "Stage"
    CONCOURS = "Concours"

# Models
class Article(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    titre: str
    slug: str
    categorie: ArticleCategory
    tags: List[str] = []
    auteur: str
    image_url: str
    contenu: str
    extrait: str
    temps_lecture: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    vedette: bool = False

class ArticleCreate(BaseModel):
    titre: str
    slug: str
    categorie: ArticleCategory
    tags: List[str] = []
    auteur: str
    image_url: str
    contenu: str
    extrait: str
    temps_lecture: int
    vedette: bool = False

class Formation(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    titre: str
    slug: str
    thematique: str
    niveau: FormationLevel
    objectifs: List[str]
    image_url: str
    contenu: str
    description: str
    duree: str
    ressources: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class FormationCreate(BaseModel):
    titre: str
    slug: str
    thematique: str
    niveau: FormationLevel
    objectifs: List[str]
    image_url: str
    contenu: str
    description: str
    duree: str
    ressources: List[str] = []

class JobOffer(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    titre: str
    slug: str
    type: JobType
    entreprise: str
    secteur: str
    localisation: str
    description: str
    exigences: List[str]
    url_candidature: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    date_expiration: Optional[datetime] = None

class JobOfferCreate(BaseModel):
    titre: str
    slug: str
    type: JobType
    entreprise: str
    secteur: str
    localisation: str
    description: str
    exigences: List[str]
    url_candidature: Optional[str] = None
    date_expiration: Optional[datetime] = None

class Newsletter(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class NewsletterCreate(BaseModel):
    email: str

# Helper function to serialize datetime
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

# Articles endpoints
@api_router.get("/articles", response_model=List[Article])
async def get_articles(
    categorie: Optional[ArticleCategory] = None,
    tag: Optional[str] = None,
    vedette: Optional[bool] = None,
    limit: int = Query(default=20, le=100)
):
    query = {}
    if categorie:
        query['categorie'] = categorie
    if tag:
        query['tags'] = tag
    if vedette is not None:
        query['vedette'] = vedette
    
    articles = await db.articles.find(query, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)
    return [deserialize_doc(article) for article in articles]

@api_router.get("/articles/{slug}", response_model=Article)
async def get_article(slug: str):
    article = await db.articles.find_one({"slug": slug}, {"_id": 0})
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return deserialize_doc(article)

@api_router.post("/articles", response_model=Article)
async def create_article(input: ArticleCreate):
    article_dict = input.model_dump()
    article_obj = Article(**article_dict)
    doc = serialize_doc(article_obj.model_dump())
    await db.articles.insert_one(doc)
    return article_obj

@api_router.put("/articles/{article_id}", response_model=Article)
async def update_article(article_id: str, input: ArticleCreate):
    article_dict = input.model_dump()
    article_dict['id'] = article_id
    article_dict['updated_at'] = datetime.now(timezone.utc)
    article_obj = Article(**article_dict)
    doc = serialize_doc(article_obj.model_dump())
    
    result = await db.articles.update_one({"id": article_id}, {"$set": doc})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return article_obj

@api_router.delete("/articles/{article_id}")
async def delete_article(article_id: str):
    result = await db.articles.delete_one({"id": article_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return {"message": "Article supprimé"}

# Formations endpoints
@api_router.get("/formations", response_model=List[Formation])
async def get_formations(
    thematique: Optional[str] = None,
    niveau: Optional[FormationLevel] = None,
    limit: int = Query(default=20, le=100)
):
    query = {}
    if thematique:
        query['thematique'] = thematique
    if niveau:
        query['niveau'] = niveau
    
    formations = await db.formations.find(query, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)
    return [deserialize_doc(formation) for formation in formations]

@api_router.get("/formations/{slug}", response_model=Formation)
async def get_formation(slug: str):
    formation = await db.formations.find_one({"slug": slug}, {"_id": 0})
    if not formation:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return deserialize_doc(formation)

@api_router.post("/formations", response_model=Formation)
async def create_formation(input: FormationCreate):
    formation_dict = input.model_dump()
    formation_obj = Formation(**formation_dict)
    doc = serialize_doc(formation_obj.model_dump())
    await db.formations.insert_one(doc)
    return formation_obj

@api_router.put("/formations/{formation_id}", response_model=Formation)
async def update_formation(formation_id: str, input: FormationCreate):
    formation_dict = input.model_dump()
    formation_dict['id'] = formation_id
    formation_dict['updated_at'] = datetime.now(timezone.utc)
    formation_obj = Formation(**formation_dict)
    doc = serialize_doc(formation_obj.model_dump())
    
    result = await db.formations.update_one({"id": formation_id}, {"$set": doc})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return formation_obj

@api_router.delete("/formations/{formation_id}")
async def delete_formation(formation_id: str):
    result = await db.formations.delete_one({"id": formation_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return {"message": "Formation supprimée"}

# Job offers endpoints
@api_router.get("/emplois", response_model=List[JobOffer])
async def get_emplois(
    type: Optional[JobType] = None,
    secteur: Optional[str] = None,
    localisation: Optional[str] = None,
    limit: int = Query(default=20, le=100)
):
    query = {}
    if type:
        query['type'] = type
    if secteur:
        query['secteur'] = secteur
    if localisation:
        query['localisation'] = localisation
    
    emplois = await db.emplois.find(query, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)
    return [deserialize_doc(emploi) for emploi in emplois]

@api_router.get("/emplois/{slug}", response_model=JobOffer)
async def get_emploi(slug: str):
    emploi = await db.emplois.find_one({"slug": slug}, {"_id": 0})
    if not emploi:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    return deserialize_doc(emploi)

@api_router.post("/emplois", response_model=JobOffer)
async def create_emploi(input: JobOfferCreate):
    emploi_dict = input.model_dump()
    emploi_obj = JobOffer(**emploi_dict)
    doc = serialize_doc(emploi_obj.model_dump())
    await db.emplois.insert_one(doc)
    return emploi_obj

@api_router.put("/emplois/{emploi_id}", response_model=JobOffer)
async def update_emploi(emploi_id: str, input: JobOfferCreate):
    emploi_dict = input.model_dump()
    emploi_dict['id'] = emploi_id
    emploi_obj = JobOffer(**emploi_dict)
    doc = serialize_doc(emploi_obj.model_dump())
    
    result = await db.emplois.update_one({"id": emploi_id}, {"$set": doc})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    return emploi_obj

@api_router.delete("/emplois/{emploi_id}")
async def delete_emploi(emploi_id: str):
    result = await db.emplois.delete_one({"id": emploi_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    return {"message": "Offre supprimée"}

# Newsletter endpoint
@api_router.post("/newsletter", response_model=Newsletter)
async def subscribe_newsletter(input: NewsletterCreate):
    # Check if email already exists
    existing = await db.newsletter.find_one({"email": input.email}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà inscrit")
    
    newsletter_dict = input.model_dump()
    newsletter_obj = Newsletter(**newsletter_dict)
    doc = serialize_doc(newsletter_obj.model_dump())
    await db.newsletter.insert_one(doc)
    return newsletter_obj

@api_router.get("/")
async def root():
    return {"message": "Plateforme API - Actualité, Formation, Emploi"}

# Webhook Stripe at root level
@app.post("/api/webhook/stripe")
async def stripe_webhook_root(request: Request):
    from candidate_routes import stripe_webhook
    return await stripe_webhook(request)

# Include the router in the main app
app.include_router(api_router)
app.include_router(candidate_router)
app.include_router(payment_router)
app.include_router(aggregation_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()