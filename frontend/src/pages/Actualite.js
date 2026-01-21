import { useEffect, useState } from 'react';
import axios from 'axios';
import { ArticleCard } from '@/components/ArticleCard';
import { Search, Filter } from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const categories = [
  'Tous',
  'Société',
  'Économie',
  'Éducation',
  'Technologie',
  'Emploi',
  'Analyses / Opinions',
];

const Actualite = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('Tous');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadArticles();
  }, [selectedCategory]);

  const loadArticles = async () => {
    setLoading(true);
    try {
      const params = selectedCategory !== 'Tous' ? `?categorie=${selectedCategory}` : '';
      const response = await axios.get(`${API}/articles${params}`);
      setArticles(response.data);
    } catch (error) {
      console.error('Erreur lors du chargement des articles:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredArticles = articles.filter((article) =>
    searchQuery
      ? article.titre.toLowerCase().includes(searchQuery.toLowerCase()) ||
        article.extrait.toLowerCase().includes(searchQuery.toLowerCase())
      : true
  );

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-deep-navy text-white py-16">
        <div className="max-w-7xl mx-auto px-4 md:px-8">
          <h1 className="font-playfair text-4xl md:text-5xl font-bold mb-4">Actualité</h1>
          <p className="font-inter text-lg text-slate-300">
            Restez informé des dernières nouvelles et analyses
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
                data-testid="article-search-input"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Rechercher un article..."
                className="w-full pl-10 pr-4 py-3 border border-slate-300 rounded-none font-inter text-sm focus:outline-none focus:border-osner-red transition-colors"
              />
            </div>

            {/* Category Filter */}
            <div className="md:w-64">
              <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                <SelectTrigger data-testid="category-filter" className="w-full">
                  <div className="flex items-center space-x-2">
                    <Filter className="w-4 h-4" />
                    <SelectValue placeholder="Catégorie" />
                  </div>
                </SelectTrigger>
                <SelectContent>
                  {categories.map((category) => (
                    <SelectItem key={category} value={category}>
                      {category}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
      </div>

      {/* Articles Grid */}
      <div className="max-w-7xl mx-auto px-4 md:px-8 py-12">
        {loading ? (
          <div className="text-center py-16">
            <div className="w-16 h-16 border-4 border-osner-red border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="font-inter text-slate-600">Chargement des articles...</p>
          </div>
        ) : filteredArticles.length === 0 ? (
          <div className="text-center py-16">
            <p className="font-inter text-slate-600">Aucun article trouvé</p>
          </div>
        ) : (
          <>
            <div className="mb-6">
              <p className="font-inter text-sm text-slate-600">
                {filteredArticles.length} article{filteredArticles.length > 1 ? 's' : ''} trouvé{filteredArticles.length > 1 ? 's' : ''}
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredArticles.map((article) => (
                <ArticleCard key={article.id} article={article} />
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Actualite;