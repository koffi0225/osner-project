import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { ArrowLeft, Briefcase, MapPin, Building, Calendar, ExternalLink, CheckCircle } from 'lucide-react';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
import { JobCard } from '@/components/JobCard';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const EmploiDetail = () => {
  const { slug } = useParams();
  const [job, setJob] = useState(null);
  const [relatedJobs, setRelatedJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadJob();
  }, [slug]);

  const loadJob = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/emplois/${slug}`);
      setJob(response.data);

      // Load related jobs from the same secteur
      const relatedRes = await axios.get(`${API}/emplois?secteur=${response.data.secteur}&limit=4`);
      setRelatedJobs(relatedRes.data.filter(j => j.slug !== slug).slice(0, 3));
    } catch (error) {
      console.error('Erreur lors du chargement de l\'offre:', error);
    } finally {
      setLoading(false);
    }
  };

  const getTypeColor = (type) => {
    const colors = {
      'Emploi': 'bg-osner-red text-white',
      'Stage': 'bg-amber-500 text-white',
      'Concours': 'bg-emerald-500 text-white',
    };
    return colors[type] || 'bg-slate-600 text-white';
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

  if (!job) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="font-inter text-slate-600 mb-4">Offre non trouvée</p>
          <Link to="/emploi" className="text-osner-red hover:underline">
            Retour aux offres
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
            to="/emploi"
            data-testid="back-to-jobs"
            className="inline-flex items-center space-x-2 text-slate-600 hover:text-osner-red transition-colors font-inter text-sm"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Retour aux offres</span>
          </Link>
        </div>
      </div>

      {/* Job Header */}
      <div className="bg-white py-12">
        <div className="max-w-4xl mx-auto px-4 md:px-8">
          {/* Type Badge */}
          <div className="mb-6">
            <span className={`px-3 py-1 font-mono text-xs font-medium ${getTypeColor(job.type)}`}>
              {job.type}
            </span>
          </div>

          {/* Title */}
          <h1 className="font-playfair text-4xl md:text-5xl font-bold text-deep-navy mb-6 leading-tight">
            {job.titre}
          </h1>

          {/* Company Info */}
          <div className="flex flex-wrap items-center gap-6 mb-8 pb-8 border-b border-slate-200">
            <div className="flex items-center space-x-2 font-inter text-base text-slate-700">
              <Building className="w-5 h-5 text-osner-red" />
              <span className="font-medium">{job.entreprise}</span>
            </div>
            <div className="flex items-center space-x-2 font-inter text-sm text-slate-600">
              <Briefcase className="w-4 h-4" />
              <span>{job.secteur}</span>
            </div>
            <div className="flex items-center space-x-2 font-inter text-sm text-slate-600">
              <MapPin className="w-4 h-4" />
              <span>{job.localisation}</span>
            </div>
            <div className="flex items-center space-x-2 font-inter text-sm text-slate-600">
              <Calendar className="w-4 h-4" />
              <span>Publié le {format(new Date(job.created_at), 'dd MMMM yyyy', { locale: fr })}</span>
            </div>
          </div>

          {/* Description */}
          <div className="mb-12">
            <h2 className="font-playfair text-2xl font-bold text-deep-navy mb-4">Description</h2>
            <div className="prose prose-lg max-w-none">
              <p className="font-inter text-slate-700 leading-relaxed whitespace-pre-line">
                {job.description}
              </p>
            </div>
          </div>

          {/* Requirements */}
          {job.exigences && job.exigences.length > 0 && (
            <div className="mb-12">
              <h2 className="font-playfair text-2xl font-bold text-deep-navy mb-6">Exigences</h2>
              <ul className="space-y-3">
                {job.exigences.map((exigence, index) => (
                  <li key={index} className="flex items-start space-x-3">
                    <CheckCircle className="w-5 h-5 text-osner-red flex-shrink-0 mt-0.5" />
                    <span className="font-inter text-slate-700">{exigence}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Apply Button */}
          {job.url_candidature && (
            <div className="pt-8 border-t border-slate-200">
              <a
                href={job.url_candidature}
                target="_blank"
                rel="noopener noreferrer"
                data-testid="apply-button"
                className="inline-flex items-center space-x-2 px-8 py-4 bg-osner-red text-white font-inter font-medium rounded-none hover:bg-blue-700 transition-colors"
              >
                <span>Postuler</span>
                <ExternalLink className="w-5 h-5" />
              </a>
            </div>
          )}
        </div>
      </div>

      {/* Related Jobs */}
      {relatedJobs.length > 0 && (
        <section className="bg-slate-50 py-16">
          <div className="max-w-7xl mx-auto px-4 md:px-8">
            <h2 className="font-playfair text-3xl font-bold text-deep-navy mb-8">
              Offres similaires
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {relatedJobs.map((relatedJob) => (
                <JobCard key={relatedJob.id} job={relatedJob} />
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default EmploiDetail;