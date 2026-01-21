from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import os
import sys
import logging
from datetime import datetime, timezone

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from aggregators.job_aggregator import JobAggregator
from aggregators.news_aggregator import NewsAggregator
from aggregators.training_aggregator import TrainingAggregator

logger = logging.getLogger(__name__)

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

aggregation_router = APIRouter(prefix="/api/aggregation", tags=["aggregation"])

def serialize_doc(doc):
    if 'created_at' in doc and isinstance(doc['created_at'], datetime):
        doc['created_at'] = doc['created_at'].isoformat()
    if 'updated_at' in doc and isinstance(doc['updated_at'], datetime):
        doc['updated_at'] = doc['updated_at'].isoformat()
    if 'date_expiration' in doc and doc['date_expiration'] and isinstance(doc['date_expiration'], datetime):
        doc['date_expiration'] = doc['date_expiration'].isoformat()
    return doc

@aggregation_router.post("/update-all")
async def update_all_content():
    """Met à jour tout le contenu agrégé (emplois, actualités, formations)"""
    try:
        results = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'jobs': {'added': 0, 'updated': 0},
            'news': {'added': 0, 'updated': 0},
            'trainings': {'added': 0, 'updated': 0}
        }
        
        # Agrégation des emplois
        logger.info("Starting job aggregation...")
        job_agg = JobAggregator()
        jobs = await job_agg.aggregate_all()
        
        for job in jobs:
            existing = await db.emplois.find_one({"slug": job['slug']}, {"_id": 0})
            if existing:
                # Update existing
                await db.emplois.update_one(
                    {"slug": job['slug']},
                    {"$set": serialize_doc(job)}
                )
                results['jobs']['updated'] += 1
            else:
                # Insert new
                await db.emplois.insert_one(serialize_doc(job))
                results['jobs']['added'] += 1
        
        logger.info(f"Jobs aggregation complete: {results['jobs']}")
        
        # Agrégation des actualités
        logger.info("Starting news aggregation...")
        news_agg = NewsAggregator()
        articles = await news_agg.aggregate_all()
        
        for article in articles:
            existing = await db.articles.find_one({"slug": article['slug']}, {"_id": 0})
            if existing:
                await db.articles.update_one(
                    {"slug": article['slug']},
                    {"$set": serialize_doc(article)}
                )
                results['news']['updated'] += 1
            else:
                await db.articles.insert_one(serialize_doc(article))
                results['news']['added'] += 1
        
        logger.info(f"News aggregation complete: {results['news']}")
        
        # Agrégation des formations
        logger.info("Starting training aggregation...")
        training_agg = TrainingAggregator()
        trainings = await training_agg.aggregate_all()
        
        for training in trainings:
            existing = await db.formations.find_one({"slug": training['slug']}, {"_id": 0})
            if existing:
                await db.formations.update_one(
                    {"slug": training['slug']},
                    {"$set": serialize_doc(training)}
                )
                results['trainings']['updated'] += 1
            else:
                await db.formations.insert_one(serialize_doc(training))
                results['trainings']['added'] += 1
        
        logger.info(f"Training aggregation complete: {results['trainings']}")
        
        return {
            'status': 'success',
            'message': 'Content aggregation completed',
            'results': results
        }
    
    except Exception as e:
        logger.error(f"Error during aggregation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@aggregation_router.post("/update-jobs")
async def update_jobs_only():
    """Met à jour uniquement les offres d'emploi"""
    try:
        job_agg = JobAggregator()
        jobs = await job_agg.aggregate_all()
        
        added = 0
        updated = 0
        
        for job in jobs:
            existing = await db.emplois.find_one({"slug": job['slug']}, {"_id": 0})
            if existing:
                await db.emplois.update_one(
                    {"slug": job['slug']},
                    {"$set": serialize_doc(job)}
                )
                updated += 1
            else:
                await db.emplois.insert_one(serialize_doc(job))
                added += 1
        
        return {
            'status': 'success',
            'message': f'Jobs updated: {added} added, {updated} updated',
            'added': added,
            'updated': updated
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@aggregation_router.post("/update-news")
async def update_news_only():
    """Met à jour uniquement les actualités"""
    try:
        news_agg = NewsAggregator()
        articles = await news_agg.aggregate_all()
        
        added = 0
        updated = 0
        
        for article in articles:
            existing = await db.articles.find_one({"slug": article['slug']}, {"_id": 0})
            if existing:
                await db.articles.update_one(
                    {"slug": article['slug']},
                    {"$set": serialize_doc(article)}
                )
                updated += 1
            else:
                await db.articles.insert_one(serialize_doc(article))
                added += 1
        
        return {
            'status': 'success',
            'message': f'News updated: {added} added, {updated} updated',
            'added': added,
            'updated': updated
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@aggregation_router.post("/update-trainings")
async def update_trainings_only():
    """Met à jour uniquement les formations"""
    try:
        training_agg = TrainingAggregator()
        trainings = await training_agg.aggregate_all()
        
        added = 0
        updated = 0
        
        for training in trainings:
            existing = await db.formations.find_one({"slug": training['slug']}, {"_id": 0})
            if existing:
                await db.formations.update_one(
                    {"slug": training['slug']},
                    {"$set": serialize_doc(training)}
                )
                updated += 1
            else:
                await db.formations.insert_one(serialize_doc(training))
                added += 1
        
        return {
            'status': 'success',
            'message': f'Trainings updated: {added} added, {updated} updated',
            'added': added,
            'updated': updated
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@aggregation_router.get("/status")
async def get_aggregation_status():
    """Récupère le statut actuel du contenu"""
    try:
        jobs_count = await db.emplois.count_documents({})
        news_count = await db.articles.count_documents({})
        trainings_count = await db.formations.count_documents({})
        
        # Get latest items
        latest_job = await db.emplois.find_one({}, {"_id": 0}, sort=[("created_at", -1)])
        latest_news = await db.articles.find_one({}, {"_id": 0}, sort=[("created_at", -1)])
        latest_training = await db.formations.find_one({}, {"_id": 0}, sort=[("created_at", -1)])
        
        return {
            'status': 'ok',
            'counts': {
                'jobs': jobs_count,
                'news': news_count,
                'trainings': trainings_count
            },
            'latest': {
                'job': latest_job.get('created_at') if latest_job else None,
                'news': latest_news.get('created_at') if latest_news else None,
                'training': latest_training.get('created_at') if latest_training else None
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))