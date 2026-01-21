# Osner-Group Platform - Product Requirements Document

## Original Problem Statement
Web platform for "Osner-Group" company serving as a news media outlet, training center, and professional orientation hub in Côte d'Ivoire.

## User Personas
- **Job Seekers**: Young professionals looking for employment opportunities
- **Students**: Seeking training and educational resources
- **General Public**: Interested in Ivorian news and current events
- **Recruiters**: Posting job opportunities (future feature)

## Core Requirements

### Phase 1 (MVP) - COMPLETED ✅
1. **News Section** - Display articles filterable by category
2. **Training Section** - List training programs and educational resources
3. **Jobs & Career Section** - Post job/internship offers and career advice
4. **Branding** - Osner-Group identity with Red/White color scheme

### Phase 2 (Advanced Features) - COMPLETED ✅
1. **Candidate Space**
   - ✅ User registration and login (JWT authentication)
   - ✅ Profile management
   - ✅ CV upload functionality
   
2. **Content Aggregation**
   - ✅ Automated news scraping (connectionivoirienne.net, linfodrome.com)
   - ✅ Job aggregation from online sources
   - ✅ Training aggregation
   - ✅ Daily cron job updates
   - ✅ Admin management interface

3. **AI-Powered Matching**
   - ✅ CV to job matching using GPT-5.2
   - ✅ CV analysis and improvement suggestions

4. **Multi-Method Payments**
   - ✅ Stripe (Visa/Mastercard)
   - ✅ Orange Money
   - ✅ MTN Money
   - ✅ Moov Money
   - ✅ Wave CI (NEW)
   - ✅ Trésor Money
   - ✅ Bank Transfer (BDA)
   - ✅ PDF receipt generation

## Technical Architecture

```
/app/
├── backend/
│   ├── aggregators/       # Web scraping modules
│   │   ├── news_aggregator.py     # Real news scraping
│   │   ├── job_aggregator.py      # Job aggregation
│   │   └── training_aggregator.py # Training aggregation
│   ├── utils/
│   │   ├── payment_processor.py   # Multi-payment handling
│   │   └── receipt_generator.py   # PDF generation
│   ├── auth.py            # JWT authentication
│   ├── server.py          # Main FastAPI app
│   └── *_routes.py        # API route handlers
└── frontend/
    └── src/
        ├── components/    # Reusable React components
        ├── context/       # AuthContext
        └── pages/         # Page components
```

## API Endpoints

### Public Endpoints
- `GET /api/articles` - News articles
- `GET /api/formations` - Training programs
- `GET /api/emplois` - Job listings
- `GET /api/payments-multi/methods` - Payment methods
- `GET /api/payments-multi/packages` - Payment packages

### Protected Endpoints (JWT required)
- `POST /api/candidate/register` - User registration
- `POST /api/candidate/login` - User login
- `POST /api/candidate/upload-cv` - CV upload
- `POST /api/candidate/match-jobs` - AI job matching
- `POST /api/payments-multi/initiate` - Start payment

### Admin Endpoints
- `POST /api/aggregation/update-all` - Trigger content update
- `POST /api/aggregation/update-news` - Update news only
- `GET /api/aggregation/status` - Check aggregation status

## Database Schema (MongoDB)

### Collections
- **users**: {email, password_hash, nom, prenom, sexe, code_inscription, credits, cv_data}
- **articles**: {titre, slug, categorie, contenu, extrait, auteur, image_url, source, vedette}
- **formations**: {titre, slug, thematique, description, niveau, duree, formateur}
- **emplois**: {titre, slug, description, entreprise, localisation, type_contrat}
- **payment_transactions**: {transaction_id, user_id, amount, payment_method, status}

## Third-Party Integrations

| Service | Purpose | Status |
|---------|---------|--------|
| OpenAI GPT-5.2 | CV matching & analysis | ✅ Working (Emergent LLM Key) |
| Stripe | Card payments | ✅ Working (Test mode) |
| Mobile Money | Orange/MTN/Moov/Wave | ⚠️ MOCKED (Manual validation) |

## Recent Changes (January 2026)

### Session Updates
1. **Fixed News Scraper** - Now scrapes real content from connectionivoirienne.net
2. **Added Wave CI** - New payment method for Wave users
3. **Updated Bank Details** - Banque D'Abidjan (BDA): CI201 01001 111803082086 75
4. **Hero Background Image** - Professional image of young businessman
5. **About & Contact Pages** - Pages now linked in footer navigation
6. **Notification System** - Complete notification system for candidates with welcome notifications

## Pending Tasks

### P1 - High Priority
- [x] ~~Link About and Contact pages in navigation~~ ✅ COMPLETED
- [x] ~~Add notification system for candidates~~ ✅ COMPLETED

### P2 - Medium Priority
- [ ] Payment history in candidate dashboard
- [ ] Admin interface for Mobile Money validation
- [ ] Fix mobile navigation bug
- [ ] Real email sending for contact form

### P3 - Future
- [ ] Granular user roles (Admin, Editor, Journalist)
- [ ] Premium content/subscriptions
- [ ] E-learning module with videos
- [ ] Recruiter portal
- [ ] Mobile application

## Known Issues
1. Mobile Money payments are MOCKED - require business-level API integration
2. Some scraped article images may use placeholder images (fallback implemented)

## Contact Information
- **Company**: Osner-Group SARL
- **Manager**: Melvin Tayorault
- **Phone**: +225 07 07 592 286, +225 05 44 498 515
- **Location**: Abidjan, Côte d'Ivoire
