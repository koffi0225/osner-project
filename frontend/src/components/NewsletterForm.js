import { useState } from 'react';
import { Mail, Send } from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const NewsletterForm = () => {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!email) {
      toast.error('Écrivez votre email');
      return;
    }

    setLoading(true);
    try {
      await axios.post(`${API}/newsletter`, { email });
      toast.success('Merci de votre inscription !');
      setEmail('');
    } catch (error) {
      if (error.response?.status === 400) {
        toast.error('Cet email est déjà inscrit');
      } else {
        toast.error('Une erreur est survenue');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-deep-navy p-8 border border-slate-700">
      <div className="flex items-center space-x-3 mb-4">
        <Mail className="w-6 h-6 text-electric-blue" />
        <h3 className="font-playfair text-xl font-bold text-white">Restez informé</h3>
      </div>
      <p className="font-inter text-sm text-slate-300 mb-6 leading-relaxed">
        Recevez nos dernières actualités, formations et offres d'emploi directement dans votre boîte mail.
      </p>
      <form onSubmit={handleSubmit} className="flex space-x-2">
        <input
          type="email"
          data-testid="newsletter-email-input"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="votre@email.com"
          className="flex-1 px-4 py-3 bg-slate-800 border border-slate-700 text-white font-inter text-sm rounded-none focus:outline-none focus:border-electric-blue transition-colors"
        />
        <button
          type="submit"
          data-testid="newsletter-submit-button"
          disabled={loading}
          className="px-6 py-3 bg-electric-blue text-white font-inter text-sm font-medium rounded-none hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
        >
          <Send className="w-4 h-4" />
          <span>{loading ? 'Envoi...' : 'S\'inscrire'}</span>
        </button>
      </form>
    </div>
  );
};