import { useEffect, useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { Link } from 'react-router-dom';
import { TrendingUp, Briefcase, MapPin, Building, ChevronRight } from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/candidate`;

const JobMatching = () => {
  const { token } = useAuth();
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMatches();
  }, []);

  const loadMatches = async () => {
    try {
      const response = await axios.get(`${API}/jobs/matching`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMatches(response.data);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erreur lors du chargement des correspondances');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-50';
    if (score >= 60) return 'text-blue-600 bg-blue-50';
    if (score >= 40) return 'text-amber-600 bg-amber-50';
    return 'text-red-600 bg-red-50';
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-deep-navy text-white py-12">
        <div className="max-w-7xl mx-auto px-4 md:px-8">
          <div className="flex items-center space-x-3 mb-2">
            <TrendingUp className="w-8 h-8" />
            <h1 className="font-playfair text-4xl font-bold">Offres matchées</h1>
          </div>
          <p className="font-inter text-slate-300">
            Découvrez les offres d'emploi qui correspondent le mieux à votre profil
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 md:px-8 py-12">
        {loading ? (
          <div className="text-center py-16">
            <div className="w-16 h-16 border-4 border-electric-blue border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="font-inter text-slate-600">Chargement...</p>
          </div>
        ) : matches.length === 0 ? (
          <div className="text-center py-16 bg-white border border-slate-200 p-12">
            <Briefcase className="w-16 h-16 text-slate-400 mx-auto mb-4" />
            <h3 className="font-playfair text-2xl font-bold text-deep-navy mb-2">
              Aucune correspondance pour le moment
            </h3>
            <p className="font-inter text-slate-600 mb-6">
              Commencez par uploader votre CV et analysez des offres pour voir vos correspondances.
            </p>
            <Link
              to="/candidate/cv-upload"
              className="inline-flex items-center px-6 py-3 bg-electric-blue text-white font-inter font-medium hover:bg-blue-700 transition-colors"
            >
              Uploader mon CV
              <ChevronRight className="w-5 h-5 ml-2" />
            </Link>
          </div>
        ) : (
          <div className="space-y-6">
            {matches.map((match) => (
              <Link
                key={match.job_id}
                to={`/emploi/${match.job_id}`}
                data-testid={`match-card-${match.job_id}`}
                className="group block bg-white border border-slate-200 p-6 transition-all hover:shadow-lg hover:border-electric-blue"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="font-playfair text-xl font-bold text-deep-navy mb-2 group-hover:text-electric-blue transition-colors">
                      {match.job_title}
                    </h3>
                    <div className="flex items-center space-x-2 mb-3">
                      <Building className="w-4 h-4 text-slate-400" />
                      <span className="font-inter text-sm text-slate-600">{match.entreprise}</span>
                    </div>
                  </div>
                  <div className={`px-4 py-2 rounded-none font-mono text-sm font-bold ${getScoreColor(match.score)}`}>
                    {match.score}%
                  </div>
                </div>

                {match.resume_analyse && (
                  <p className="font-inter text-sm text-slate-600 mb-4 line-clamp-2">
                    {match.resume_analyse}
                  </p>
                )}

                <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                  <span className="font-inter text-xs text-slate-500">
                    Compatibilité : {match.score >= 80 ? 'Excellente' : match.score >= 60 ? 'Bonne' : match.score >= 40 ? 'Moyenne' : 'Faible'}
                  </span>
                  <ChevronRight className="w-5 h-5 text-electric-blue transition-transform group-hover:translate-x-1" />
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default JobMatching;