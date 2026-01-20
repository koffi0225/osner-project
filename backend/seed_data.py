import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timezone
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Sample data
articles_data = [
    {
        "id": str(uuid.uuid4()),
        "titre": "La transformation numérique dans l'éducation",
        "slug": "transformation-numerique-education",
        "categorie": "Éducation",
        "tags": ["numérique", "innovation", "école"],
        "auteur": "Sophie Martin",
        "image_url": "https://images.pexels.com/photos/35539427/pexels-photo-35539427.jpeg",
        "contenu": "L'éducation connaît une révolution sans précédent avec l'intégration massive des technologies numériques. Des tableaux interactifs aux plateformes d'apprentissage en ligne, les outils se multiplient pour enrichir l'expérience pédagogique.\n\nLes enseignants adaptent leurs méthodes, créant des parcours personnalisés pour chaque élève. Cette transformation permet également de franchir les barrières géographiques, offrant un accès équitable à une éducation de qualité.\n\nToutefois, cette évolution soulève des questions importantes sur l'équité d'accès aux technologies et la formation des enseignants. Un défi majeur consiste à garantir que personne ne soit laissé pour compte dans cette transition vers l'école du futur.",
        "extrait": "L'intégration des technologies numériques transforme radicalement les méthodes d'enseignement et d'apprentissage.",
        "temps_lecture": 5,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "vedette": True
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "L'intelligence artificielle au service de la société",
        "slug": "ia-service-societe",
        "categorie": "Technologie",
        "tags": ["IA", "innovation", "société"],
        "auteur": "Marc Dubois",
        "image_url": "https://images.pexels.com/photos/8124399/pexels-photo-8124399.jpeg",
        "contenu": "L'intelligence artificielle n'est plus une technologie futuriste. Elle est déjà présente dans notre quotidien : assistants vocaux, recommandations personnalisées, diagnostic médical, et bien plus encore.\n\nLes applications bénéfiques de l'IA se multiplient dans tous les secteurs. En médecine, elle aide à détecter des maladies plus rapidement. Dans l'agriculture, elle optimise les rendements tout en réduisant l'impact environnemental.\n\nCependant, cette révolution technologique soulève des questions éthiques importantes : protection de la vie privée, biais algorithmiques, impact sur l'emploi. Il est crucial de développer une IA responsable, centrée sur l'humain.",
        "extrait": "Comment l'intelligence artificielle transforme-t-elle notre quotidien et quels sont les enjeux éthiques ?",
        "temps_lecture": 6,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "vedette": True
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Les défis économiques de 2025",
        "slug": "defis-economiques-2025",
        "categorie": "Économie",
        "tags": ["économie", "finance", "2025"],
        "auteur": "Claire Dupont",
        "image_url": "https://images.pexels.com/photos/7647950/pexels-photo-7647950.jpeg",
        "contenu": "L'année 2025 marque un tournant crucial pour l'économie mondiale. Entre inflation persistante, transitions énergétiques et bouleversements géopolitiques, les défis s'accumulent.\n\nLes entreprises doivent naviguer dans un environnement complexe, marqué par des incertitudes sur les chaînes d'approvisionnement et les coûts de l'énergie. La transformation écologique nécessite des investissements massifs tout en préservant la compétitivité.\n\nLes gouvernements jonglent entre soutien à l'économie et maîtrise des déficits. Les politiques monétaires restent un outil clé, mais leur efficacité est questionnée. L'adaptation et l'innovation seront essentielles pour surmonter ces défis.",
        "extrait": "Analyse des principaux enjeux économiques qui façonneront l'année 2025.",
        "temps_lecture": 7,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "vedette": True
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Le marché de l'emploi se transforme",
        "slug": "marche-emploi-transformation",
        "categorie": "Emploi",
        "tags": ["emploi", "compétences", "formation"],
        "auteur": "Thomas Leroy",
        "image_url": "https://images.pexels.com/photos/6794928/pexels-photo-6794928.jpeg",
        "contenu": "Le monde du travail évolue rapidement. Le télétravail s'est installé durablement, modifiant les attentes des employés et les stratégies des employeurs.\n\nLes compétences recherchées changent : agilité, capacité d'adaptation et compétences numériques deviennent essentielles. La formation continue n'est plus une option mais une nécessité pour rester compétitif sur le marché.\n\nParallèlement, de nouveaux métiers émergent tandis que d'autres disparaissent. L'accompagnement des transitions professionnelles devient crucial pour garantir l'employabilité de tous.",
        "extrait": "Comment le marché de l'emploi évolue-t-il et quelles compétences seront essentielles demain ?",
        "temps_lecture": 5,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "vedette": False
    }
]

formations_data = [
    {
        "id": str(uuid.uuid4()),
        "titre": "Initiation au développement web",
        "slug": "initiation-developpement-web",
        "thematique": "Informatique",
        "niveau": "Débutant",
        "objectifs": [
            "Comprendre les fondamentaux du HTML et CSS",
            "Créer des pages web responsives",
            "Maîtriser les bases de JavaScript",
            "Publier un site web en ligne"
        ],
        "image_url": "https://images.pexels.com/photos/35539427/pexels-photo-35539427.jpeg",
        "contenu": "Cette formation vous accompagne dans vos premiers pas dans le développement web. Vous apprendrez à créer des sites web modernes et attractifs.\n\nModule 1 : Introduction au HTML\n- Structure d'une page web\n- Balises principales\n- Sémantique HTML5\n\nModule 2 : Styliser avec CSS\n- Sélecteurs et propriétés\n- Flexbox et Grid\n- Design responsive\n\nModule 3 : Interactivité avec JavaScript\n- Variables et fonctions\n- Manipulation du DOM\n- Événements utilisateur\n\nModule 4 : Mise en ligne\n- Hébergement web\n- Nom de domaine\n- Maintenance",
        "description": "Apprenez à créer vos premiers sites web avec HTML, CSS et JavaScript. Formation pratique avec projets concrets.",
        "duree": "40 heures",
        "ressources": [
            "Support de cours PDF",
            "Exercices pratiques",
            "Vidéos tutoriels",
            "Accès à une communauté d'entraide"
        ],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Marketing digital avancé",
        "slug": "marketing-digital-avance",
        "thematique": "Marketing",
        "niveau": "Avancé",
        "objectifs": [
            "Maîtriser les stratégies SEO avancées",
            "Créer des campagnes publicitaires performantes",
            "Analyser les données marketing",
            "Optimiser le taux de conversion"
        ],
        "image_url": "https://images.pexels.com/photos/7647950/pexels-photo-7647950.jpeg",
        "contenu": "Formation approfondie pour les professionnels du marketing souhaitant maîtriser les techniques avancées du digital.\n\nModule 1 : SEO Technique\n- Optimisation de la vitesse\n- Architecture de site\n- Core Web Vitals\n\nModule 2 : Publicité digitale\n- Google Ads avancé\n- Social Media Ads\n- Retargeting\n\nModule 3 : Analytics et Data\n- Google Analytics 4\n- Data Studio\n- Attribution modeling\n\nModule 4 : Conversion\n- A/B testing\n- UX optimization\n- Funnel analysis",
        "description": "Perfectionnez vos compétences en marketing digital avec des stratégies avancées et orientées résultats.",
        "duree": "60 heures",
        "ressources": [
            "Études de cas réels",
            "Templates et outils",
            "Certification incluse",
            "Mentorat personnalisé"
        ],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Gestion de projet agile",
        "slug": "gestion-projet-agile",
        "thematique": "Management",
        "niveau": "Intermédiaire",
        "objectifs": [
            "Comprendre les principes de l'agilité",
            "Maîtriser Scrum et Kanban",
            "Gérer une équipe agile",
            "Utiliser les outils collaboratifs"
        ],
        "image_url": "https://images.pexels.com/photos/6794928/pexels-photo-6794928.jpeg",
        "contenu": "Apprenez à piloter des projets avec les méthodes agiles pour plus de flexibilité et d'efficacité.\n\nModule 1 : Fondamentaux Agile\n- Manifeste agile\n- Valeurs et principes\n- Vs méthodes traditionnelles\n\nModule 2 : Framework Scrum\n- Rôles (PO, SM, équipe)\n- Cérémonies\n- Artefacts\n\nModule 3 : Méthode Kanban\n- Visualisation du flux\n- Limiter le WIP\n- Amélioration continue\n\nModule 4 : Outils et pratiques\n- Jira, Trello\n- User stories\n- Estimation et vélocité",
        "description": "Devenez expert en gestion de projet agile et pilotez vos équipes vers le succès avec Scrum et Kanban.",
        "duree": "30 heures",
        "ressources": [
            "Guide Scrum officiel",
            "Templates Jira/Trello",
            "Préparation certification",
            "Forum de discussion"
        ],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
]

emplois_data = [
    {
        "id": str(uuid.uuid4()),
        "titre": "Développeur Full Stack JavaScript",
        "slug": "developpeur-fullstack-javascript",
        "type": "Emploi",
        "entreprise": "TechInnovate",
        "secteur": "Informatique",
        "localisation": "Paris, France (Télétravail partiel)",
        "description": "Nous recherchons un développeur Full Stack passionné pour rejoindre notre équipe dynamique. Vous travaillerez sur des projets innovants utilisant React, Node.js et MongoDB.",
        "exigences": [
            "3+ années d'expérience en développement web",
            "Maîtrise de React et Node.js",
            "Connaissance de MongoDB et des API REST",
            "Expérience avec Git et méthodologies agiles",
            "Bon niveau d'anglais technique"
        ],
        "url_candidature": "https://example.com/apply",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Chef de Projet Marketing Digital",
        "slug": "chef-projet-marketing-digital",
        "type": "Emploi",
        "entreprise": "DigiMarket",
        "secteur": "Marketing",
        "localisation": "Lyon, France",
        "description": "Rejoignez notre agence en pleine croissance en tant que Chef de Projet Marketing Digital. Vous piloterez des campagnes pour des clients prestigieux.",
        "exigences": [
            "5+ années en marketing digital",
            "Expertise SEO/SEA et réseaux sociaux",
            "Maîtrise des outils analytics",
            "Excellentes capacités de gestion de projet",
            "Leadership et esprit d'équipe"
        ],
        "url_candidature": "https://example.com/apply",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Stage Data Analyst",
        "slug": "stage-data-analyst",
        "type": "Stage",
        "entreprise": "DataCorp",
        "secteur": "Data Science",
        "localisation": "Toulouse, France",
        "description": "Stage de 6 mois pour étudiant en fin d'études. Vous participerez à l'analyse de données et à la création de dashboards pour nos clients.",
        "exigences": [
            "Formation en data science ou statistiques",
            "Connaissance de Python et SQL",
            "Maîtrise d'Excel avancé",
            "Curiosité et rigueur analytique",
            "Disponibilité 6 mois minimum"
        ],
        "url_candidature": "https://example.com/apply",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Concours Enseignant Numérique",
        "slug": "concours-enseignant-numerique",
        "type": "Concours",
        "entreprise": "Ministère de l'Éducation",
        "secteur": "Éducation",
        "localisation": "National, France",
        "description": "Concours national pour le recrutement d'enseignants spécialisés dans le numérique éducatif. Mission : former les élèves aux compétences digitales.",
        "exigences": [
            "Master 2 ou équivalent",
            "Compétences pédagogiques démontrées",
            "Expertise en outils numériques",
            "Capacité d'animation et de formation",
            "Nationalité française ou UE"
        ],
        "url_candidature": "https://example.com/concours",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
]

async def seed_database():
    print("🌱 Début du seeding de la base de données...")
    
    # Clear existing data
    await db.articles.delete_many({})
    await db.formations.delete_many({})
    await db.emplois.delete_many({})
    print("✅ Collections vidées")
    
    # Insert articles
    await db.articles.insert_many(articles_data)
    print(f"✅ {len(articles_data)} articles insérés")
    
    # Insert formations
    await db.formations.insert_many(formations_data)
    print(f"✅ {len(formations_data)} formations insérées")
    
    # Insert emplois
    await db.emplois.insert_many(emplois_data)
    print(f"✅ {len(emplois_data)} offres d'emploi insérées")
    
    print("🎉 Seeding terminé avec succès!")

if __name__ == "__main__":
    asyncio.run(seed_database())
    client.close()
