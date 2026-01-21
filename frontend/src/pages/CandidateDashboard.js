import { Link } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { FileText, Coins, Briefcase, TrendingUp, Upload, CreditCard } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { NotificationCenter } from '@/components/NotificationCenter';

const CandidateDashboard = () => {
  const { user } = useAuth();

  const stats = [
    {
      icon: Coins,
      label: 'Crédits disponibles',
      value: user?.credits || 0,
      color: 'text-amber-600',
      bgColor: 'bg-amber-50'
    },
    {
      icon: FileText,
      label: 'CV Uploadé',
      value: 'Oui',
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    },
    {
      icon: Briefcase,
      label: 'Offres matchées',
      value: '-',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    }
  ];

  const quickActions = [
    {
      title: 'Uploader mon CV',
      description: 'Analysez votre CV et obtenez des suggestions d\'amélioration',
      icon: Upload,
      link: '/candidate/cv-upload',
      color: 'bg-osner-red'
    },
    {
      title: 'Voir les correspondances',
      description: 'Découvrez les offres qui correspondent à votre profil',
      icon: TrendingUp,
      link: '/candidate/matching',
      color: 'bg-emerald-600'
    },
    {
      title: 'Recharger des crédits',
      description: 'Achetez des crédits pour plus d\'analyses et de matchings',
      icon: CreditCard,
      link: '/candidate/payment',
      color: 'bg-amber-600'
    }
  ];

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-deep-navy text-white py-12">
        <div className="max-w-7xl mx-auto px-4 md:px-8">
          <h1 className="font-playfair text-4xl font-bold mb-2">
            Bonjour, {user?.prenom} !
          </h1>
          <p className="font-inter text-slate-300">
            Bienvenue dans votre espace candidat
          </p>
        </div>
      </div>

      {/* Stats */}
      <div className="max-w-7xl mx-auto px-4 md:px-8 -mt-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div key={index} className="bg-white p-6 border border-slate-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-inter text-sm text-slate-600 mb-1">{stat.label}</p>
                    <p className="font-playfair text-3xl font-bold text-deep-navy">
                      {stat.value}
                    </p>
                  </div>
                  <div className={`w-12 h-12 ${stat.bgColor} rounded-none flex items-center justify-center`}>
                    <Icon className={`w-6 h-6 ${stat.color}`} />
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Quick Actions */}
        <div className="mb-12">
          <h2 className="font-playfair text-2xl font-bold text-deep-navy mb-6">
            Actions rapides
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {quickActions.map((action, index) => {
              const Icon = action.icon;
              return (
                <Link
                  key={index}
                  to={action.link}
                  data-testid={`quick-action-${index}`}
                  className="group bg-white p-6 border border-slate-200 transition-all hover:shadow-lg hover:border-osner-red"
                >
                  <div className={`w-12 h-12 ${action.color} rounded-none flex items-center justify-center mb-4`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="font-playfair text-xl font-bold text-deep-navy mb-2 group-hover:text-osner-red transition-colors">
                    {action.title}
                  </h3>
                  <p className="font-inter text-sm text-slate-600">
                    {action.description}
                  </p>
                </Link>
              );
            })}
          </div>
        </div>

        {/* Info Box */}
        {user?.credits === 0 && (
          <div className="bg-amber-50 border border-amber-200 p-6 mb-12">
            <div className="flex items-start space-x-4">
              <Coins className="w-6 h-6 text-amber-600 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-playfair text-lg font-bold text-amber-900 mb-2">
                  Vous n'avez pas de crédits
                </h3>
                <p className="font-inter text-sm text-amber-800 mb-4">
                  Achetez des crédits pour analyser votre CV et découvrir les offres qui vous correspondent.
                </p>
                <Button asChild className="bg-amber-600 hover:bg-amber-700">
                  <Link to="/candidate/payment" data-testid="buy-credits-button">
                    Acheter des crédits
                  </Link>
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CandidateDashboard;