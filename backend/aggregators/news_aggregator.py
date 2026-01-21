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
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.timeout = aiohttp.ClientTimeout(total=20)
    
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
        
        if any(word in text_lower for word in ['sport', 'football', 'basket', 'athlé', 'can ', 'afcon', 'éléphant', 'match', 'championnat']):
            return "Sport"
        elif any(word in text_lower for word in ['économ', 'finance', 'pib', 'croissance', 'banque', 'investiss', 'commerce', 'port', 'export', 'entreprise', 'marché']):
            return "Économie"
        elif any(word in text_lower for word in ['technolog', 'digital', 'startup', 'innov', 'numérique', 'tech', 'internet', 'mobile', 'application']):
            return "Technologie"
        elif any(word in text_lower for word in ['politique', 'gouvernement', 'président', 'ministre', 'élection', 'parlement', 'assemblée', 'parti', 'opposition']):
            return "Politique"
        elif any(word in text_lower for word in ['santé', 'médecin', 'hôpital', 'vaccin', 'maladie', 'oms', 'covid', 'épidémie']):
            return "Santé"
        elif any(word in text_lower for word in ['éducation', 'école', 'université', 'formation', 'étudiant', 'bac', 'diplôme', 'enseignement']):
            return "Éducation"
        elif any(word in text_lower for word in ['culture', 'musique', 'artiste', 'cinéma', 'festival', 'spectacle', 'concert']):
            return "Culture"
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
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching {url}")
            return ""
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return ""
    
    async def scrape_connection_ivoirienne(self, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Scrape Connection Ivoirienne - Portail d'actualités"""
        articles = []
        base_url = "https://www.connectionivoirienne.net"
        
        try:
            html = await self.fetch_page(session, base_url)
            if not html:
                logger.warning("Could not fetch Connection Ivoirienne")
                return articles
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Chercher les articles - structure typique WordPress
            article_elements = soup.select('article, .post, .entry, .news-item, .td-block-span6, .td-block-span12')
            
            if not article_elements:
                # Fallback: chercher les titres avec liens
                article_elements = soup.select('.entry-title, .td-module-title, h3.td-module-title')
            
            for element in article_elements[:10]:
                try:
                    # Extraire le titre
                    title_elem = element.select_one('h3, h2, .entry-title, .td-module-title')
                    if not title_elem:
                        title_elem = element.find('a')
                    
                    if not title_elem:
                        continue
                    
                    title = self.clean_text(title_elem.get_text())
                    if not title or len(title) < 15:
                        continue
                    
                    # Extraire le lien
                    link_elem = element.find('a') or title_elem.find('a')
                    if title_elem.name == 'a':
                        link_elem = title_elem
                    link = link_elem.get('href', '') if link_elem else ''
                    if link and not link.startswith('http'):
                        link = base_url + link
                    
                    # Extraire l'extrait
                    excerpt_elem = element.select_one('.td-excerpt, .entry-summary, p')
                    excerpt = self.clean_text(excerpt_elem.get_text())[:250] if excerpt_elem else title
                    
                    # Extraire l'image avec validation
                    img_elem = element.select_one('img')
                    image_url = ""
                    if img_elem:
                        image_url = img_elem.get('src', '') or img_elem.get('data-src', '') or img_elem.get('data-lazy-src', '')
                    
                    # Valider l'image - exclure les placeholders
                    invalid_patterns = ['data:image', 'blank.gif', 'placeholder', 'loading', '1x1', 'spacer', 'pixel']
                    is_valid_image = image_url and not any(pattern in image_url.lower() for pattern in invalid_patterns)
                    
                    if not is_valid_image:
                        # Images par défaut par catégorie
                        category = self.extract_category(title + " " + excerpt, link)
                        default_images = {
                            "Sport": "https://images.pexels.com/photos/274506/pexels-photo-274506.jpeg",
                            "Économie": "https://images.pexels.com/photos/7647950/pexels-photo-7647950.jpeg",
                            "Technologie": "https://images.pexels.com/photos/8124399/pexels-photo-8124399.jpeg",
                            "Politique": "https://images.pexels.com/photos/1550337/pexels-photo-1550337.jpeg",
                            "Santé": "https://images.pexels.com/photos/3952231/pexels-photo-3952231.jpeg",
                            "Éducation": "https://images.pexels.com/photos/5212345/pexels-photo-5212345.jpeg",
                            "Culture": "https://images.pexels.com/photos/2263436/pexels-photo-2263436.jpeg",
                            "Société": "https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg",
                        }
                        image_url = default_images.get(category, default_images["Société"])
                    
                    articles.append({
                        'id': str(uuid.uuid4()),
                        'titre': title,
                        'slug': self.generate_slug(title),
                        'categorie': self.extract_category(title + " " + excerpt, link),
                        'tags': ['Côte d\'Ivoire', 'Actualité'],
                        'auteur': 'Connection Ivoirienne',
                        'image_url': image_url,
                        'contenu': f"{excerpt}\n\nSource: Connection Ivoirienne\nLire l'article complet: {link}",
                        'extrait': excerpt[:200] if len(excerpt) > 200 else excerpt,
                        'temps_lecture': max(1, len(excerpt.split()) // 200),
                        'created_at': datetime.now(timezone.utc).isoformat(),
                        'updated_at': datetime.now(timezone.utc).isoformat(),
                        'vedette': False,
                        'source': 'connectionivoirienne.net',
                        'source_url': link
                    })
                except Exception as e:
                    logger.debug(f"Error parsing article: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(articles)} articles from Connection Ivoirienne")
            
        except Exception as e:
            logger.error(f"Error scraping Connection Ivoirienne: {str(e)}")
        
        return articles
    
    async def scrape_linfodrome(self, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Scrape L'Infodrome - Actualités Côte d'Ivoire"""
        articles = []
        base_url = "https://www.linfodrome.com"
        
        try:
            html = await self.fetch_page(session, base_url)
            if not html:
                logger.warning("Could not fetch L'Infodrome")
                return articles
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Chercher les articles
            article_elements = soup.select('article, .post, .entry, .news-box, .article-box, .item-news')
            
            if not article_elements:
                article_elements = soup.select('h2 a, h3 a, .title a')
            
            for element in article_elements[:10]:
                try:
                    title_elem = element.select_one('h2, h3, .title, a')
                    if not title_elem:
                        title_elem = element if element.name == 'a' else None
                    
                    if not title_elem:
                        continue
                    
                    title = self.clean_text(title_elem.get_text())
                    if not title or len(title) < 15:
                        continue
                    
                    link_elem = element.find('a') or (title_elem if title_elem.name == 'a' else title_elem.find('a'))
                    link = link_elem.get('href', '') if link_elem else ''
                    if link and not link.startswith('http'):
                        link = base_url + link
                    
                    excerpt_elem = element.select_one('p, .excerpt, .summary, .description')
                    excerpt = self.clean_text(excerpt_elem.get_text())[:250] if excerpt_elem else title
                    
                    img_elem = element.select_one('img')
                    image_url = ""
                    if img_elem:
                        image_url = img_elem.get('src', '') or img_elem.get('data-src', '')
                    
                    if not image_url:
                        image_url = "https://images.pexels.com/photos/3944454/pexels-photo-3944454.jpeg"
                    
                    articles.append({
                        'id': str(uuid.uuid4()),
                        'titre': title,
                        'slug': self.generate_slug(title),
                        'categorie': self.extract_category(title + " " + excerpt, link),
                        'tags': ['Côte d\'Ivoire', 'Infodrome'],
                        'auteur': "L'Infodrome",
                        'image_url': image_url,
                        'contenu': f"{excerpt}\n\nSource: L'Infodrome\nLire l'article complet: {link}",
                        'extrait': excerpt[:200] if len(excerpt) > 200 else excerpt,
                        'temps_lecture': max(1, len(excerpt.split()) // 200),
                        'created_at': datetime.now(timezone.utc).isoformat(),
                        'updated_at': datetime.now(timezone.utc).isoformat(),
                        'vedette': False,
                        'source': 'linfodrome.com',
                        'source_url': link
                    })
                except Exception as e:
                    logger.debug(f"Error parsing article from Linfodrome: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(articles)} articles from L'Infodrome")
            
        except Exception as e:
            logger.error(f"Error scraping L'Infodrome: {str(e)}")
        
        return articles
    
    async def get_demo_news(self) -> List[Dict[str, Any]]:
        """Génère des actualités de démonstration pour la Côte d'Ivoire (fallback)"""
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

Les jeunes âgés de 18 à 35 ans peuvent déjà s'inscrire en ligne sur le portail dédié.''',
                'tags': ['emploi', 'jeunesse', 'gouvernement'],
                'auteur': 'Agence Ivoirienne de Presse',
                'image_url': 'https://images.pexels.com/photos/6794928/pexels-photo-6794928.jpeg'
            },
            {
                'titre': 'Les Éléphants se Préparent pour les Compétitions Africaines',
                'categorie': 'Sport',
                'extrait': 'L\'équipe nationale de Côte d\'Ivoire se prépare intensivement pour les prochaines compétitions continentales.',
                'contenu': '''Les Éléphants de Côte d'Ivoire intensifient leur préparation en vue des prochaines échéances africaines.

L'équipe nationale a entamé un stage de préparation à Abidjan avec un effectif de 28 joueurs. Plusieurs stars évoluant en Europe ont répondu présent.

Le calendrier de préparation comprend plusieurs matchs amicaux contre des sélections africaines de premier plan. L'objectif affiché est clair : briller sur la scène continentale.''',
                'tags': ['football', 'sport', 'Éléphants'],
                'auteur': 'Sport Plus CI',
                'image_url': 'https://images.pexels.com/photos/274506/pexels-photo-274506.jpeg'
            },
            {
                'titre': 'Transformation Digitale : Abidjan Devient un Hub Tech en Afrique',
                'categorie': 'Technologie',
                'extrait': 'La capitale économique ivoirienne attire de plus en plus de startups technologiques et d\'investisseurs internationaux.',
                'contenu': '''Abidjan s'impose progressivement comme un hub technologique majeur en Afrique de l'Ouest.

Avec l'ouverture récente de nouveaux incubateurs de startups et l'arrivée de géants tech internationaux, la ville connait une transformation digitale sans précédent.

Le gouvernement soutient cette dynamique avec le programme "Côte d'Ivoire Digital" qui vise à former des milliers de développeurs et à créer un écosystème favorable à l'innovation.''',
                'tags': ['technologie', 'startup', 'innovation'],
                'auteur': 'TechAfrique',
                'image_url': 'https://images.pexels.com/photos/8124399/pexels-photo-8124399.jpeg'
            },
            {
                'titre': 'Éducation : Renforcement des Lycées Professionnels',
                'categorie': 'Éducation',
                'extrait': 'Le Ministère de l\'Éducation Nationale investit dans la formation technique et professionnelle.',
                'contenu': '''Dans le cadre du renforcement du système éducatif ivoirien, le gouvernement investit massivement dans les lycées professionnels.

Ces établissements offrent des formations dans des filières porteuses : électricité, mécanique automobile, bâtiment, hôtellerie-restauration, informatique et agriculture moderne.

L'objectif est d'atteindre un taux d'insertion professionnelle de 70% pour les diplômés de ces filières techniques.''',
                'tags': ['éducation', 'formation', 'jeunesse'],
                'auteur': 'Éducation News CI',
                'image_url': 'https://images.pexels.com/photos/5212345/pexels-photo-5212345.jpeg'
            },
            {
                'titre': 'Le Port d\'Abidjan Confirme sa Position de Leader Régional',
                'categorie': 'Économie',
                'extrait': 'Le Port Autonome d\'Abidjan enregistre une hausse significative de son trafic, consolidant sa position de premier port d\'Afrique de l\'Ouest.',
                'contenu': '''Le Port Autonome d'Abidjan (PAA) confirme son statut de poumon économique de la Côte d'Ivoire avec des résultats exceptionnels.

Avec un trafic en hausse par rapport à l'année précédente, le port traite des millions de tonnes de marchandises annuellement. Cette performance est attribuée aux investissements dans la modernisation des infrastructures.

Le PAA dessert également les pays enclavés de la sous-région, renforçant son rôle de hub logistique régional.''',
                'tags': ['économie', 'commerce', 'infrastructure'],
                'auteur': 'Business Côte d\'Ivoire',
                'image_url': 'https://images.pexels.com/photos/7647950/pexels-photo-7647950.jpeg'
            },
            {
                'titre': 'Campagne de Vaccination Nationale : Un Succès',
                'categorie': 'Santé',
                'extrait': 'Le Ministère de la Santé célèbre le succès de la campagne de vaccination qui a touché des millions d\'enfants.',
                'contenu': '''Le Ministère de la Santé et de l'Hygiène Publique se félicite des résultats de sa campagne nationale de vaccination.

Cette opération a permis d'immuniser des millions d'enfants contre plusieurs maladies : rougeole, poliomyélite, diphtérie et coqueluche.

Des milliers d'agents de santé ont été mobilisés sur l'ensemble du territoire. La campagne a bénéficié du soutien de l'OMS et de l'UNICEF.''',
                'tags': ['santé', 'vaccination', 'enfance'],
                'auteur': 'Santé Info CI',
                'image_url': 'https://images.pexels.com/photos/3952231/pexels-photo-3952231.jpeg'
            }
        ]
        
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
                    self.scrape_connection_ivoirienne(session),
                    self.scrape_linfodrome(session),
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
            return await self.get_demo_news()
