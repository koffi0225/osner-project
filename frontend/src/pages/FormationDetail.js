import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { ArrowLeft, GraduationCap, Clock, BookOpen, Target, Download } from 'lucide-react';
import { FormationCard } from '@/components/FormationCard';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const FormationDetail = () => {
  const { slug } = useParams();
  const [formation, setFormation] = useState(null);
  const [relatedFormations, setRelatedFormations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFormation();
  }, [slug]);

  const loadFormation = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/formations/${slug}`);
      setFormation(response.data);

      // Load related formations from the same thematique
      const relatedRes = await axios.get(`${API}/formations?thematique=${response.data.thematique}&limit=3`);
      setRelatedFormations(relatedRes.data.filter(f => f.slug !== slug).slice(0, 3));
    } catch (error) {
      console.error('Erreur lors du chargement de la formation:', error);
    } finally {
      setLoading(false);
    }
  };

  const getNiveauColor = (niveau) => {
    const colors = {
      'Débutant': 'bg-green-100 text-green-700',
      'Intermédiaire': 'bg-blue-100 text-blue-700',
      'Avancé': 'bg-purple-100 text-purple-700',
    };
    return colors[niveau] || 'bg-slate-100 text-slate-700';
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

  if (!formation) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="font-inter text-slate-600 mb-4">Formation non trouvée</p>
          <Link to="/formation" className="text-osner-red hover:underline">
            Retour aux formations
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
            to="/formation"
            data-testid="back-to-formations"
            className="inline-flex items-center space-x-2 text-slate-600 hover:text-osner-red transition-colors font-inter text-sm"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Retour aux formations</span>
          </Link>
        </div>
      </div>

      {/* Formation Header */}
      <div className="bg-white py-12">
        <div className="max-w-4xl mx-auto px-4 md:px-8">
          {/* Niveau and Thematique */}
          <div className="flex flex-wrap items-center gap-3 mb-6">
            <span className={`px-3 py-1 font-mono text-xs font-medium ${getNiveauColor(formation.niveau)}`}>
              {formation.niveau}
            </span>
            <div className="flex items-center space-x-2">
              <GraduationCap className="w-4 h-4 text-osner-red" />
              <span className="font-mono text-xs text-slate-600">{formation.thematique}</span>
            </div>
          </div>

          {/* Title */}
          <h1 className="font-playfair text-4xl md:text-5xl font-bold text-deep-navy mb-6 leading-tight">
            {formation.titre}
          </h1>

          {/* Description */}
          <p className="font-inter text-lg text-slate-600 leading-relaxed mb-8">
            {formation.description}
          </p>

          {/* Meta */}
          <div className="flex items-center space-x-6 mb-8 pb-8 border-b border-slate-200">
            <div className="flex items-center space-x-2 font-inter text-sm text-slate-600">
              <Clock className="w-4 h-4" />
              <span>{formation.duree}</span>
            </div>
          </div>

          {/* Featured Image */}
          <div className="mb-12">
            <img
              src={formation.image_url}
              alt={formation.titre}
              className="w-full aspect-[16/9] object-cover"
            />
          </div>
        </div>
      </div>

      {/* Objectives */}
      {formation.objectifs && formation.objectifs.length > 0 && (
        <div className="bg-slate-50 py-12">
          <div className="max-w-4xl mx-auto px-4 md:px-8">
            <div className="flex items-center space-x-3 mb-6">
              <Target className="w-6 h-6 text-osner-red" />
              <h2 className="font-playfair text-2xl font-bold text-deep-navy">Objectifs</h2>
            </div>
            <ul className="space-y-3">
              {formation.objectifs.map((objectif, index) => (
                <li key={index} className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-osner-red text-white rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="font-mono text-xs font-bold">{index + 1}</span>
                  </div>
                  <span className="font-inter text-slate-700">{objectif}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Content */}
      <div className="bg-white py-12">
        <div className="max-w-4xl mx-auto px-4 md:px-8">
          <div className="flex items-center space-x-3 mb-6">
            <BookOpen className="w-6 h-6 text-osner-red" />
            <h2 className="font-playfair text-2xl font-bold text-deep-navy">Contenu de la formation</h2>
          </div>
          <div className="prose prose-lg max-w-none">
            <div className="font-inter text-slate-700 leading-relaxed whitespace-pre-line">
              {formation.contenu}
            </div>
          </div>
        </div>
      </div>

      {/* Resources */}
      {formation.ressources && formation.ressources.length > 0 && (
        <div className="bg-slate-50 py-12">
          <div className="max-w-4xl mx-auto px-4 md:px-8">
            <div className="flex items-center space-x-3 mb-6">
              <Download className="w-6 h-6 text-osner-red" />
              <h2 className="font-playfair text-2xl font-bold text-deep-navy">Ressources</h2>
            </div>
            <ul className="space-y-2">
              {formation.ressources.map((ressource, index) => (
                <li key={index} className="flex items-center space-x-3 p-4 bg-white border border-slate-200">
                  <Download className="w-4 h-4 text-slate-400" />
                  <span className="font-inter text-sm text-slate-700">{ressource}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Related Formations */}
      {relatedFormations.length > 0 && (
        <section className="bg-white py-16">
          <div className="max-w-7xl mx-auto px-4 md:px-8">
            <h2 className="font-playfair text-3xl font-bold text-deep-navy mb-8">
              Formations similaires
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {relatedFormations.map((relatedFormation) => (
                <FormationCard key={relatedFormation.id} formation={relatedFormation} />
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default FormationDetail;