import asyncio
from datetime import datetime, timezone
import logging
from typing import List, Dict, Any
import uuid
import random

logger = logging.getLogger(__name__)

class TrainingAggregator:
    """Agrégateur de formations professionnelles"""
    
    def __init__(self):
        pass
    
    async def get_demo_trainings(self) -> List[Dict[str, Any]]:
        """Génère des formations de démonstration pour la Côte d'Ivoire"""
        
        trainings = [
            {
                'titre': 'Formation Téléconseiller Professionnel',
                'thematique': 'Relation Client',
                'niveau': 'Débutant',
                'objectifs': [
                    'Maîtriser les techniques de communication téléphonique',
                    'Gérer efficacement les appels clients',
                    'Traiter les réclamations avec professionnalisme',
                    'Utiliser les outils CRM'
                ],
                'description': 'Formation complète pour devenir téléconseiller professionnel. Inclut modules théoriques et pratiques avec mises en situation réelles.',
                'contenu': '''Module 1 : Fondamentaux de la Relation Client (2 semaines)
- Les bases de la communication
- L\'accueil téléphonique
- La gestion du stress

Module 2 : Techniques de Vente (2 semaines)
- Identification des besoins clients
- Techniques de persuasion
- Conclusion de vente

Module 3 : Gestion des Réclamations (1 semaine)
- Écoute active
- Résolution de conflits
- Satisfaction client

Module 4 : Outils et Pratique (1 semaine)
- Logiciels CRM
- Mises en situation
- Stage pratique''',
                'duree': '3 mois (dont 1 mois de stage)',
                'ressources': [
                    'Manuel de formation',
                    'Accès plateforme e-learning',
                    'Certificat de fin de formation',
                    'Placement en stage garanti'
                ],
                'image_url': 'https://images.pexels.com/photos/7688336/pexels-photo-7688336.jpeg'
            },
            {
                'titre': 'Développement Web avec React & Node.js',
                'thematique': 'Informatique',
                'niveau': 'Intermédiaire',
                'objectifs': [
                    'Créer des applications web modernes avec React',
                    'Développer des API REST avec Node.js',
                    'Gérer des bases de données MongoDB',
                    'Déployer des applications en production'
                ],
                'description': 'Formation intensive pour devenir développeur Full Stack. Technologies actuelles du marché avec projets concrets.',
                'contenu': '''Module 1 : HTML/CSS/JavaScript (3 semaines)
- Fondamentaux du web
- JavaScript moderne (ES6+)
- Responsive design

Module 2 : React (4 semaines)
- Components et Props
- Hooks et State Management
- React Router
- Redux

Module 3 : Node.js & Express (3 semaines)
- Serveur Node.js
- API REST
- Authentification JWT

Module 4 : MongoDB & Déploiement (2 semaines)
- Bases de données NoSQL
- CRUD operations
- Déploiement cloud''',
                'duree': '4 mois',
                'ressources': [
                    'Cours vidéo HD',
                    'Projets pratiques guidés',
                    'Accès à vie au contenu',
                    'Certificat reconnu',
                    'Mentorat personnalisé'
                ],
                'image_url': 'https://images.pexels.com/photos/35539427/pexels-photo-35539427.jpeg'
            },
            {
                'titre': 'Aide-Soignant : Formation Certifiante',
                'thematique': 'Santé',
                'niveau': 'Débutant',
                'objectifs': [
                    'Maîtriser les soins d\'hygiène et de confort',
                    'Surveiller l\'état de santé des patients',
                    'Accompagner dans les actes de la vie quotidienne',
                    'Travailler en équipe pluridisciplinaire'
                ],
                'description': 'Formation diplômante d\'aide-soignant conforme aux standards du Ministère de la Santé. Stage en milieu hospitalier inclus.',
                'contenu': '''Module 1 : Accompagnement d\'une personne (5 semaines)
- Hygiene corporelle
- Aide à l\'alimentation
- Mobilisation

Module 2 : État clinique d\'une personne (3 semaines)
- Signes vitaux
- Observation
- Transmission d\'informations

Module 3 : Soins (4 semaines)
- Prévention infections
- Ergonomie
- Règles d\'hygiène

Module 4 : Travail en équipe (2 semaines)
- Communication professionnelle
- Collaboration pluridisciplinaire

Stages : 12 semaines en hôpital''',
                'duree': '6 mois',
                'ressources': [
                    'Manuel officiel',
                    'Stages en cliniques partenaires',
                    'Diplôme d\'État',
                    'Suivi pédagogique'
                ],
                'image_url': 'https://images.pexels.com/photos/3952231/pexels-photo-3952231.jpeg'
            },
            {
                'titre': 'Marketing Digital & Réseaux Sociaux',
                'thematique': 'Marketing',
                'niveau': 'Intermédiaire',
                'objectifs': [
                    'Elaborer une stratégie marketing digitale',
                    'Gérer les réseaux sociaux professionnels',
                    'Créer des campagnes publicitaires efficaces',
                    'Analyser les performances avec Google Analytics'
                ],
                'description': 'Devenez expert en marketing digital. Formation pratique avec études de cas réels et campagnes live.',
                'contenu': '''Module 1 : Fondamentaux du Digital (2 semaines)
- Eco système digital
- Stratégie de contenu
- Personal branding

Module 2 : Réseaux Sociaux (3 semaines)
- Facebook, Instagram, LinkedIn
- Community management
- Content creation

Module 3 : Publicité en Ligne (3 semaines)
- Google Ads
- Facebook Ads
- Optimisation campagnes

Module 4 : Analytics & ROI (2 semaines)
- Google Analytics
- Mesure de performance
- Reporting''',
                'duree': '3 mois',
                'ressources': [
                    'Certifications Google & Meta',
                    'Outils marketing professionnels',
                    'Portfolio de campagnes',
                    'Placement en agence possible'
                ],
                'image_url': 'https://images.pexels.com/photos/7647950/pexels-photo-7647950.jpeg'
            },
            {
                'titre': 'Comptabilité & Gestion Financière',
                'thematique': 'Gestion',
                'niveau': 'Débutant',
                'objectifs': [
                    'Maîtriser les principes comptables',
                    'Tenir une comptabilité générale',
                    'Etablir des bilans et comptes de résultat',
                    'Utiliser les logiciels comptables'
                ],
                'description': 'Formation en comptabilité pour PME. Parfait pour entrepreneurs et futurs comptables.',
                'contenu': '''Module 1 : Comptabilité Générale (4 semaines)
- Plan comptable SYSCOHADA
- Enregistrement opérations
- Grand livre et balance

Module 2 : Etats Financiers (3 semaines)
- Bilan comptable
- Compte de résultat
- Annexes

Module 3 : Analyse Financière (2 semaines)
- Ratios financiers
- Solvabilité et rentabilité
- Tableau de bord

Module 4 : Pratique Logiciels (3 semaines)
- Sage Compta
- Excel avancé
- Cas pratiques''',
                'duree': '4 mois',
                'ressources': [
                    'Logiciels inclus',
                    'Exercices pratiques',
                    'Certificat professionnel',
                    'Stage en cabinet'
                ],
                'image_url': 'https://images.pexels.com/photos/6863332/pexels-photo-6863332.jpeg'
            }
        ]
        
        # Convertir en format attendu
        formations = []
        for item in trainings:
            slug = item['titre'].lower()
            slug = slug.replace(' ', '-').replace('\'', '')
            
            formations.append({
                'id': str(uuid.uuid4()),
                'titre': item['titre'],
                'slug': slug,
                'thematique': item['thematique'],
                'niveau': item['niveau'],
                'objectifs': item['objectifs'],
                'image_url': item['image_url'],
                'contenu': item['contenu'],
                'description': item['description'],
                'duree': item['duree'],
                'ressources': item['ressources'],
                'created_at': datetime.now(timezone.utc).isoformat(),
                'updated_at': datetime.now(timezone.utc).isoformat(),
                'source': 'aggregated'
            })
        
        return formations
    
    async def aggregate_all(self) -> List[Dict[str, Any]]:
        """Agrège toutes les formations"""
        return await self.get_demo_trainings()