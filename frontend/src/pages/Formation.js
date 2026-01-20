import { useEffect, useState } from 'react';
import axios from 'axios';
import { FormationCard } from '@/components/FormationCard';
import { Search, Filter } from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const niveaux = ['Tous', 'Débutant', 'Intermédiaire', 'Avancé'];

const Formation = () => {
  const [formations, setFormations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedNiveau, setSelectedNiveau] = useState('Tous');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadFormations();
  }, [selectedNiveau]);

  const loadFormations = async () => {
    setLoading(true);
    try {
      const params = selectedNiveau !== 'Tous' ? `?niveau=${selectedNiveau}` : '';
      const response = await axios.get(`${API}/formations${params}`);
      setFormations(response.data);
    } catch (error) {
      console.error('Erreur lors du chargement des formations:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredFormations = formations.filter((formation) =>
    searchQuery
      ? formation.titre.toLowerCase().includes(searchQuery.toLowerCase()) ||
        formation.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        formation.thematique.toLowerCase().includes(searchQuery.toLowerCase())
      : true
  );

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-deep-navy text-white py-16">
        <div className="max-w-7xl mx-auto px-4 md:px-8">
          <h1 className="font-playfair text-4xl md:text-5xl font-bold mb-4">Formation</h1>
          <p className="font-inter text-lg text-slate-300">
            Développez vos compétences avec nos parcours de formation
          </p>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white border-b border-slate-200 sticky top-20 z-40">
        <div className="max-w-7xl mx-auto px-4 md:px-8 py-6">
          <div className="flex flex-col md:flex-row gap-4">
            {/* Search */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input
                type="text"
                data-testid="formation-search-input"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Rechercher une formation..."
                className="w-full pl-10 pr-4 py-3 border border-slate-300 rounded-none font-inter text-sm focus:outline-none focus:border-electric-blue transition-colors"
              />
            </div>

            {/* Level Filter */}
            <div className="md:w-64">
              <Select value={selectedNiveau} onValueChange={setSelectedNiveau}>
                <SelectTrigger data-testid="niveau-filter" className="w-full">
                  <div className="flex items-center space-x-2">
                    <Filter className="w-4 h-4" />
                    <SelectValue placeholder="Niveau" />
                  </div>
                </SelectTrigger>
                <SelectContent>
                  {niveaux.map((niveau) => (
                    <SelectItem key={niveau} value={niveau}>
                      {niveau}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
      </div>

      {/* Formations Grid */}
      <div className="max-w-7xl mx-auto px-4 md:px-8 py-12">
        {loading ? (
          <div className="text-center py-16">
            <div className="w-16 h-16 border-4 border-electric-blue border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="font-inter text-slate-600">Chargement des formations...</p>
          </div>
        ) : filteredFormations.length === 0 ? (
          <div className="text-center py-16">
            <p className="font-inter text-slate-600">Aucune formation trouvée</p>
          </div>
        ) : (
          <>
            <div className="mb-6">
              <p className="font-inter text-sm text-slate-600">
                {filteredFormations.length} formation{filteredFormations.length > 1 ? 's' : ''} trouvée{filteredFormations.length > 1 ? 's' : ''}
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredFormations.map((formation) => (
                <FormationCard key={formation.id} formation={formation} />
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Formation;