import { Link } from 'react-router-dom';
import { Clock, User, ArrowRight } from 'lucide-react';

export const ArticleCard = ({ article, featured = false }) => {
  return (
    <Link
      to={`/actualite/${article.slug}`}
      data-testid={`article-card-${article.slug}`}
      className={`group block bg-white border border-slate-200 overflow-hidden transition-all hover:shadow-lg ${
        featured ? 'row-span-2' : ''
      }`}
    >
      {/* Image */}
      <div className="relative overflow-hidden aspect-[16/9]">
        <img
          src={article.image_url}
          alt={article.titre}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
        />
        <div className="absolute top-4 left-4">
          <span className="px-3 py-1 bg-electric-blue text-white font-mono text-xs font-medium">
            {article.categorie}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className={`p-6 ${featured ? 'p-8' : ''}`}>
        <h3
          className={`font-playfair font-bold text-deep-navy mb-3 line-clamp-2 group-hover:text-electric-blue transition-colors ${
            featured ? 'text-2xl' : 'text-xl'
          }`}
        >
          {article.titre}
        </h3>

        <p className="font-inter text-slate-600 text-sm leading-relaxed mb-4 line-clamp-3">
          {article.extrait}
        </p>

        {/* Meta */}
        <div className="flex items-center justify-between pt-4 border-t border-slate-100">
          <div className="flex items-center space-x-4 font-inter text-xs text-slate-500">
            <div className="flex items-center space-x-1">
              <User className="w-3 h-3" />
              <span>{article.auteur}</span>
            </div>
            <div className="flex items-center space-x-1">
              <Clock className="w-3 h-3" />
              <span>{article.temps_lecture} min</span>
            </div>
          </div>

          <ArrowRight className="w-4 h-4 text-electric-blue transition-transform group-hover:translate-x-1" />
        </div>
      </div>
    </Link>
  );
};