import { useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { Coins, Check } from 'lucide-react';
import { Button } from '@/components/ui/button';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/payments`;

const Payment = () => {
  const { token, user } = useAuth();
  const [loading, setLoading] = useState(false);

  const packages = [
    {
      id: 'cv_analysis',
      name: 'Analyse de CV',
      price: 5,
      credits: 1,
      features: [
        '1 analyse de CV complète',
        'Suggestions d\'amélioration',
        'Matching avec 1 offre',
        'Valide 30 jours'
      ]
    },
    {
      id: 'matching_premium',
      name: 'Matching Premium',
      price: 10,
      credits: 5,
      popular: true,
      features: [
        '5 analyses de correspondance',
        'Scores de compatibilité',
        'Suggestions personnalisées',
        'Valide 60 jours'
      ]
    },
    {
      id: 'monthly_subscription',
      name: 'Abonnement Mensuel',
      price: 20,
      credits: 20,
      features: [
        '20 analyses illimitées',
        'Toutes les fonctionnalités',
        'Support prioritaire',
        'Renouvelable chaque mois'
      ]
    }
  ];

  const handlePurchase = async (packageId) => {
    setLoading(true);
    try {
      const originUrl = window.location.origin;
      const response = await axios.post(
        `${API}/checkout/session`,
        { package_id: packageId, origin_url: originUrl },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      // Redirect to Stripe Checkout
      window.location.href = response.data.url;
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erreur lors de la création de la session de paiement');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-deep-navy text-white py-12">
        <div className="max-w-7xl mx-auto px-4 md:px-8">
          <div className="flex items-center space-x-3 mb-2">
            <Coins className="w-8 h-8" />
            <h1 className="font-playfair text-4xl font-bold">Recharger des crédits</h1>
          </div>
          <p className="font-inter text-slate-300">
            Choisissez le package qui vous convient
          </p>
        </div>
      </div>

      {/* Current Credits */}
      <div className="max-w-7xl mx-auto px-4 md:px-8 py-8">
        <div className="bg-white p-6 border border-slate-200 mb-12">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-inter text-sm text-slate-600 mb-1">Crédits actuels</p>
              <p className="font-playfair text-3xl font-bold text-deep-navy">
                {user?.credits || 0}
              </p>
            </div>
            <Coins className="w-12 h-12 text-amber-600" />
          </div>
        </div>

        {/* Packages */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {packages.map((pkg) => (
            <div
              key={pkg.id}
              className={`bg-white border-2 p-8 relative ${
                pkg.popular ? 'border-osner-red' : 'border-slate-200'
              }`}
            >
              {pkg.popular && (
                <div className="absolute top-0 right-0 bg-osner-red text-white px-3 py-1 font-inter text-xs font-medium">
                  POPULAIRE
                </div>
              )}

              <div className="text-center mb-6">
                <h3 className="font-playfair text-2xl font-bold text-deep-navy mb-2">
                  {pkg.name}
                </h3>
                <div className="flex items-baseline justify-center mb-2">
                  <span className="font-playfair text-4xl font-bold text-deep-navy">
                    {pkg.price}€
                  </span>
                </div>
                <p className="font-inter text-sm text-slate-600">
                  {pkg.credits} crédit{pkg.credits > 1 ? 's' : ''}
                </p>
              </div>

              <ul className="space-y-3 mb-8">
                {pkg.features.map((feature, idx) => (
                  <li key={idx} className="flex items-start space-x-2">
                    <Check className="w-5 h-5 text-osner-red flex-shrink-0 mt-0.5" />
                    <span className="font-inter text-sm text-slate-600">{feature}</span>
                  </li>
                ))}
              </ul>

              <Button
                onClick={() => handlePurchase(pkg.id)}
                data-testid={`purchase-${pkg.id}`}
                disabled={loading}
                className={`w-full ${
                  pkg.popular
                    ? 'bg-osner-red hover:bg-blue-700'
                    : 'bg-deep-navy hover:bg-slate-800'
                }`}
              >
                {loading ? 'Traitement...' : 'Acheter maintenant'}
              </Button>
            </div>
          ))}
        </div>

        {/* Info */}
        <div className="mt-12 bg-blue-50 border border-blue-200 p-6">
          <h3 className="font-playfair text-lg font-bold text-blue-900 mb-2">
            Comment ça marche ?
          </h3>
          <ul className="space-y-2 font-inter text-sm text-blue-800">
            <li>• Chaque analyse de CV ou matching avec une offre coûte 1 crédit</li>
            <li>• Les crédits n'expirent pas tant que vous les utilisez régulièrement</li>
            <li>• Paiement sécurisé par Stripe</li>
            <li>• Satisfaction garantie ou remboursé</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Payment;