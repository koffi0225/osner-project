import { useEffect, useState } from 'react';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { Plus, Edit, Trash2 } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const categories = ['Société', 'Économie', 'Éducation', 'Technologie', 'Emploi', 'Analyses / Opinions'];

export const ArticlesAdmin = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingArticle, setEditingArticle] = useState(null);
  const [formData, setFormData] = useState({
    titre: '',
    slug: '',
    categorie: '',
    tags: '',
    auteur: '',
    image_url: '',
    contenu: '',
    extrait: '',
    temps_lecture: 5,
    vedette: false,
  });

  useEffect(() => {
    loadArticles();
  }, []);

  const loadArticles = async () => {
    try {
      const response = await axios.get(`${API}/articles?limit=100`);
      setArticles(response.data);
    } catch (error) {
      toast.error('Erreur lors du chargement des articles');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const payload = {
      ...formData,
      tags: formData.tags ? formData.tags.split(',').map(t => t.trim()) : [],
      temps_lecture: parseInt(formData.temps_lecture),
    };

    try {
      if (editingArticle) {
        await axios.put(`${API}/articles/${editingArticle.id}`, payload);
        toast.success('Article mis à jour');
      } else {
        await axios.post(`${API}/articles`, payload);
        toast.success('Article créé');
      }
      setDialogOpen(false);
      resetForm();
      loadArticles();
    } catch (error) {
      toast.error('Erreur lors de la sauvegarde');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cet article ?')) return;
    
    try {
      await axios.delete(`${API}/articles/${id}`);
      toast.success('Article supprimé');
      loadArticles();
    } catch (error) {
      toast.error('Erreur lors de la suppression');
    }
  };

  const handleEdit = (article) => {
    setEditingArticle(article);
    setFormData({
      titre: article.titre,
      slug: article.slug,
      categorie: article.categorie,
      tags: article.tags.join(', '),
      auteur: article.auteur,
      image_url: article.image_url,
      contenu: article.contenu,
      extrait: article.extrait,
      temps_lecture: article.temps_lecture,
      vedette: article.vedette,
    });
    setDialogOpen(true);
  };

  const resetForm = () => {
    setEditingArticle(null);
    setFormData({
      titre: '',
      slug: '',
      categorie: '',
      tags: '',
      auteur: '',
      image_url: '',
      contenu: '',
      extrait: '',
      temps_lecture: 5,
      vedette: false,
    });
  };

  if (loading) {
    return <div className="text-center py-8">Chargement...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="font-playfair text-2xl font-bold text-deep-navy">Gestion des articles</h2>
        <Dialog open={dialogOpen} onOpenChange={(open) => {
          setDialogOpen(open);
          if (!open) resetForm();
        }}>
          <DialogTrigger asChild>
            <Button data-testid="add-article-button" className="bg-osner-red hover:bg-blue-700">
              <Plus className="w-4 h-4 mr-2" />
              Nouvel article
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>{editingArticle ? 'Éditer' : 'Nouvel'} article</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="titre">Titre*</Label>
                  <Input
                    id="titre"
                    data-testid="article-titre-input"
                    value={formData.titre}
                    onChange={(e) => setFormData({ ...formData, titre: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="slug">Slug*</Label>
                  <Input
                    id="slug"
                    data-testid="article-slug-input"
                    value={formData.slug}
                    onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="categorie">Catégorie*</Label>
                  <Select value={formData.categorie} onValueChange={(value) => setFormData({ ...formData, categorie: value })}>
                    <SelectTrigger data-testid="article-categorie-select">
                      <SelectValue placeholder="Sélectionnez" />
                    </SelectTrigger>
                    <SelectContent>
                      {categories.map((cat) => (
                        <SelectItem key={cat} value={cat}>{cat}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="auteur">Auteur*</Label>
                  <Input
                    id="auteur"
                    data-testid="article-auteur-input"
                    value={formData.auteur}
                    onChange={(e) => setFormData({ ...formData, auteur: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="image_url">URL Image*</Label>
                <Input
                  id="image_url"
                  data-testid="article-image-input"
                  value={formData.image_url}
                  onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                  required
                />
              </div>

              <div>
                <Label htmlFor="extrait">Extrait*</Label>
                <Textarea
                  id="extrait"
                  data-testid="article-extrait-input"
                  value={formData.extrait}
                  onChange={(e) => setFormData({ ...formData, extrait: e.target.value })}
                  rows={3}
                  required
                />
              </div>

              <div>
                <Label htmlFor="contenu">Contenu*</Label>
                <Textarea
                  id="contenu"
                  data-testid="article-contenu-input"
                  value={formData.contenu}
                  onChange={(e) => setFormData({ ...formData, contenu: e.target.value })}
                  rows={8}
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="tags">Tags (séparés par virgule)</Label>
                  <Input
                    id="tags"
                    data-testid="article-tags-input"
                    value={formData.tags}
                    onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
                  />
                </div>
                <div>
                  <Label htmlFor="temps_lecture">Temps de lecture (min)*</Label>
                  <Input
                    id="temps_lecture"
                    type="number"
                    data-testid="article-temps-input"
                    value={formData.temps_lecture}
                    onChange={(e) => setFormData({ ...formData, temps_lecture: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="vedette"
                  data-testid="article-vedette-checkbox"
                  checked={formData.vedette}
                  onCheckedChange={(checked) => setFormData({ ...formData, vedette: checked })}
                />
                <Label htmlFor="vedette">Article en vedette</Label>
              </div>

              <div className="flex justify-end space-x-2 pt-4">
                <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>
                  Annuler
                </Button>
                <Button type="submit" data-testid="save-article-button" className="bg-osner-red hover:bg-blue-700">
                  Enregistrer
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="bg-white border border-slate-200">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-6 py-3 text-left font-inter text-sm font-medium text-slate-700">Titre</th>
                <th className="px-6 py-3 text-left font-inter text-sm font-medium text-slate-700">Catégorie</th>
                <th className="px-6 py-3 text-left font-inter text-sm font-medium text-slate-700">Auteur</th>
                <th className="px-6 py-3 text-left font-inter text-sm font-medium text-slate-700">Vedette</th>
                <th className="px-6 py-3 text-right font-inter text-sm font-medium text-slate-700">Actions</th>
              </tr>
            </thead>
            <tbody>
              {articles.map((article) => (
                <tr key={article.id} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-6 py-4 font-inter text-sm text-slate-900">{article.titre}</td>
                  <td className="px-6 py-4 font-mono text-xs text-slate-600">{article.categorie}</td>
                  <td className="px-6 py-4 font-inter text-sm text-slate-600">{article.auteur}</td>
                  <td className="px-6 py-4 font-inter text-sm text-slate-600">{article.vedette ? 'Oui' : 'Non'}</td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex justify-end space-x-2">
                      <Button
                        size="sm"
                        variant="outline"
                        data-testid={`edit-article-${article.slug}`}
                        onClick={() => handleEdit(article)}
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="destructive"
                        data-testid={`delete-article-${article.slug}`}
                        onClick={() => handleDelete(article.id)}
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};