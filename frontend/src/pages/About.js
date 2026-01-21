import { Calendar, Target, Users, Award, TrendingUp, Heart } from 'lucide-react';

const About = () => {
  const values = [
    {
      icon: Target,
      title: 'Excellence',
      description: 'Nous visons l\'excellence dans chaque service que nous offrons à nos utilisateurs.'
    },
    {
      icon: Heart,
      title: 'Engagement',
      description: 'Nous nous engageons à accompagner chaque candidat vers la réussite professionnelle.'
    },
    {
      icon: Users,
      title: 'Proximité',
      description: 'Nous restons proches de nos utilisateurs avec un support réactif et personnalisé.'
    },
    {
      icon: TrendingUp,
      title: 'Innovation',
      description: 'Nous innovons constamment pour offrir les meilleures solutions du marché.'
    }
  ];

  const stats = [
    { number: '2019', label: 'Année de création' },
    { number: '10K+', label: 'Utilisateurs actifs' },
    { number: '500+', label: 'Entreprises partenaires' },
    { number: '5K+', label: 'Offres publiées' }
  ];

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Hero */}
      <div className="bg-deep-navy text-white py-20">
        <div className="max-w-7xl mx-auto px-4 md:px-8">
          <div className="max-w-3xl">
            <h1 className="font-playfair text-4xl md:text-5xl font-bold mb-6">
              À propos d'Osner-Group
            </h1>
            <p className="font-inter text-lg md:text-xl text-slate-300 leading-relaxed">
              Depuis 2019, nous connectons les talents ivoiriens aux opportunités qui façonnent leur avenir.
            </p>
          </div>
        </div>
      </div>

      {/* Mission */}
      <div className="max-w-7xl mx-auto px-4 md:px-8 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="font-playfair text-3xl font-bold text-deep-navy mb-6">
              Notre Mission
            </h2>
            <div className="space-y-4 font-inter text-slate-700 leading-relaxed">
              <p>
                Osner-Group est né d'une vision simple mais ambitieuse : <strong>démocratiser l'accès à l'emploi et à la formation en Côte d'Ivoire</strong>.
              </p>
              <p>
                Fondée le <strong>12 mars 2019</strong> par Melvin Tayorault, notre plateforme révolutionne la manière dont les candidats trouvent des opportunités professionnelles et développent leurs compétences.
              </p>
              <p>
                Nous croyons que chaque Ivoirien mérite d'avoir accès aux meilleures opportunités, indépendamment de son origine ou de sa localisation. C'est pourquoi nous avons créé une plateforme qui combine :
              </p>
              <ul className="list-disc list-inside space-y-2 ml-4">
                <li>Actualités professionnelles pertinentes</li>
                <li>Formations de qualité adaptées au marché</li>
                <li>Offres d'emploi vérifiées et actualisées quotidiennement</li>
                <li>Matching intelligent CV-Offres avec IA</li>
              </ul>
            </div>
          </div>

          <div className="bg-white p-8 border border-slate-200">
            <div className="flex items-center space-x-4 mb-6">
              <Calendar className="w-12 h-12 text-osner-red" />
              <div>
                <p className="font-inter text-sm text-slate-600">Fondée en</p>
                <p className="font-playfair text-3xl font-bold text-deep-navy">2019</p>
              </div>
            </div>
            <p className="font-inter text-slate-600 mb-6">
              Plus de 6 ans d'expérience au service de l'emploi et de la formation en Côte d'Ivoire.
            </p>
            <div className="space-y-3">
              <div className="flex items-center space-x-2">
                <Award className="w-5 h-5 text-osner-red" />
                <span className="font-inter text-sm text-slate-700">Plateforme certifiée</span>
              </div>
              <div className="flex items-center space-x-2">
                <Users className="w-5 h-5 text-osner-red" />
                <span className="font-inter text-sm text-slate-700">Équipe passionnée et expérimentée</span>
              </div>
              <div className="flex items-center space-x-2">
                <TrendingUp className="w-5 h-5 text-osner-red" />
                <span className="font-inter text-sm text-slate-700">Croissance continue</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4 md:px-8">
          <h2 className="font-playfair text-3xl font-bold text-deep-navy text-center mb-12">
            Osner-Group en chiffres
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, idx) => (
              <div key={idx} className="text-center">
                <p className="font-playfair text-4xl md:text-5xl font-bold text-osner-red mb-2">
                  {stat.number}
                </p>
                <p className="font-inter text-sm text-slate-600">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Values */}
      <div className="max-w-7xl mx-auto px-4 md:px-8 py-16">
        <h2 className="font-playfair text-3xl font-bold text-deep-navy text-center mb-12">
          Nos Valeurs
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {values.map((value, idx) => {
            const Icon = value.icon;
            return (
              <div key={idx} className="bg-white p-6 border border-slate-200 text-center">
                <div className="w-16 h-16 bg-osner-red rounded-full flex items-center justify-center mx-auto mb-4">
                  <Icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="font-playfair text-xl font-bold text-deep-navy mb-3">
                  {value.title}
                </h3>
                <p className="font-inter text-sm text-slate-600">
                  {value.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Team */}
      <div className="bg-deep-navy text-white py-16">
        <div className="max-w-7xl mx-auto px-4 md:px-8 text-center">
          <h2 className="font-playfair text-3xl font-bold mb-6">
            Direction
          </h2>
          <p className="font-inter text-lg text-slate-300 mb-8">
            <strong>Melvin Tayorault</strong>, Manager
          </p>
          <p className="font-inter text-slate-300 max-w-2xl mx-auto">
            Sous sa direction, Osner-Group est devenue une référence en matière de placement professionnel et de formation en Côte d'Ivoire.
          </p>
        </div>
      </div>

      {/* CTA */}
      <div className="max-w-7xl mx-auto px-4 md:px-8 py-16">
        <div className="bg-osner-red text-white p-12 text-center">
          <h2 className="font-playfair text-3xl font-bold mb-4">
            Rejoignez des milliers d'Ivoiriens qui ont trouvé leur voie
          </h2>
          <p className="font-inter text-lg mb-8">
            Inscrivez-vous gratuitement et accédez à des opportunités exclusives
          </p>
          <a
            href="/candidate/auth"
            className="inline-block px-8 py-4 bg-white text-osner-red font-inter font-medium hover:bg-slate-100 transition-colors"
          >
            Créer mon compte gratuitement
          </a>
        </div>
      </div>
    </div>
  );
};

export default About;