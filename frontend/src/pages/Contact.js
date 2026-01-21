import { Mail, Phone, MapPin, Send } from 'lucide-react';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { toast } from 'sonner';

const Contact = () => {
  const [formData, setFormData] = useState({
    nom: '',
    email: '',
    telephone: '',
    sujet: '',
    message: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    // Simuler l'envoi (à remplacer par un vrai endpoint)
    setTimeout(() => {
      toast.success('Message envoyé ! Nous vous répondrons dans les 24h.');
      setFormData({ nom: '', email: '', telephone: '', sujet: '', message: '' });
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-deep-navy text-white py-16">
        <div className="max-w-7xl mx-auto px-4 md:px-8">
          <h1 className="font-playfair text-4xl md:text-5xl font-bold mb-4">Contactez-nous</h1>
          <p className="font-inter text-lg text-slate-300">
            Notre équipe est à votre écoute pour répondre à toutes vos questions
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 md:px-8 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Contact Info */}
          <div>
            <h2 className="font-playfair text-3xl font-bold text-deep-navy mb-8">
              Nos coordonnées
            </h2>

            <div className="space-y-6">
              {/* Téléphone Mobile */}
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-osner-red rounded-none flex items-center justify-center flex-shrink-0">
                  <Phone className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="font-playfair text-lg font-bold text-deep-navy mb-2">Téléphone Mobile</h3>
                  <p className="font-inter text-slate-600">+225 07 07 592 286</p>
                  <p className="font-inter text-slate-600">+225 05 44 498 515</p>
                </div>
              </div>

              {/* Téléphone Fixe */}
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-osner-red rounded-none flex items-center justify-center flex-shrink-0">
                  <Phone className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="font-playfair text-lg font-bold text-deep-navy mb-2">Téléphone Fixe</h3>
                  <p className="font-inter text-slate-600">+225 27 31 960 751</p>
                </div>
              </div>

              {/* Email */}
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-osner-red rounded-none flex items-center justify-center flex-shrink-0">
                  <Mail className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="font-playfair text-lg font-bold text-deep-navy mb-2">Email</h3>
                  <p className="font-inter text-slate-600">contact@osner-group.com</p>
                  <p className="font-inter text-slate-600">info@osner-group.com</p>
                </div>
              </div>

              {/* Adresse */}
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-osner-red rounded-none flex items-center justify-center flex-shrink-0">
                  <MapPin className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="font-playfair text-lg font-bold text-deep-navy mb-2">Adresse</h3>
                  <p className="font-inter text-slate-600">Abidjan, Côte d'Ivoire</p>
                  <p className="font-inter text-sm text-slate-500 mt-2">Manager : Melvin Tayorault</p>
                </div>
              </div>
            </div>

            {/* Horaires */}
            <div className="mt-8 bg-blue-50 border border-blue-200 p-6">
              <h3 className="font-playfair text-lg font-bold text-blue-900 mb-3">Horaires d'ouverture</h3>
              <div className="space-y-2 font-inter text-sm text-blue-800">
                <p><strong>Lundi - Vendredi :</strong> 8h00 - 18h00</p>
                <p><strong>Samedi :</strong> 9h00 - 13h00</p>
                <p><strong>Dimanche :</strong> Fermé</p>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <div className="bg-white p-8 border border-slate-200">
            <h2 className="font-playfair text-2xl font-bold text-deep-navy mb-6">
              Envoyez-nous un message
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="nom">Nom complet *</Label>
                <Input
                  id="nom"
                  value={formData.nom}
                  onChange={(e) => setFormData({ ...formData, nom: e.target.value })}
                  required
                />
              </div>

              <div>
                <Label htmlFor="email">Email *</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                />
              </div>

              <div>
                <Label htmlFor="telephone">Téléphone</Label>
                <Input
                  id="telephone"
                  type="tel"
                  value={formData.telephone}
                  onChange={(e) => setFormData({ ...formData, telephone: e.target.value })}
                />
              </div>

              <div>
                <Label htmlFor="sujet">Sujet *</Label>
                <Input
                  id="sujet"
                  value={formData.sujet}
                  onChange={(e) => setFormData({ ...formData, sujet: e.target.value })}
                  required
                />
              </div>

              <div>
                <Label htmlFor="message">Message *</Label>
                <Textarea
                  id="message"
                  value={formData.message}
                  onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                  rows={6}
                  required
                />
              </div>

              <Button
                type="submit"
                disabled={loading}
                className="w-full bg-osner-red hover:bg-red-700"
              >
                <Send className="w-4 h-4 mr-2" />
                {loading ? 'Envoi en cours...' : 'Envoyer le message'}
              </Button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;