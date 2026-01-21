import asyncio
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import logging
from typing import List, Dict, Any
import re
import uuid
import random

logger = logging.getLogger(__name__)

class NewsAggregator:
    """Agrégateur d'actualités de sources multiples"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def generate_slug(self, title: str) -> str:
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        return slug[:100]
    
    async def get_demo_news(self) -> List[Dict[str, Any]]:
        """Génère des actualités de démonstration pour la Côte d'Ivoire"""
        categories = ["Politique", "Société", "Économie", "Sport", "Technologie"]
        
        news_items = [
            {
                'titre': 'Lancement du Programme National d\'Emploi des Jeunes 2025',
                'categorie': 'Économie',
                'extrait': 'Le gouvernement ivoirien lance un ambitieux programme visant à créer 50 000 emplois pour les jeunes d\'ici fin 2025.',
                'contenu': '''Le Ministre de l'Emploi et de la Protection Sociale a officiellement lancé le Programme National d'Emploi des Jeunes (PNEJ) 2025 lors d'une cérémonie à Abidjan.

Ce programme ambitieux vise à créer 50 000 emplois directs pour les jeunes ivoiriens d'ici la fin de l'année. Il s'articule autour de trois axes majeurs :

1. Formation professionnelle accélérée dans les métiers porteurs
2. Accompagnement à l'entrepreneuriat avec des subventions allant jusqu'à 10 millions FCFA
3. Placement direct dans les entreprises partenaires du secteur privé

Les jeunes âgés de 18 à 35 ans peuvent déjà s'inscrire en ligne sur le portail dédié. Les inscriptions sont ouvertes jusqu'au 31 mars 2025.''',
                'tags': ['emploi', 'jeunesse', 'gouvernement'],
                'auteur': 'Agence Ivoirienne de Presse',
                'image_url': 'https://images.pexels.com/photos/6794928/pexels-photo-6794928.jpeg'
            },
            {
                'titre': 'AFCON 2025 : Les Éléphants en Quête de Gloire',
                'categorie': 'Sport',
                'extrait': 'L\'équipe nationale de Côte d\'Ivoire se prépare intensivement pour la Coupe d\'Afrique des Nations qui débute le mois prochain.',
                'contenu': '''Les Éléphants de Côte d'Ivoire intensifient leur préparation en vue de la Coupe d'Afrique des Nations 2025 qui se tiendra au Maroc.

L'équipe dirigée par le sélectionneur Emerse Faé a entamé un stage de préparation à Abidjan avec un effectif de 28 joueurs. Plusieurs stars évoluant en Europe ont répondu présent.

Le calendrier de préparation comprend trois matchs amicaux contre des sélections africaines de premier plan. L'objectif affiché est clair : ramener le trophée continental à Abidjan.

Les supporters ivoiriens, encore marqués par le succès de 2023, espèrent voir leurs Éléphants briller à nouveau sur la scène continentale.''',
                'tags': ['football', 'AFCON', 'sport'],
                'auteur': 'Sport Plus CI',
                'image_url': 'https://images.pexels.com/photos/274506/pexels-photo-274506.jpeg'
            },
            {
                'titre': 'Transformation Digitale : Abidjan Devient un Hub Tech en Afrique',
                'categorie': 'Technologie',
                'extrait': 'La capitale économique ivoirienne attire de plus en plus de startups technologiques et d\'investisseurs internationaux.',
                'contenu': '''Abidjan s'impose progressivement comme un hub technologique majeur en Afrique de l'Ouest. Avec l'ouverture récente de trois nouveaux incubateurs de startups et l'arrivée de géants tech internationaux, la ville connait une transformation digitale sans précédent.

Le quartier de la Zone 4 à Marcory est devenu le "Silicon Valley" ivoirien, concentrant plus de 150 startups actives dans des domaines variés : fintech, e-commerce, edtech, healthtech.

Le gouvernement soutient cette dynamique avec le programme "Côte d'Ivoire Digital 2025" qui vise à former 10 000 développeurs et à créer un écosystème favorable à l'innovation.

Plusieurs success stories ivoiriennes ont récemment lévé des fonds importants auprès d'investisseurs internationaux, confirmant le potentiel du marché.''',
                'tags': ['technologie', 'startup', 'innovation'],
                'auteur': 'TechAfrique',
                'image_url': 'https://images.pexels.com/photos/8124399/pexels-photo-8124399.jpeg'
            },
            {
                'titre': 'Éducation : Ouverture de 10 Nouveaux Lycées Professionnels',
                'categorie': 'Société',
                'extrait': 'Le Ministère de l\'Éducation Nationale inaugure 10 établissements spécialisés dans la formation technique et professionnelle.',
                'contenu': '''Dans le cadre du renforcement du système éducatif ivoirien, le gouvernement a procédé à l'ouverture de 10 nouveaux lycées professionnels répartis sur l'ensemble du territoire national.

Ces établissements ultra-modernes offrent des formations dans des filières porteuses : électricité, mécanique automobile, bâtiment, hôtellerie-restauration, informatique et agriculture moderne.

Chaque lycée peut accueillir jusqu'à 500 élèves et dispose d'équipements de pointe grâce à un partenariat avec des entreprises du secteur privé.

L'objectif est d'atteindre un taux d'insertion professionnelle de 70% pour les diplômés de ces filières techniques.''',
                'tags': ['éducation', 'formation', 'jeunesse'],
                'auteur': 'Éducation News CI',
                'image_url': 'https://images.pexels.com/photos/35539427/pexels-photo-35539427.jpeg'
            },
            {
                'titre': 'Commerce : Le Port d\'Abidjan Bat de Nouveaux Records',
                'categorie': 'Économie',
                'extrait': 'Le Port Autonome d\'Abidjan enregistre une hausse de 15% de son trafic en 2025, consolidant sa position de premier port d\'Afrique de l\'Ouest.',
                'contenu': '''Le Port Autonome d'Abidjan (PAA) confirme son statut de poumon économique de la Côte d'Ivoire avec des résultats exceptionnels pour 2025.

Avec un trafic en hausse de 15% par rapport à 2024, le port traite désormais plus de 30 millions de tonnes de marchandises par an. Cette performance est attribuée aux investissements massifs dans la modernisation des infrastructures.

Le nouveau terminal à conteneurs, d'une capacité de 2 millions d'EVP, joue un rôle clé dans cette croissance. Il permet de réduire considérablement les délais de traitement des marchandises.

Le PAA dessert également les pays enclavés de la sous-région (Mali, Burkina Faso, Niger), renforçant ainsi son rôle de hub logistique régional.''',
                'tags': ['économie', 'commerce', 'infrastructure'],
                'auteur': 'Business Côte d\'Ivoire',
                'image_url': 'https://images.pexels.com/photos/7647950/pexels-photo-7647950.jpeg'
            },
            {
                'titre': 'Santé : Lancement d\'une Campagne de Vaccination Nationale',
                'categorie': 'Société',
                'extrait': 'Le Ministère de la Santé lance une vaste campagne de vaccination contre plusieurs maladies infectieuses ciblant 5 millions d\'enfants.',
                'contenu': '''Le Ministère de la Santé et de l'Hygiène Publique a lancé ce lundi une campagne nationale de vaccination d'envergure.

Cette opération, qui durera trois mois, vise à immuniser 5 millions d'enfants de moins de 5 ans contre plusieurs maladies : rougeole, poliomyélite, diphtérie et coqueluche.

Plus de 10 000 agents de santé ont été mobilisés sur l'ensemble du territoire. Des unités mobiles se rendront même dans les zones rurales les plus reculées.

La campagne bénéficie du soutien de l'OMS et de l'UNICEF. Elle est entièrement gratuite pour les familles ivoiriennes.''',
                'tags': ['santé', 'vaccination', 'enfance'],
                'auteur': 'Santé Info CI',
                'image_url': 'https://images.pexels.com/photos/3952231/pexels-photo-3952231.jpeg'
            }
        ]
        
        # Générer des articles avec dates variables
        articles = []
        for i, item in enumerate(news_items):
            days_ago = random.randint(0, 7)
            created_date = datetime.now(timezone.utc) - timedelta(days=days_ago)
            
            articles.append({
                'id': str(uuid.uuid4()),
                'titre': item['titre'],
                'slug': self.generate_slug(item['titre']),
                'categorie': item['categorie'],
                'tags': item['tags'],
                'auteur': item['auteur'],
                'image_url': item['image_url'],
                'contenu': item['contenu'],
                'extrait': item['extrait'],
                'temps_lecture': len(item['contenu'].split()) // 200 + 1,
                'created_at': created_date.isoformat(),
                'updated_at': created_date.isoformat(),
                'vedette': i < 3,
                'source': 'aggregated'
            })
        
        return articles
    
    async def aggregate_all(self) -> List[Dict[str, Any]]:
        """Agrège toutes les actualités"""
        return await self.get_demo_news()