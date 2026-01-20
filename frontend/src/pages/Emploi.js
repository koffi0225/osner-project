import { useEffect, useState } from 'react';
import axios from 'axios';
import { JobCard } from '@/components/JobCard';
import { Search, Filter } from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const types = ['Tous', 'Emploi', 'Stage', 'Concours'];

const Emploi = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedType, setSelectedType] = useState('Tous');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadJobs();
  }, [selectedType]);

  const loadJobs = async () => {
    setLoading(true);
    try {
      const params = selectedType !== 'Tous' ? `?type=${selectedType}` : '';
      const response = await axios.get(`${API}/emplois${params}`);
      setJobs(response.data);
    } catch (error) {
      console.error('Erreur lors du chargement des offres:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredJobs = jobs.filter((job) =>
    searchQuery
      ? job.titre.toLowerCase().includes(searchQuery.toLowerCase()) ||
        job.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        job.entreprise.toLowerCase().includes(searchQuery.toLowerCase()) ||
        job.secteur.toLowerCase().includes(searchQuery.toLowerCase()) ||
        job.localisation.toLowerCase().includes(searchQuery.toLowerCase())
      : true
  );

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-deep-navy text-white py-16">
        <div className="max-w-7xl mx-auto px-4 md:px-8">
          <h1 className="font-playfair text-4xl md:text-5xl font-bold mb-4">Emploi & Carrière</h1>
          <p className="font-inter text-lg text-slate-300">
            Découvrez les opportunités professionnelles qui vous correspondent
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
                data-testid="job-search-input"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Rechercher une offre (titre, entreprise, secteur, localisation)..."
                className="w-full pl-10 pr-4 py-3 border border-slate-300 rounded-none font-inter text-sm focus:outline-none focus:border-electric-blue transition-colors"
              />
            </div>

            {/* Type Filter */}
            <div className="md:w-64">
              <Select value={selectedType} onValueChange={setSelectedType}>
                <SelectTrigger data-testid="type-filter" className="w-full">
                  <div className="flex items-center space-x-2">
                    <Filter className="w-4 h-4" />
                    <SelectValue placeholder="Type" />
                  </div>
                </SelectTrigger>
                <SelectContent>
                  {types.map((type) => (
                    <SelectItem key={type} value={type}>
                      {type}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
      </div>

      {/* Jobs Grid */}
      <div className="max-w-7xl mx-auto px-4 md:px-8 py-12">
        {loading ? (
          <div className="text-center py-16">
            <div className="w-16 h-16 border-4 border-electric-blue border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="font-inter text-slate-600">Chargement des offres...</p>
          </div>
        ) : filteredJobs.length === 0 ? (
          <div className="text-center py-16">
            <p className="font-inter text-slate-600">Aucune offre trouvée</p>
          </div>
        ) : (
          <>
            <div className="mb-6">
              <p className="font-inter text-sm text-slate-600">
                {filteredJobs.length} offre{filteredJobs.length > 1 ? 's' : ''} trouvée{filteredJobs.length > 1 ? 's' : ''}
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {filteredJobs.map((job) => (
                <JobCard key={job.id} job={job} />
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Emploi;