import { Link } from 'react-router-dom';
import { Briefcase, MapPin, Building, ArrowRight } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { fr } from 'date-fns/locale';

export const JobCard = ({ job }) => {
  const getTypeColor = (type) => {
    const colors = {
      'Emploi': 'bg-electric-blue text-white',
      'Stage': 'bg-amber-500 text-white',
      'Concours': 'bg-emerald-500 text-white',
    };
    return colors[type] || 'bg-slate-600 text-white';
  };

  return (
    <Link
      to={`/emploi/${job.slug}`}
      data-testid={`job-card-${job.slug}`}
      className="group block bg-white border border-slate-200 p-6 transition-all hover:shadow-lg hover:border-electric-blue"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="font-playfair text-xl font-bold text-deep-navy mb-2 group-hover:text-electric-blue transition-colors">
            {job.titre}
          </h3>
          <div className="flex items-center space-x-2 mb-3">
            <Building className="w-4 h-4 text-slate-400" />
            <span className="font-inter text-sm text-slate-600 font-medium">{job.entreprise}</span>
          </div>
        </div>
        <span className={`px-3 py-1 font-mono text-xs font-medium ${getTypeColor(job.type)}`}>
          {job.type}
        </span>
      </div>

      <p className="font-inter text-slate-600 text-sm leading-relaxed mb-4 line-clamp-2">
        {job.description}
      </p>

      <div className="flex items-center space-x-4 font-inter text-xs text-slate-500 mb-4">
        <div className="flex items-center space-x-1">
          <Briefcase className="w-3 h-3" />
          <span>{job.secteur}</span>
        </div>
        <div className="flex items-center space-x-1">
          <MapPin className="w-3 h-3" />
          <span>{job.localisation}</span>
        </div>
      </div>

      <div className="flex items-center justify-between pt-4 border-t border-slate-100">
        <span className="font-mono text-xs text-slate-400">
          {formatDistanceToNow(new Date(job.created_at), { addSuffix: true, locale: fr })}
        </span>
        <ArrowRight className="w-4 h-4 text-electric-blue transition-transform group-hover:translate-x-1" />
      </div>
    </Link>
  );
};