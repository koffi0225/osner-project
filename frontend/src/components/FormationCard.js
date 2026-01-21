import { Link } from 'react-router-dom';
import { GraduationCap, Clock, ArrowRight } from 'lucide-react';

export const FormationCard = ({ formation }) => {
  const getNiveauColor = (niveau) => {
    const colors = {
      'Débutant': 'bg-green-100 text-green-700',
      'Intermédiaire': 'bg-blue-100 text-blue-700',
      'Avancé': 'bg-purple-100 text-purple-700',
    };
    return colors[niveau] || 'bg-slate-100 text-slate-700';
  };

  return (
    <Link
      to={`/formation/${formation.slug}`}
      data-testid={`formation-card-${formation.slug}`}
      className="group block bg-white border border-slate-200 overflow-hidden transition-all hover:shadow-lg"
    >
      {/* Image */}
      <div className="relative overflow-hidden aspect-[16/9]">
        <img
          src={formation.image_url}
          alt={formation.titre}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
        />
        <div className="absolute top-4 left-4 flex items-center space-x-2">
          <span className={`px-3 py-1 font-mono text-xs font-medium ${getNiveauColor(formation.niveau)}`}>
            {formation.niveau}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        <div className="flex items-center space-x-2 mb-2">
          <GraduationCap className="w-4 h-4 text-osner-red" />
          <span className="font-mono text-xs text-slate-500">{formation.thematique}</span>
        </div>

        <h3 className="font-playfair text-xl font-bold text-deep-navy mb-3 line-clamp-2 group-hover:text-osner-red transition-colors">
          {formation.titre}
        </h3>

        <p className="font-inter text-slate-600 text-sm leading-relaxed mb-4 line-clamp-3">
          {formation.description}
        </p>

        {/* Meta */}
        <div className="flex items-center justify-between pt-4 border-t border-slate-100">
          <div className="flex items-center space-x-1 font-inter text-xs text-slate-500">
            <Clock className="w-3 h-3" />
            <span>{formation.duree}</span>
          </div>

          <ArrowRight className="w-4 h-4 text-osner-red transition-transform group-hover:translate-x-1" />
        </div>
      </div>
    </Link>
  );
};