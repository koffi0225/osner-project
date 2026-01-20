import { useEffect, useState } from 'react';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Plus, Edit, Trash2 } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const types = ['Emploi', 'Stage', 'Concours'];

export const EmploisAdmin = () => {
  const [emplois, setEmplois] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingEmploi, setEditingEmploi] = useState(null);
  const [formData, setFormData] = useState({
    titre: '',
    slug: '',
    type: '',
    entreprise: '',
    secteur: '',
    localisation: '',
    description: '',
    exigences: '',
    url_candidature: '',
  });

  useEffect(() => {
    loadEmplois();
  }, []);

  const loadEmplois = async () => {
    try {
      const response = await axios.get(`${API}/emplois?limit=100`);
      setEmplois(response.data);
    } catch (error) {
      toast.error('Erreur lors du chargement des offres');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const payload = {
      ...formData,
      exigences: formData.exigences ? formData.exigences.split('\n').filter(e => e.trim()) : [],
    };

    try {
      if (editingEmploi) {
        await axios.put(`${API}/emplois/${editingEmploi.id}`, payload);
        toast.success('Offre mise à jour');
      } else {
        await axios.post(`${API}/emplois`, payload);
        toast.success('Offre créée');
      }
      setDialogOpen(false);
      resetForm();
      loadEmplois();
    } catch (error) {
      toast.error('Erreur lors de la sauvegarde');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cette offre ?')) return;
    
    try {
      await axios.delete(`${API}/emplois/${id}`);
      toast.success('Offre supprimée');
      loadEmplois();
    } catch (error) {
      toast.error('Erreur lors de la suppression');
    }
  };

  const handleEdit = (emploi) => {
    setEditingEmploi(emploi);
    setFormData({
      titre: emploi.titre,
      slug: emploi.slug,
      type: emploi.type,
      entreprise: emploi.entreprise,
      secteur: emploi.secteur,
      localisation: emploi.localisation,
      description: emploi.description,
      exigences: emploi.exigences.join('\n'),
      url_candidature: emploi.url_candidature || '',
    });
    setDialogOpen(true);
  };

  const resetForm = () => {
    setEditingEmploi(null);
    setFormData({
      titre: '',
      slug: '',
      type: '',
      entreprise: '',
      secteur: '',
      localisation: '',
      description: '',
      exigences: '',
      url_candidature: '',
    });
  };

  if (loading) {
    return <div className="text-center py-8">Chargement...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="font-playfair text-2xl font-bold text-deep-navy">Gestion des offres d'emploi</h2>
        <Dialog open={dialogOpen} onOpenChange={(open) => {
          setDialogOpen(open);
          if (!open) resetForm();
        }}>
          <DialogTrigger asChild>
            <Button data-testid="add-emploi-button" className="bg-electric-blue hover:bg-blue-700">
              <Plus className="w-4 h-4 mr-2" />
              Nouvelle offre
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>{editingEmploi ? 'Éditer' : 'Nouvelle'} offre</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="titre">Titre*</Label>
                  <Input
                    id="titre"
                    data-testid="emploi-titre-input"
                    value={formData.titre}
                    onChange={(e) => setFormData({ ...formData, titre: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="slug">Slug*</Label>
                  <Input
                    id="slug"
                    data-testid="emploi-slug-input"
                    value={formData.slug}
                    onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="type">Type*</Label>
                  <Select value={formData.type} onValueChange={(value) => setFormData({ ...formData, type: value })}>
                    <SelectTrigger data-testid="emploi-type-select">
                      <SelectValue placeholder="Sélectionnez" />
                    </SelectTrigger>
                    <SelectContent>
                      {types.map((type) => (
                        <SelectItem key={type} value={type}>{type}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="entreprise">Entreprise*</Label>
                  <Input
                    id="entreprise"
                    data-testid="emploi-entreprise-input"
                    value={formData.entreprise}
                    onChange={(e) => setFormData({ ...formData, entreprise: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="secteur">Secteur*</Label>
                  <Input
                    id="secteur"
                    data-testid="emploi-secteur-input"
                    value={formData.secteur}
                    onChange={(e) => setFormData({ ...formData, secteur: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="localisation">Localisation*</Label>
                <Input
                  id="localisation"
                  data-testid="emploi-localisation-input"
                  value={formData.localisation}
                  onChange={(e) => setFormData({ ...formData, localisation: e.target.value })}
                  required
                />
              </div>

              <div>
                <Label htmlFor="description">Description*</Label>
                <Textarea
                  id="description"
                  data-testid="emploi-description-input"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows={5}
                  required
                />
              </div>

              <div>
                <Label htmlFor="exigences">Exigences (une par ligne)*</Label>
                <Textarea
                  id="exigences"
                  data-testid="emploi-exigences-input"
                  value={formData.exigences}
                  onChange={(e) => setFormData({ ...formData, exigences: e.target.value })}
                  rows={5}
                  required
                />
              </div>

              <div>
                <Label htmlFor="url_candidature">URL de candidature</Label>
                <Input
                  id="url_candidature"
                  data-testid="emploi-url-input"
                  value={formData.url_candidature}
                  onChange={(e) => setFormData({ ...formData, url_candidature: e.target.value })}
                  placeholder="https://..."
                />
              </div>

              <div className="flex justify-end space-x-2 pt-4">
                <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>
                  Annuler
                </Button>
                <Button type="submit" data-testid="save-emploi-button" className="bg-electric-blue hover:bg-blue-700">
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
                <th className="px-6 py-3 text-left font-inter text-sm font-medium text-slate-700">Entreprise</th>
                <th className="px-6 py-3 text-left font-inter text-sm font-medium text-slate-700">Type</th>
                <th className="px-6 py-3 text-left font-inter text-sm font-medium text-slate-700">Localisation</th>
                <th className="px-6 py-3 text-right font-inter text-sm font-medium text-slate-700">Actions</th>
              </tr>
            </thead>
            <tbody>
              {emplois.map((emploi) => (
                <tr key={emploi.id} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-6 py-4 font-inter text-sm text-slate-900">{emploi.titre}</td>
                  <td className="px-6 py-4 font-inter text-sm text-slate-600">{emploi.entreprise}</td>
                  <td className="px-6 py-4 font-mono text-xs text-slate-600">{emploi.type}</td>
                  <td className="px-6 py-4 font-inter text-sm text-slate-600">{emploi.localisation}</td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex justify-end space-x-2">
                      <Button
                        size="sm"
                        variant="outline"
                        data-testid={`edit-emploi-${emploi.slug}`}
                        onClick={() => handleEdit(emploi)}
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="destructive"
                        data-testid={`delete-emploi-${emploi.slug}`}
                        onClick={() => handleDelete(emploi.id)}
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