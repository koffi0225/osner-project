"""
Système de notifications pour les candidats
Gère les notifications pour les nouveaux matchs d'emplois, validations de paiements, etc.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone
from enum import Enum
import os
import uuid

from auth import get_current_user, TokenData
from motor.motor_asyncio import AsyncIOMotorClient

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

notification_router = APIRouter(prefix="/api/notifications", tags=["notifications"])


class NotificationType(str, Enum):
    JOB_MATCH = "job_match"
    PAYMENT_VALIDATED = "payment_validated"
    PAYMENT_PENDING = "payment_pending"
    CV_ANALYZED = "cv_analyzed"
    NEW_JOB = "new_job"
    WELCOME = "welcome"
    SYSTEM = "system"


class NotificationCreate(BaseModel):
    user_id: str
    type: NotificationType
    title: str
    message: str
    link: Optional[str] = None
    metadata: Optional[dict] = None


class Notification(BaseModel):
    id: str
    user_id: str
    type: NotificationType
    title: str
    message: str
    link: Optional[str] = None
    read: bool = False
    created_at: str
    metadata: Optional[dict] = None


@notification_router.get("", response_model=List[Notification])
async def get_notifications(
    limit: int = 20,
    unread_only: bool = False,
    token_data: TokenData = Depends(get_current_user)
):
    """Récupère les notifications de l'utilisateur connecté"""
    
    # Get user
    user = await db.users.find_one({"email": token_data.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    query = {"user_id": user["id"]}
    if unread_only:
        query["read"] = False
    
    cursor = db.notifications.find(query, {"_id": 0}).sort("created_at", -1).limit(limit)
    notifications = await cursor.to_list(length=limit)
    
    return notifications


@notification_router.get("/count")
async def get_unread_count(token_data: TokenData = Depends(get_current_user)):
    """Compte les notifications non lues"""
    
    user = await db.users.find_one({"email": token_data.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    count = await db.notifications.count_documents({
        "user_id": user["id"],
        "read": False
    })
    
    return {"unread_count": count}


@notification_router.put("/{notification_id}/read")
async def mark_as_read(
    notification_id: str,
    token_data: TokenData = Depends(get_current_user)
):
    """Marque une notification comme lue"""
    
    user = await db.users.find_one({"email": token_data.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    result = await db.notifications.update_one(
        {"id": notification_id, "user_id": user["id"]},
        {"$set": {"read": True}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    
    return {"status": "success", "message": "Notification marquée comme lue"}


@notification_router.put("/read-all")
async def mark_all_as_read(token_data: TokenData = Depends(get_current_user)):
    """Marque toutes les notifications comme lues"""
    
    user = await db.users.find_one({"email": token_data.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    result = await db.notifications.update_many(
        {"user_id": user["id"], "read": False},
        {"$set": {"read": True}}
    )
    
    return {"status": "success", "marked_count": result.modified_count}


@notification_router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    token_data: TokenData = Depends(get_current_user)
):
    """Supprime une notification"""
    
    user = await db.users.find_one({"email": token_data.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    result = await db.notifications.delete_one({
        "id": notification_id,
        "user_id": user["id"]
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    
    return {"status": "success", "message": "Notification supprimée"}


# Fonction utilitaire pour créer des notifications (appelée par d'autres modules)
async def create_notification(
    user_id: str,
    notification_type: NotificationType,
    title: str,
    message: str,
    link: Optional[str] = None,
    metadata: Optional[dict] = None
):
    """Crée une nouvelle notification pour un utilisateur"""
    
    notification = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "type": notification_type,
        "title": title,
        "message": message,
        "link": link,
        "read": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata or {}
    }
    
    await db.notifications.insert_one(notification)
    return notification


# Fonction pour envoyer une notification de bienvenue
async def send_welcome_notification(user_id: str, user_name: str):
    """Envoie une notification de bienvenue à un nouvel utilisateur"""
    await create_notification(
        user_id=user_id,
        notification_type=NotificationType.WELCOME,
        title="Bienvenue sur Osner-Group !",
        message=f"Bonjour {user_name}, bienvenue sur la plateforme ! Complétez votre profil et téléchargez votre CV pour recevoir des offres personnalisées.",
        link="/candidate/cv-upload"
    )


# Fonction pour notifier un match d'emploi
async def send_job_match_notification(user_id: str, job_title: str, match_score: int, job_slug: str):
    """Notifie un utilisateur d'un nouveau match d'emploi"""
    await create_notification(
        user_id=user_id,
        notification_type=NotificationType.JOB_MATCH,
        title="Nouvelle opportunité d'emploi !",
        message=f"Votre profil correspond à {match_score}% au poste \"{job_title}\". Consultez cette offre dès maintenant !",
        link=f"/emploi/{job_slug}",
        metadata={"job_slug": job_slug, "match_score": match_score}
    )


# Fonction pour notifier une validation de paiement
async def send_payment_validated_notification(user_id: str, amount: float, credits: int):
    """Notifie un utilisateur que son paiement a été validé"""
    await create_notification(
        user_id=user_id,
        notification_type=NotificationType.PAYMENT_VALIDATED,
        title="Paiement validé !",
        message=f"Votre paiement de {amount:,.0f} XOF a été validé. {credits} crédits ont été ajoutés à votre compte.",
        link="/candidate/dashboard"
    )


# Fonction pour notifier une analyse de CV
async def send_cv_analyzed_notification(user_id: str, suggestions_count: int):
    """Notifie un utilisateur que son CV a été analysé"""
    await create_notification(
        user_id=user_id,
        notification_type=NotificationType.CV_ANALYZED,
        title="Analyse de CV terminée",
        message=f"L'analyse de votre CV est terminée. {suggestions_count} suggestions d'amélioration sont disponibles.",
        link="/candidate/matching"
    )
