import { useEffect, useState } from 'react';
import axios from 'axios';
import { ArticleCard } from '@/components/ArticleCard';
import { FormationCard } from '@/components/FormationCard';
import { JobCard } from '@/components/JobCard';
import { NewsletterForm } from '@/components/NewsletterForm';
import { ArrowRight, TrendingUp, BookOpen, Target } from 'lucide-react';
import { Link } from 'react-router-dom';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const [featuredArticles, setFeaturedArticles] = useState([]);
  const [recentArticles, setRecentArticles] = useState([]);
  const [formations, setFormations] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [articlesRes, formationsRes, jobsRes] = await Promise.all([
        axios.get(`${API}/articles?limit=8`),
        axios.get(`${API}/formations?limit=3`),
        axios.get(`${API}/emplois?limit=4`),
      ]);

      const articles = articlesRes.data;
      setFeaturedArticles(articles.filter(a => a.vedette).slice(0, 3));
      setRecentArticles(articles.filter(a => !a.vedette).slice(0, 6));
      setFormations(formationsRes.data);
      setJobs(jobsRes.data);
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-osner-red border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="font-inter text-slate-600">Chargement...</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Hero Section */}
      <section className="relative bg-deep-navy text-white overflow-hidden">
        <div className="absolute inset-0 grain"></div>
        <div className="max-w-7xl mx-auto px-4 md:px-8 py-24 md:py-32 relative z-10">
          <div className="max-w-3xl">
            <h1 className="font-playfair text-4xl sm:text-5xl lg:text-6xl font-bold mb-6 tracking-tight leading-tight">
              Votre plateforme de référence
            </h1>
            <p className="font-inter text-lg md:text-xl text-slate-300 mb-8 leading-relaxed">
              Actualités, formations et opportunités professionnelles réunies en un seul endroit.
              Informez-vous, formez-vous, évoluez.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link
                to="/actualite"
                data-testid="hero-cta-actualite"
                className="px-8 py-4 bg-osner-red text-white font-inter font-medium rounded-none hover:bg-blue-700 transition-colors flex items-center space-x-2"
              >
                <span>Découvrir l'actualité</span>
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                to="/formation"
                data-testid="hero-cta-formation"
                className="px-8 py-4 bg-transparent border-2 border-white text-white font-inter font-medium rounded-none hover:bg-white hover:text-deep-navy transition-colors"
              >
                Explorer les formations
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Articles - Tetris Grid */}
      {featuredArticles.length > 0 && (
        <section className="max-w-7xl mx-auto px-4 md:px-8 py-16">
          <div className="flex items-center justify-between mb-8">
            <h2 className="font-playfair text-3xl md:text-4xl font-bold text-deep-navy flex items-center space-x-3">
              <TrendingUp className="w-8 h-8 text-osner-red" />
              <span>À la Une</span>
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredArticles[0] && (
              <div className="lg:col-span-2 lg:row-span-2">
                <ArticleCard article={featuredArticles[0]} featured={true} />
              </div>
            )}
            {featuredArticles.slice(1).map((article) => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>
        </section>
      )}

      {/* Recent Articles */}
      {recentArticles.length > 0 && (
        <section className="bg-white py-16">
          <div className="max-w-7xl mx-auto px-4 md:px-8">
            <div className="flex items-center justify-between mb-8">
              <h2 className="font-playfair text-3xl md:text-4xl font-bold text-deep-navy">
                Dernières actualités
              </h2>
              <Link
                to="/actualite"
                data-testid="view-all-articles"
                className="font-inter text-sm font-medium text-osner-red hover:underline flex items-center space-x-1"
              >
                <span>Voir tout</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {recentArticles.map((article) => (
                <ArticleCard key={article.id} article={article} />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Formations Section */}
      {formations.length > 0 && (
        <section className="bg-slate-50 py-16">
          <div className="max-w-7xl mx-auto px-4 md:px-8">
            <div className="flex items-center justify-between mb-8">
              <h2 className="font-playfair text-3xl md:text-4xl font-bold text-deep-navy flex items-center space-x-3">
                <BookOpen className="w-8 h-8 text-osner-red" />
                <span>Formations en vedette</span>
              </h2>
              <Link
                to="/formation"
                data-testid="view-all-formations"
                className="font-inter text-sm font-medium text-osner-red hover:underline flex items-center space-x-1"
              >
                <span>Voir tout</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {formations.map((formation) => (
                <FormationCard key={formation.id} formation={formation} />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Jobs Section */}
      {jobs.length > 0 && (
        <section className="bg-white py-16">
          <div className="max-w-7xl mx-auto px-4 md:px-8">
            <div className="flex items-center justify-between mb-8">
              <h2 className="font-playfair text-3xl md:text-4xl font-bold text-deep-navy flex items-center space-x-3">
                <Target className="w-8 h-8 text-osner-red" />
                <span>Opportunités d'emploi</span>
              </h2>
              <Link
                to="/emploi"
                data-testid="view-all-jobs"
                className="font-inter text-sm font-medium text-osner-red hover:underline flex items-center space-x-1"
              >
                <span>Voir tout</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {jobs.map((job) => (
                <JobCard key={job.id} job={job} />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Newsletter Section */}
      <section className="bg-slate-50 py-16">
        <div className="max-w-3xl mx-auto px-4 md:px-8">
          <NewsletterForm />
        </div>
      </section>
    </div>
  );
};

export default Home;