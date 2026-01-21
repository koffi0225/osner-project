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
    """Agrégateur d'actualités de sources multiples pour la Côte d'Ivoire"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
        }
        self.timeout = aiohttp.ClientTimeout(total=30)
    
    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def generate_slug(self, title: str) -> str:
        slug = title.lower()
        slug = re.sub(r'[àâä]', 'a', slug)
        slug = re.sub(r'[éèêë]', 'e', slug)
        slug = re.sub(r'[ïî]', 'i', slug)
        slug = re.sub(r'[ôö]', 'o', slug)
        slug = re.sub(r'[ùûü]', 'u', slug)
        slug = re.sub(r'[ç]', 'c', slug)
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        return slug[:100]
    
    def extract_category(self, text: str, url: str = "") -> str:
        """Extrait la catégorie basée sur le contenu et l'URL"""
        text_lower = (text + " " + url).lower()
        
        if any(word in text_lower for word in ['sport', 'football', 'basket', 'athlé', 'can ', 'afcon', 'éléphant']):
            return "Sport"
        elif any(word in text_lower for word in ['économ', 'finance', 'pib', 'croissance', 'banque', 'investiss', 'commerce', 'port', 'export']):
            return "Économie"
        elif any(word in text_lower for word in ['technolog', 'digital', 'startup', 'innov', 'numérique', 'tech', 'internet']):
            return "Technologie"
        elif any(word in text_lower for word in ['politique', 'gouvernement', 'président', 'ministre', 'élection', 'parlement', 'assemblée']):
            return "Politique"
        elif any(word in text_lower for word in ['santé', 'médecin', 'hôpital', 'vaccin', 'maladie', 'oms']):
            return "Santé"
        elif any(word in text_lower for word in ['éducation', 'école', 'université', 'formation', 'étudiant', 'bac', 'diplôme']):
            return "Éducation"
        else:
            return "Société"
    
    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> str:
        """Récupère le contenu HTML d'une page"""
        try:
            async with session.get(url, headers=self.headers, timeout=self.timeout, ssl=False) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.warning(f"Failed to fetch {url}: status {response.status}")
                    return ""
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return ""
    
    async def scrape_abidjan_net(self, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Scrape Abidjan.net - Un des plus grands portails d'actualités ivoiriennes"""
        articles = []
        base_url = "https://news.abidjan.net"
        
        try:
            # Page principale des actualités
            html = await self.fetch_page(session, f"{base_url}/articles/")
            if not html:
                logger.warning("Could not fetch Abidjan.net")
                return articles
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Chercher les articles - plusieurs sélecteurs possibles
            article_elements = soup.select('article, .article, .news-item, .post-item, div[class*="article"]')
            
            if not article_elements:
                # Essayer d'autres sélecteurs
                article_elements = soup.select('h2 a, h3 a, .title a')
            
            for element in article_elements[:10]:
                try:
                    # Extraire le titre
                    title_elem = element.select_one('h2, h3, .title, a')
                    if not title_elem:
                        title_elem = element if element.name == 'a' else element.find('a')
                    
                    if not title_elem:
                        continue
                    
                    title = self.clean_text(title_elem.get_text())
                    if not title or len(title) < 15:
                        continue
                    
                    # Extraire le lien
                    link_elem = title_elem if title_elem.name == 'a' else title_elem.find('a')
                    link = link_elem.get('href', '') if link_elem else ''
                    if link and not link.startswith('http'):
                        link = base_url + link
                    
                    # Extraire l'extrait
                    excerpt_elem = element.select_one('p, .excerpt, .summary, .description')
                    excerpt = self.clean_text(excerpt_elem.get_text()) if excerpt_elem else title[:150] + "..."
                    
                    # Extraire l'image
                    img_elem = element.select_one('img')
                    image_url = img_elem.get('src', '') if img_elem else ''
                    if image_url and not image_url.startswith('http'):
                        image_url = base_url + image_url
                    
                    if not image_url:
                        image_url = f"https://images.pexels.com/photos/{random.randint(1000000, 9999999)}/pexels-photo.jpeg"
                    
                    articles.append({
                        'id': str(uuid.uuid4()),
                        'titre': title,
                        'slug': self.generate_slug(title),
                        'categorie': self.extract_category(title + " " + excerpt, link),
                        'tags': ['Côte d\'Ivoire', 'Actualité'],
                        'auteur': 'Abidjan.net',
                        'image_url': image_url,
                        'contenu': f"{excerpt}\n\nSource: Abidjan.net\nLire l'article complet: {link}",
                        'extrait': excerpt[:200] if len(excerpt) > 200 else excerpt,
                        'temps_lecture': max(1, len(excerpt.split()) // 200),
                        'created_at': datetime.now(timezone.utc).isoformat(),
                        'updated_at': datetime.now(timezone.utc).isoformat(),
                        'vedette': False,
                        'source': 'abidjan.net',
                        'source_url': link
                    })
                except Exception as e:
                    logger.error(f"Error parsing article from Abidjan.net: {str(e)}")
                    continue
            
        except Exception as e:
            logger.error(f"Error scraping Abidjan.net: {str(e)}")
        
        return articles
    
    async def scrape_fratmat(self, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Scrape Fraternité Matin - Journal officiel de Côte d'Ivoire"""
        articles = []
        base_url = "https://www.fratmat.info"
        
        try:
            html = await self.fetch_page(session, base_url)
            if not html:
                logger.warning("Could not fetch Fratmat")
                return articles
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Chercher les articles
            article_elements = soup.select('article, .post, .news-item, .article-item')
            
            if not article_elements:
                article_elements = soup.select('h2 a, h3 a')
            
            for element in article_elements[:8]:
                try:
                    title_elem = element.select_one('h2, h3, .entry-title, a')
                    if not title_elem:
                        title_elem = element if element.name == 'a' else None
                    
                    if not title_elem:
                        continue
                    
                    title = self.clean_text(title_elem.get_text())
                    if not title or len(title) < 15:
                        continue
                    
                    link_elem = title_elem if title_elem.name == 'a' else title_elem.find('a')
                    link = link_elem.get('href', '') if link_elem else ''
                    if link and not link.startswith('http'):
                        link = base_url + link
                    
                    excerpt_elem = element.select_one('p, .excerpt, .entry-content')
                    excerpt = self.clean_text(excerpt_elem.get_text())[:300] if excerpt_elem else title
                    
                    img_elem = element.select_one('img')
                    image_url = img_elem.get('src', '') or img_elem.get('data-src', '') if img_elem else ''
                    
                    if not image_url:
                        image_url = "https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg"
                    
                    articles.append({
                        'id': str(uuid.uuid4()),
                        'titre': title,
                        'slug': self.generate_slug(title),
                        'categorie': self.extract_category(title + " " + excerpt, link),
                        'tags': ['Côte d\'Ivoire', 'Fratmat'],
                        'auteur': 'Fraternité Matin',
                        'image_url': image_url,
                        'contenu': f"{excerpt}\n\nSource: Fraternité Matin\nLire l'article complet: {link}",
                        'extrait': excerpt[:200] if len(excerpt) > 200 else excerpt,
                        'temps_lecture': max(1, len(excerpt.split()) // 200),
                        'created_at': datetime.now(timezone.utc).isoformat(),
                        'updated_at': datetime.now(timezone.utc).isoformat(),
                        'vedette': False,
                        'source': 'fratmat.info',
                        'source_url': link
                    })
                except Exception as e:
                    logger.error(f"Error parsing article from Fratmat: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping Fratmat: {str(e)}")
        
        return articles
    
    async def scrape_rfi_afrique(self, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Scrape RFI Afrique - Section Côte d'Ivoire"""
        articles = []
        url = "https://www.rfi.fr/fr/tag/c%C3%B4te-d-ivoire/"
        
        try:
            html = await self.fetch_page(session, url)
            if not html:
                logger.warning("Could not fetch RFI Afrique")
                return articles
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # RFI utilise des articles avec une structure spécifique
            article_elements = soup.select('article, .article, .o-archive-article')
            
            for element in article_elements[:8]:
                try:
                    title_elem = element.select_one('h2, h3, .article__title, a.o-card__title')
                    if not title_elem:
                        continue
                    
                    title = self.clean_text(title_elem.get_text())
                    if not title or len(title) < 15 or 'côte d\'ivoire' not in title.lower():
                        # S'assurer que l'article concerne la CI
                        continue
                    
                    link_elem = element.select_one('a')
                    link = link_elem.get('href', '') if link_elem else ''
                    if link and not link.startswith('http'):
                        link = "https://www.rfi.fr" + link
                    
                    excerpt_elem = element.select_one('p, .article__desc')
                    excerpt = self.clean_text(excerpt_elem.get_text())[:300] if excerpt_elem else title
                    
                    img_elem = element.select_one('img')
                    image_url = img_elem.get('src', '') or img_elem.get('data-src', '') if img_elem else ''
                    
                    if not image_url:
                        image_url = "https://images.pexels.com/photos/3944454/pexels-photo-3944454.jpeg"
                    
                    articles.append({
                        'id': str(uuid.uuid4()),
                        'titre': title,
                        'slug': self.generate_slug(title),
                        'categorie': self.extract_category(title + " " + excerpt, link),
                        'tags': ['Côte d\'Ivoire', 'Afrique', 'International'],
                        'auteur': 'RFI Afrique',
                        'image_url': image_url,
                        'contenu': f"{excerpt}\n\nSource: RFI Afrique\nLire l'article complet: {link}",
                        'extrait': excerpt[:200] if len(excerpt) > 200 else excerpt,
                        'temps_lecture': max(1, len(excerpt.split()) // 200),
                        'created_at': datetime.now(timezone.utc).isoformat(),
                        'updated_at': datetime.now(timezone.utc).isoformat(),
                        'vedette': True,  # Articles internationaux en vedette
                        'source': 'rfi.fr',
                        'source_url': link
                    })
                except Exception as e:
                    logger.error(f"Error parsing article from RFI: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping RFI: {str(e)}")
        
        return articles
    
    async def get_demo_news(self) -> List[Dict[str, Any]]:
        """Génère des actualités de démonstration pour la Côte d'Ivoire (fallback)"""
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
                'image_url': 'https://images.pexels.com/photos/5212345/pexels-photo-5212345.jpeg'
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
                'categorie': 'Santé',
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
                'source': 'demo'
            })
        
        return articles
    
    async def aggregate_all(self) -> List[Dict[str, Any]]:
        """Agrège toutes les actualités de toutes les sources"""
        all_articles = []
        
        try:
            async with aiohttp.ClientSession() as session:
                # Lancer tous les scrapers en parallèle
                tasks = [
                    self.scrape_abidjan_net(session),
                    self.scrape_fratmat(session),
                    self.scrape_rfi_afrique(session),
                ]
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in results:
                    if isinstance(result, list):
                        all_articles.extend(result)
                    elif isinstance(result, Exception):
                        logger.error(f"Scraper error: {str(result)}")
                
                logger.info(f"Scraped {len(all_articles)} articles from real sources")
                
                # Si aucun article n'a été récupéré, utiliser le fallback
                if len(all_articles) < 3:
                    logger.warning("Not enough articles scraped, adding demo content")
                    demo_articles = await self.get_demo_news()
                    all_articles.extend(demo_articles)
                
                # Dédupliquer par titre similaire
                seen_titles = set()
                unique_articles = []
                for article in all_articles:
                    title_key = article['titre'].lower()[:50]
                    if title_key not in seen_titles:
                        seen_titles.add(title_key)
                        unique_articles.append(article)
                
                # Marquer les 3 premiers comme vedette
                for i, article in enumerate(unique_articles[:3]):
                    article['vedette'] = True
                
                return unique_articles
                
        except Exception as e:
            logger.error(f"Error in aggregate_all: {str(e)}")
            # Retourner du contenu de démo en cas d'erreur
            return await self.get_demo_news()
