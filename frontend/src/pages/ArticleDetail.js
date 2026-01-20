import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { Clock, User, ArrowLeft, Share2, Calendar } from 'lucide-react';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
import { ArticleCard } from '@/components/ArticleCard';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ArticleDetail = () => {
  const { slug } = useParams();
  const [article, setArticle] = useState(null);
  const [relatedArticles, setRelatedArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadArticle();
  }, [slug]);

  const loadArticle = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/articles/${slug}`);
      setArticle(response.data);

      // Load related articles from the same category
      const relatedRes = await axios.get(`${API}/articles?categorie=${response.data.categorie}&limit=3`);
      setRelatedArticles(relatedRes.data.filter(a => a.slug !== slug).slice(0, 3));
    } catch (error) {
      console.error('Erreur lors du chargement de l\'article:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-electric-blue border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="font-inter text-slate-600">Chargement...</p>
        </div>
      </div>
    );
  }

  if (!article) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="font-inter text-slate-600 mb-4">Article non trouvé</p>
          <Link to="/actualite" className="text-electric-blue hover:underline">
            Retour aux articles
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Back Button */}
      <div className="bg-white border-b border-slate-200">
        <div className="max-w-4xl mx-auto px-4 md:px-8 py-4">
          <Link
            to="/actualite"
            data-testid="back-to-articles"
            className="inline-flex items-center space-x-2 text-slate-600 hover:text-electric-blue transition-colors font-inter text-sm"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Retour aux articles</span>
          </Link>
        </div>
      </div>

      {/* Article Header */}
      <article className="bg-white py-12">
        <div className="max-w-4xl mx-auto px-4 md:px-8">
          {/* Category */}
          <div className="mb-6">
            <span className="px-3 py-1 bg-electric-blue text-white font-mono text-xs font-medium">
              {article.categorie}
            </span>
          </div>

          {/* Title */}
          <h1 className="font-playfair text-4xl md:text-5xl font-bold text-deep-navy mb-6 leading-tight">
            {article.titre}
          </h1>

          {/* Meta */}
          <div className="flex flex-wrap items-center gap-6 mb-8 pb-8 border-b border-slate-200">
            <div className="flex items-center space-x-2 font-inter text-sm text-slate-600">
              <User className="w-4 h-4" />
              <span>{article.auteur}</span>
            </div>
            <div className="flex items-center space-x-2 font-inter text-sm text-slate-600">
              <Calendar className="w-4 h-4" />
              <span>{format(new Date(article.created_at), 'dd MMMM yyyy', { locale: fr })}</span>
            </div>
            <div className="flex items-center space-x-2 font-inter text-sm text-slate-600">
              <Clock className="w-4 h-4" />
              <span>{article.temps_lecture} min de lecture</span>
            </div>
            <button
              data-testid="share-button"
              className="ml-auto flex items-center space-x-2 text-electric-blue hover:text-blue-700 transition-colors font-inter text-sm font-medium"
            >
              <Share2 className="w-4 h-4" />
              <span>Partager</span>
            </button>
          </div>

          {/* Featured Image */}
          <div className="mb-12">
            <img
              src={article.image_url}
              alt={article.titre}
              className="w-full aspect-[16/9] object-cover"
            />
          </div>

          {/* Content */}
          <div className="prose prose-lg max-w-none">
            <div className="font-inter text-slate-700 leading-relaxed whitespace-pre-line">
              {article.contenu}
            </div>
          </div>

          {/* Tags */}
          {article.tags && article.tags.length > 0 && (
            <div className="mt-12 pt-8 border-t border-slate-200">
              <h3 className="font-playfair text-lg font-bold text-deep-navy mb-4">Tags</h3>
              <div className="flex flex-wrap gap-2">
                {article.tags.map((tag) => (
                  <span
                    key={tag}
                    className="px-3 py-1 bg-slate-100 text-slate-700 font-mono text-xs"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </article>

      {/* Related Articles */}
      {relatedArticles.length > 0 && (
        <section className="bg-slate-50 py-16">
          <div className="max-w-7xl mx-auto px-4 md:px-8">
            <h2 className="font-playfair text-3xl font-bold text-deep-navy mb-8">
              Articles similaires
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {relatedArticles.map((relatedArticle) => (
                <ArticleCard key={relatedArticle.id} article={relatedArticle} />
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default ArticleDetail;