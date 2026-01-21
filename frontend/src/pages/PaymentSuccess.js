import { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { CheckCircle, Coins, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/payments`;

const PaymentSuccess = () => {
  const [searchParams] = useSearchParams();
  const { token, refreshUser } = useAuth();
  const sessionId = searchParams.get('session_id');
  const [status, setStatus] = useState('checking');
  const [credits, setCredits] = useState(0);
  const [attempts, setAttempts] = useState(0);
  const maxAttempts = 5;

  useEffect(() => {
    if (sessionId) {
      checkPaymentStatus();
    }
  }, [sessionId, attempts]);

  const checkPaymentStatus = async () => {
    try {
      const response = await axios.get(`${API}/checkout/status/${sessionId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (response.data.payment_status === 'paid') {
        setStatus('success');
        setCredits(response.data.credits_added);
        await refreshUser();
      } else if (response.data.status === 'expired') {
        setStatus('expired');
      } else if (attempts < maxAttempts) {
        // Continue polling
        setTimeout(() => setAttempts(attempts + 1), 2000);
      } else {
        setStatus('timeout');
      }
    } catch (error) {
      console.error('Erreur lors de la vérification du paiement:', error);
      setStatus('error');
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center py-12 px-4">
      <div className="max-w-md w-full">
        {status === 'checking' && (
          <div className="bg-white p-12 border border-slate-200 text-center">
            <div className="w-16 h-16 border-4 border-osner-red border-t-transparent rounded-full animate-spin mx-auto mb-6"></div>
            <h2 className="font-playfair text-2xl font-bold text-deep-navy mb-2">
              Vérification du paiement
            </h2>
            <p className="font-inter text-slate-600">
              Veuillez patienter quelques instants...
            </p>
          </div>
        )}

        {status === 'success' && (
          <div className="bg-white p-12 border border-slate-200 text-center">
            <div className="w-16 h-16 bg-green-50 rounded-full flex items-center justify-center mx-auto mb-6">
              <CheckCircle className="w-10 h-10 text-green-600" />
            </div>
            <h2 className="font-playfair text-2xl font-bold text-deep-navy mb-2">
              Paiement réussi !
            </h2>
            <p className="font-inter text-slate-600 mb-6">
              Votre compte a été crédité de {credits} crédit{credits > 1 ? 's' : ''}.
            </p>

            <div className="bg-green-50 border border-green-200 p-4 mb-8">
              <div className="flex items-center justify-center space-x-2">
                <Coins className="w-5 h-5 text-green-700" />
                <span className="font-inter text-sm text-green-800">
                  Vous pouvez maintenant utiliser vos crédits pour analyser votre CV et matcher avec des offres
                </span>
              </div>
            </div>

            <div className="space-y-3">
              <Button asChild className="w-full bg-osner-red hover:bg-blue-700">
                <Link to="/candidate/dashboard" data-testid="go-to-dashboard">
                  Retour au tableau de bord
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Link>
              </Button>
              <Button asChild variant="outline" className="w-full">
                <Link to="/candidate/cv-upload">
                  Uploader mon CV
                </Link>
              </Button>
            </div>
          </div>
        )}

        {(status === 'expired' || status === 'timeout' || status === 'error') && (
          <div className="bg-white p-12 border border-slate-200 text-center">
            <div className="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-6">
              <span className="text-3xl">❌</span>
            </div>
            <h2 className="font-playfair text-2xl font-bold text-deep-navy mb-2">
              {status === 'expired' ? 'Session expirée' : 'Erreur'}
            </h2>
            <p className="font-inter text-slate-600 mb-8">
              {status === 'expired'
                ? 'Votre session de paiement a expiré. Veuillez réessayer.'
                : 'Une erreur est survenue lors de la vérification du paiement. Si vous avez été débité, vos crédits seront ajoutés sous peu.'}
            </p>
            <Button asChild className="w-full bg-osner-red hover:bg-blue-700">
              <Link to="/candidate/payment">
                Retour aux paiements
              </Link>
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default PaymentSuccess;