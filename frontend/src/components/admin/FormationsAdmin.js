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

const niveaux = ['Débutant', 'Intermédiaire', 'Avancé'];

export const FormationsAdmin = () => {
  const [formations, setFormations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingFormation, setEditingFormation] = useState(null);
  const [formData, setFormData] = useState({
    titre: '',
    slug: '',
    thematique: '',
    niveau: '',
    objectifs: '',
    image_url: '',
    contenu: '',
    description: '',
    duree: '',
    ressources: '',
  });

  useEffect(() => {
    loadFormations();
  }, []);

  const loadFormations = async () => {
    try {
      const response = await axios.get(`${API}/formations?limit=100`);
      setFormations(response.data);
    } catch (error) {
      toast.error('Erreur lors du chargement des formations');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const payload = {
      ...formData,
      objectifs: formData.objectifs ? formData.objectifs.split('\n').filter(o => o.trim()) : [],
      ressources: formData.ressources ? formData.ressources.split('\n').filter(r => r.trim()) : [],
    };

    try {
      if (editingFormation) {
        await axios.put(`${API}/formations/${editingFormation.id}`, payload);
        toast.success('Formation mise à jour');
      } else {
        await axios.post(`${API}/formations`, payload);
        toast.success('Formation créée');
      }
      setDialogOpen(false);
      resetForm();
      loadFormations();
    } catch (error) {
      toast.error('Erreur lors de la sauvegarde');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cette formation ?')) return;
    
    try {
      await axios.delete(`${API}/formations/${id}`);
      toast.success('Formation supprimée');
      loadFormations();
    } catch (error) {
      toast.error('Erreur lors de la suppression');
    }
  };

  const handleEdit = (formation) => {
    setEditingFormation(formation);
    setFormData({
      titre: formation.titre,
      slug: formation.slug,
      thematique: formation.thematique,
      niveau: formation.niveau,
      objectifs: formation.objectifs.join('\n'),
      image_url: formation.image_url,
      contenu: formation.contenu,
      description: formation.description,
      duree: formation.duree,
      ressources: formation.ressources.join('\n'),
    });
    setDialogOpen(true);
  };

  const resetForm = () => {
    setEditingFormation(null);
    setFormData({
      titre: '',
      slug: '',
      thematique: '',
      niveau: '',
      objectifs: '',
      image_url: '',
      contenu: '',
      description: '',
      duree: '',
      ressources: '',
    });
  };

  if (loading) {
    return <div className="text-center py-8">Chargement...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="font-playfair text-2xl font-bold text-deep-navy">Gestion des formations</h2>
        <Dialog open={dialogOpen} onOpenChange={(open) => {
          setDialogOpen(open);
          if (!open) resetForm();
        }}>
          <DialogTrigger asChild>
            <Button data-testid="add-formation-button" className="bg-osner-red hover:bg-blue-700">
              <Plus className="w-4 h-4 mr-2" />
              Nouvelle formation
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>{editingFormation ? 'Éditer' : 'Nouvelle'} formation</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="titre">Titre*</Label>
                  <Input
                    id="titre"
                    data-testid="formation-titre-input"
                    value={formData.titre}
                    onChange={(e) => setFormData({ ...formData, titre: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="slug">Slug*</Label>
                  <Input
                    id="slug"
                    data-testid="formation-slug-input"
                    value={formData.slug}
                    onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="thematique">Thématique*</Label>
                  <Input
                    id="thematique"
                    data-testid="formation-thematique-input"
                    value={formData.thematique}
                    onChange={(e) => setFormData({ ...formData, thematique: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="niveau">Niveau*</Label>
                  <Select value={formData.niveau} onValueChange={(value) => setFormData({ ...formData, niveau: value })}>
                    <SelectTrigger data-testid="formation-niveau-select">
                      <SelectValue placeholder="Sélectionnez" />
                    </SelectTrigger>
                    <SelectContent>
                      {niveaux.map((niveau) => (
                        <SelectItem key={niveau} value={niveau}>{niveau}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="duree">Durée*</Label>
                  <Input
                    id="duree"
                    data-testid="formation-duree-input"
                    placeholder="Ex: 10 heures"
                    value={formData.duree}
                    onChange={(e) => setFormData({ ...formData, duree: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="image_url">URL Image*</Label>
                <Input
                  id="image_url"
                  data-testid="formation-image-input"
                  value={formData.image_url}
                  onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                  required
                />
              </div>

              <div>
                <Label htmlFor="description">Description*</Label>
                <Textarea
                  id="description"
                  data-testid="formation-description-input"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows={3}
                  required
                />
              </div>

              <div>
                <Label htmlFor="objectifs">Objectifs (un par ligne)*</Label>
                <Textarea
                  id="objectifs"
                  data-testid="formation-objectifs-input"
                  value={formData.objectifs}
                  onChange={(e) => setFormData({ ...formData, objectifs: e.target.value })}
                  rows={4}
                  required
                />
              </div>

              <div>
                <Label htmlFor="contenu">Contenu*</Label>
                <Textarea
                  id="contenu"
                  data-testid="formation-contenu-input"
                  value={formData.contenu}
                  onChange={(e) => setFormData({ ...formData, contenu: e.target.value })}
                  rows={8}
                  required
                />
              </div>

              <div>
                <Label htmlFor="ressources">Ressources (une par ligne)</Label>
                <Textarea
                  id="ressources"
                  data-testid="formation-ressources-input"
                  value={formData.ressources}
                  onChange={(e) => setFormData({ ...formData, ressources: e.target.value })}
                  rows={3}
                />
              </div>

              <div className="flex justify-end space-x-2 pt-4">
                <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>
                  Annuler
                </Button>
                <Button type="submit" data-testid="save-formation-button" className="bg-osner-red hover:bg-blue-700">
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
                <th className="px-6 py-3 text-left font-inter text-sm font-medium text-slate-700">Thématique</th>
                <th className="px-6 py-3 text-left font-inter text-sm font-medium text-slate-700">Niveau</th>
                <th className="px-6 py-3 text-left font-inter text-sm font-medium text-slate-700">Durée</th>
                <th className="px-6 py-3 text-right font-inter text-sm font-medium text-slate-700">Actions</th>
              </tr>
            </thead>
            <tbody>
              {formations.map((formation) => (
                <tr key={formation.id} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-6 py-4 font-inter text-sm text-slate-900">{formation.titre}</td>
                  <td className="px-6 py-4 font-mono text-xs text-slate-600">{formation.thematique}</td>
                  <td className="px-6 py-4 font-mono text-xs text-slate-600">{formation.niveau}</td>
                  <td className="px-6 py-4 font-inter text-sm text-slate-600">{formation.duree}</td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex justify-end space-x-2">
                      <Button
                        size="sm"
                        variant="outline"
                        data-testid={`edit-formation-${formation.slug}`}
                        onClick={() => handleEdit(formation)}
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="destructive"
                        data-testid={`delete-formation-${formation.slug}`}
                        onClick={() => handleDelete(formation.id)}
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