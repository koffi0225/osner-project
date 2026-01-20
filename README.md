# Plateforme E1 - Actualité, Formation & Emploi

Plateforme numérique moderne combinant **média d'actualité**, **centre de formation** et **hub d'orientation professionnelle**.

## 🎯 Fonctionnalités

### Section Actualité
- Listing d'articles avec filtres par catégorie
- Recherche avancée
- Pages détaillées avec contenu riche
- Articles en vedette (disposition Tetris Grid)
- Articles similaires

### Section Formation
- Catalogue de formations
- Filtres par niveau (Débutant, Intermédiaire, Avancé)
- Objectifs et contenu détaillés
- Ressources téléchargeables

### Section Emploi & Carrière
- Offres d'emploi, stages, concours
- Filtres par type, secteur, localisation
- Recherche multicritères
- Liens de candidature

### Dashboard Administrateur
- Gestion complète des articles (CRUD)
- Gestion des formations (CRUD)
- Gestion des offres d'emploi (CRUD)
- Interface intuitive avec tabs

### Newsletter
- Inscription par email
- Validation et feedback utilisateur

## 🎨 Design

- **Typographie** : Playfair Display (titres), Inter (corps de texte), JetBrains Mono (technique)
- **Palette** : Swiss Authority - Deep Navy (#0F172A) + Electric Blue (#2563EB)
- **Layout** : Responsive (mobile, tablette, desktop)
- **Components** : Shadcn UI + composants personnalisés

## 🛠 Stack Technique

### Backend
- **Framework** : FastAPI
- **Base de données** : MongoDB
- **ORM** : Motor (async MongoDB driver)

### Frontend
- **Framework** : React 19
- **Routing** : React Router v7
- **Styling** : Tailwind CSS
- **UI Library** : Shadcn UI (Radix UI)
- **Icons** : Lucide React

## 📁 Structure du projet

```
/app
├── backend/
│   ├── server.py          # API FastAPI
│   ├── seed_data.py       # Script de données de démo
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── pages/         # Pages principales
│   │   ├── components/    # Composants réutilisables
│   │   │   ├── admin/     # Composants admin
│   │   │   └── ui/        # Shadcn UI components
│   │   ├── App.js
│   │   └── index.css
│   ├── package.json
│   └── .env
└── README.md
```

## 🚀 Démarrage rapide

### Prérequis
- Python 3.11+
- Node.js 18+
- MongoDB

### Installation

1. **Backend**
```bash
cd /app/backend
pip install -r requirements.txt
python seed_data.py  # Charger les données de démo
```

2. **Frontend**
```bash
cd /app/frontend
yarn install
```

### Lancement

Les services sont gérés par Supervisor :
```bash
sudo supervisorctl status
sudo supervisorctl restart backend frontend
```

Accès :
- Frontend : http://localhost:3000
- Backend API : http://localhost:8001

## 📊 API Endpoints

### Articles
- `GET /api/articles` - Liste des articles (avec filtres)
- `GET /api/articles/{slug}` - Détail d'un article
- `POST /api/articles` - Créer un article
- `PUT /api/articles/{id}` - Mettre à jour un article
- `DELETE /api/articles/{id}` - Supprimer un article

### Formations
- `GET /api/formations` - Liste des formations
- `GET /api/formations/{slug}` - Détail d'une formation
- `POST /api/formations` - Créer une formation
- `PUT /api/formations/{id}` - Mettre à jour une formation
- `DELETE /api/formations/{id}` - Supprimer une formation

### Emplois
- `GET /api/emplois` - Liste des offres
- `GET /api/emplois/{slug}` - Détail d'une offre
- `POST /api/emplois` - Créer une offre
- `PUT /api/emplois/{id}` - Mettre à jour une offre
- `DELETE /api/emplois/{id}` - Supprimer une offre

### Newsletter
- `POST /api/newsletter` - Inscription newsletter

## 🎭 Données de démonstration

Le script `seed_data.py` charge :
- 4 articles (3 en vedette)
- 3 formations (différents niveaux)
- 4 offres d'emploi (emploi, stage, concours)

## 🔐 Sécurité

- Variables d'environnement pour les credentials
- Validation Pydantic côté backend
- CORS configuré
- Exclusion des `_id` MongoDB dans les réponses

## 📱 Responsive Design

- Mobile : navigation hamburger, grilles adaptatives
- Tablette : layout optimisé
- Desktop : expérience complète avec grilles multi-colonnes

## 🎯 Prochaines étapes (Phase 2)

- [ ] Authentification utilisateurs (JWT ou Google Auth)
- [ ] Profils utilisateurs
- [ ] Sauvegarde d'articles favoris
- [ ] Alertes emploi personnalisées
- [ ] Système de commentaires
- [ ] Monétisation (contenus premium)
- [ ] E-learning avec vidéos et quiz

## 📝 Notes techniques

- Hot reload activé pour backend et frontend
- API préfixée avec `/api` pour routing Kubernetes
- Base de données MongoDB accessible via `MONGO_URL`
- Frontend utilise `REACT_APP_BACKEND_URL` pour les appels API
- Tests automatisés disponibles : `pytest /app/backend_test.py`

## 📄 Licence

© 2025 E1 Platform. Tous droits réservés.
