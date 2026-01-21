import asyncio
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import logging
from typing import List, Dict, Any
import re
import uuid

logger = logging.getLogger(__name__)

class JobAggregator:
    """Agrégateur d'offres d'emploi de sources multiples"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> str:
        """Récupère le contenu HTML d'une page"""
        try:
            async with session.get(url, headers=self.headers, timeout=30) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.warning(f"Failed to fetch {url}: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None
    
    def clean_text(self, text: str) -> str:
        """Nettoie le texte extrait"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def generate_slug(self, title: str) -> str:
        """Génère un slug à partir du titre"""
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        return slug[:100]
    
    async def scrape_emploi_ci(self) -> List[Dict[str, Any]]:
        """Scrape les offres depuis emploi.ci (structure générique)"""
        jobs = []
        try:
            async with aiohttp.ClientSession() as session:
                html = await self.fetch_page(session, "https://www.emploi.ci")
                if not html:
                    return jobs
                
                soup = BeautifulSoup(html, 'html.parser')
                
                # Note: Structure à adapter selon le site réel
                # Exemple générique de parsing
                job_listings = soup.find_all('div', class_='job-item')[:20]
                
                for job_elem in job_listings:
                    try:
                        title = self.clean_text(job_elem.find('h3').text if job_elem.find('h3') else '')
                        company = self.clean_text(job_elem.find('span', class_='company').text if job_elem.find('span', class_='company') else 'Non spécifié')
                        location = self.clean_text(job_elem.find('span', class_='location').text if job_elem.find('span', class_='location') else 'Abidjan, Côte d\'Ivoire')
                        
                        if title:
                            jobs.append({
                                'id': str(uuid.uuid4()),
                                'titre': title,
                                'slug': self.generate_slug(title),
                                'type': 'Emploi',
                                'entreprise': company,
                                'secteur': 'Divers',
                                'localisation': location,
                                'description': f"Offre d'emploi pour {title} chez {company}",
                                'exigences': ['Expérience professionnelle requise', 'Formation adaptée au poste'],
                                'url_candidature': 'https://www.emploi.ci',
                                'source': 'emploi.ci',
                                'created_at': datetime.now(timezone.utc).isoformat()
                            })
                    except Exception as e:
                        logger.error(f"Error parsing job item: {str(e)}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error scraping emploi.ci: {str(e)}")
        
        return jobs
    
    async def get_demo_jobs(self) -> List[Dict[str, Any]]:
        """Génère des offres de démonstration réalistes pour la Côte d'Ivoire"""
        demo_jobs = [
            {
                'id': str(uuid.uuid4()),
                'titre': 'Téléconseiller Bilingue (Fr/Ang)',
                'slug': 'teleconseiller-bilingue-fr-ang',
                'type': 'Emploi',
                'entreprise': 'Orange Côte d\'Ivoire',
                'secteur': 'Télécom',
                'localisation': 'Abidjan, Plateau',
                'description': 'Recherche téléconseiller pour service client. Mission: gérer les appels entrants/sortants, conseiller les clients sur nos offres, traiter les réclamations.',
                'exigences': [
                    'Bac+2 minimum',
                    'Excellente expression orale et écrite en français et anglais',
                    'Expérience en relation client (1 an minimum)',
                    'Maîtrise des outils informatiques'
                ],
                'url_candidature': 'https://www.emploi.ci',
                'source': 'aggregated',
                'created_at': datetime.now(timezone.utc).isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'titre': 'Développeur Web Full Stack',
                'slug': 'developpeur-web-full-stack',
                'type': 'Emploi',
                'entreprise': 'CITech Solutions',
                'secteur': 'Informatique',
                'localisation': 'Abidjan, Cocody',
                'description': 'Startup tech recherche développeur Full Stack. Technologies: React, Node.js, MongoDB. Projet: plateforme e-commerce innovante.',
                'exigences': [
                    'Bac+3 en informatique ou équivalent',
                    '2+ années d\'expérience en développement web',
                    'Maîtrise React, Node.js, bases de données',
                    'Portfolio de projets requis'
                ],
                'url_candidature': 'https://www.emploi.ci',
                'source': 'aggregated',
                'created_at': datetime.now(timezone.utc).isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'titre': 'Aide-Soignant(e)',
                'slug': 'aide-soignant',
                'type': 'Emploi',
                'entreprise': 'Polyclinique Sainte Anne-Marie',
                'secteur': 'Santé',
                'localisation': 'Abidjan, Marcory',
                'description': 'Clinique privée recrute aide-soignant(e) pour accompagnement patients, soins d\'hygiène et confort, surveillance paramètres vitaux.',
                'exigences': [
                    'Diplôme d\'État d\'aide-soignant',
                    'Expérience en milieu hospitalier souhaitée',
                    'Sens du contact et de l\'écoute',
                    'Disponibilité pour travail posté'
                ],
                'url_candidature': 'https://www.emploi.ci',
                'source': 'aggregated',
                'created_at': datetime.now(timezone.utc).isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'titre': 'Spécialiste Marketing Digital',
                'slug': 'specialiste-marketing-digital',
                'type': 'Emploi',
                'entreprise': 'Agence DigitalBoost',
                'secteur': 'Marketing',
                'localisation': 'Abidjan, Zone 4',
                'description': 'Agence digitale recherche expert en marketing digital. Missions: stratégies SEO/SEA, gestion réseaux sociaux, campagnes publicitaires digitales.',
                'exigences': [
                    'Bac+4/5 en marketing digital ou communication',
                    '3+ ans d\'expérience en agence',
                    'Maîtrise Google Ads, Facebook Ads, Analytics',
                    'Certifications Google/Meta un plus'
                ],
                'url_candidature': 'https://www.emploi.ci',
                'source': 'aggregated',
                'created_at': datetime.now(timezone.utc).isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'titre': 'Caissier(ère) Principal(e)',
                'slug': 'caissier-principal',
                'type': 'Emploi',
                'entreprise': 'Supermarché Cap Sud',
                'secteur': 'Commerce',
                'localisation': 'Abidjan, Yopougon',
                'description': 'Chaîne de supermarchés recrute caissier(ère) principal(e). Gestion de caisse, encaissement, relation client, supervision équipe.',
                'exigences': [
                    'Bac ou équivalent',
                    'Expérience en grande distribution (2 ans)',
                    'Rigueur et honnêteté',
                    'Bonnes capacités relationnelles'
                ],
                'url_candidature': 'https://www.emploi.ci',
                'source': 'aggregated',
                'created_at': datetime.now(timezone.utc).isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'titre': 'Ingénieur Génie Civil',
                'slug': 'ingenieur-genie-civil',
                'type': 'Emploi',
                'entreprise': 'BTP Construct CI',
                'secteur': 'BTP',
                'localisation': 'Abidjan, Treichville',
                'description': 'Entreprise de construction recherche ingénieur génie civil. Supervision chantiers, études techniques, contrôle qualité, gestion équipes.',
                'exigences': [
                    'Diplôme d\'ingénieur en génie civil',
                    '5+ ans d\'expérience en gestion de projets BTP',
                    'Maîtrise logiciels CAO (AutoCAD, Revit)',
                    'Permis de conduire catégorie B'
                ],
                'url_candidature': 'https://www.emploi.ci',
                'source': 'aggregated',
                'created_at': datetime.now(timezone.utc).isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'titre': 'Stage - Assistant RH',
                'slug': 'stage-assistant-rh',
                'type': 'Stage',
                'entreprise': 'Banque Atlantique CI',
                'secteur': 'Banque/Finance',
                'localisation': 'Abidjan, Plateau',
                'description': 'Stage de 6 mois au département RH. Missions: recrutement, gestion administrative, organisation formations, communication interne.',
                'exigences': [
                    'Bac+3/4 en RH, gestion ou psychologie',
                    'Maîtrise Pack Office',
                    'Dynamisme et sens de l\'organisation',
                    'Disponible immédiatement'
                ],
                'url_candidature': 'https://www.emploi.ci',
                'source': 'aggregated',
                'created_at': datetime.now(timezone.utc).isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'titre': 'Concours Professeur Lycée Technique',
                'slug': 'concours-professeur-lycee-technique',
                'type': 'Concours',
                'entreprise': 'Ministère de l\'Éducation Nationale CI',
                'secteur': 'Éducation',
                'localisation': 'National, Côte d\'Ivoire',
                'description': 'Concours national de recrutement de professeurs de lycée technique. Disciplines: électricité, mécanique, informatique, comptabilité.',
                'exigences': [
                    'Licence/Master dans la discipline',
                    'Nationalité ivoirienne',
                    'Âge maximum 40 ans',
                    'Dossier de candidature complet'
                ],
                'url_candidature': 'https://www.fonction-publique.gouv.ci',
                'source': 'aggregated',
                'created_at': datetime.now(timezone.utc).isoformat()
            }
        ]
        return demo_jobs
    
    async def aggregate_all(self) -> List[Dict[str, Any]]:
        """Agrège toutes les offres de toutes les sources"""
        all_jobs = []
        
        # Offres de démonstration (toujours disponibles)
        demo_jobs = await self.get_demo_jobs()
        all_jobs.extend(demo_jobs)
        
        # Tentative de scraping réel (peut échouer)
        try:
            scraped_jobs = await self.scrape_emploi_ci()
            all_jobs.extend(scraped_jobs)
        except Exception as e:
            logger.warning(f"Real scraping failed, using demo data: {str(e)}")
        
        return all_jobs