import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { RefreshCw, Database, CheckCircle, AlertCircle } from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/aggregation`;

export const AggregationManager = () => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingStatus, setLoadingStatus] = useState(false);

  const loadStatus = async () => {
    setLoadingStatus(true);
    try {
      const response = await axios.get(`${API}/status`);
      setStatus(response.data);
    } catch (error) {
      toast.error('Erreur lors du chargement du statut');
    } finally {
      setLoadingStatus(false);
    }
  };

  const runAggregation = async (type = 'all') => {
    setLoading(true);
    try {
      const endpoint = type === 'all' ? '/update-all' : `/update-${type}`;
      const response = await axios.post(`${API}${endpoint}`);
      
      toast.success(`Mise à jour réussie : ${response.data.message}`);
      await loadStatus();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erreur lors de l\'agrégation');
    } finally {
      setLoading(false);
    }
  };

  useState(() => {
    loadStatus();
  }, []);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="font-playfair text-2xl font-bold text-deep-navy">Gestion des Contenus Agrégés</h2>
        <Button
          onClick={loadStatus}
          disabled={loadingStatus}
          variant="outline"
          data-testid="refresh-status-button"
        >
          <RefreshCw className={`w-4 h-4 mr-2 ${loadingStatus ? 'animate-spin' : ''}`} />
          Actualiser
        </Button>
      </div>

      {/* Status Cards */}
      {status && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div>
                <p className="font-inter text-sm text-slate-600 mb-1">Offres d'Emploi</p>
                <p className="font-playfair text-3xl font-bold text-deep-navy">
                  {status.counts.jobs}
                </p>
              </div>
              <Database className="w-10 h-10 text-osner-red" />
            </div>
            {status.latest.job && (
              <p className="font-inter text-xs text-slate-500">
                Dernière màj : {new Date(status.latest.job).toLocaleString('fr-FR')}
              </p>
            )}
          </div>

          <div className="bg-white p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div>
                <p className="font-inter text-sm text-slate-600 mb-1">Actualités</p>
                <p className="font-playfair text-3xl font-bold text-deep-navy">
                  {status.counts.news}
                </p>
              </div>
              <Database className="w-10 h-10 text-osner-red" />
            </div>
            {status.latest.news && (
              <p className="font-inter text-xs text-slate-500">
                Dernière màj : {new Date(status.latest.news).toLocaleString('fr-FR')}
              </p>
            )}
          </div>

          <div className="bg-white p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div>
                <p className="font-inter text-sm text-slate-600 mb-1">Formations</p>
                <p className="font-playfair text-3xl font-bold text-deep-navy">
                  {status.counts.trainings}
                </p>
              </div>
              <Database className="w-10 h-10 text-osner-red" />
            </div>
            {status.latest.training && (
              <p className="font-inter text-xs text-slate-500">
                Dernière màj : {new Date(status.latest.training).toLocaleString('fr-FR')}
              </p>
            )}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="bg-white p-8 border border-slate-200 mb-8">
        <h3 className="font-playfair text-xl font-bold text-deep-navy mb-4">
          Mise à Jour Manuelle
        </h3>
        <p className="font-inter text-sm text-slate-600 mb-6">
          Déclenchez une mise à jour manuelle du contenu agrégé. La mise à jour automatique quotidienne s'exécute tous les jours à 2h du matin.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Button
            onClick={() => runAggregation('all')}
            disabled={loading}
            data-testid="aggregate-all-button"
            className="w-full bg-osner-red hover:bg-red-700"
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Tout Mettre à Jour
          </Button>

          <Button
            onClick={() => runAggregation('jobs')}
            disabled={loading}
            variant="outline"
            data-testid="aggregate-jobs-button"
            className="w-full"
          >
            Emplois
          </Button>

          <Button
            onClick={() => runAggregation('news')}
            disabled={loading}
            variant="outline"
            data-testid="aggregate-news-button"
            className="w-full"
          >
            Actualités
          </Button>

          <Button
            onClick={() => runAggregation('trainings')}
            disabled={loading}
            variant="outline"
            data-testid="aggregate-trainings-button"
            className="w-full"
          >
            Formations
          </Button>
        </div>
      </div>

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 p-6">
        <div className="flex items-start space-x-4">
          <CheckCircle className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
          <div>
            <h3 className="font-playfair text-lg font-bold text-blue-900 mb-2">
              Système d'Agrégation Automatique
            </h3>
            <ul className="space-y-2 font-inter text-sm text-blue-800">
              <li>✅ Mise à jour automatique quotidienne à 2h du matin</li>
              <li>✅ Agrégation depuis plusieurs sources de Côte d'Ivoire</li>
              <li>✅ Déduplication automatique des contenus</li>
              <li>✅ Actualités : Politique, Sport, Économie, Société, Technologie</li>
              <li>✅ Emplois : Abidjan et toute la Côte d'Ivoire</li>
              <li>✅ Formations : Téléconseil, Développement, Santé, Marketing, Comptabilité</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
