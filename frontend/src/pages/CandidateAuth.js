import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { UserPlus, LogIn, Briefcase } from 'lucide-react';
import { toast } from 'sonner';

const CandidateAuth = () => {
  const navigate = useNavigate();
  const { login, register } = useAuth();
  const [loading, setLoading] = useState(false);

  const [loginForm, setLoginForm] = useState({ email: '', password: '' });
  const [registerForm, setRegisterForm] = useState({
    email: '',
    password: '',
    nom: '',
    prenom: '',
    sexe: 'M',
    telephone: ''
  });

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login(loginForm.email, loginForm.password);
      toast.success('Connexion réussie !');
      navigate('/candidate/dashboard');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await register(registerForm);
      toast.success('Inscription réussie !');
      navigate('/candidate/dashboard');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erreur d\'inscription');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center py-12 px-4">
      <div className="max-w-md w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center mb-4">
            <img 
              src="https://customer-assets.emergentagent.com/job_newsedujobs/artifacts/e8d397x7_Osner%20logo.png" 
              alt="Osner-Group Logo" 
              className="h-16 w-auto"
            />
          </div>
          <h1 className="font-playfair text-3xl font-bold text-deep-navy mb-2">
            Espace Candidat
          </h1>
          <p className="font-inter text-slate-600">
            Accédez à votre espace personnel Osner-Group
          </p>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="login" className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-6">
            <TabsTrigger value="login" data-testid="tab-login">
              <LogIn className="w-4 h-4 mr-2" />
              Connexion
            </TabsTrigger>
            <TabsTrigger value="register" data-testid="tab-register">
              <UserPlus className="w-4 h-4 mr-2" />
              Inscription
            </TabsTrigger>
          </TabsList>

          {/* Login Tab */}
          <TabsContent value="login">
            <div className="bg-white p-8 border border-slate-200">
              <form onSubmit={handleLogin} className="space-y-4">
                <div>
                  <Label htmlFor="login-email">Email</Label>
                  <Input
                    id="login-email"
                    type="email"
                    data-testid="login-email-input"
                    value={loginForm.email}
                    onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="login-password">Mot de passe</Label>
                  <Input
                    id="login-password"
                    type="password"
                    data-testid="login-password-input"
                    value={loginForm.password}
                    onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                    required
                  />
                </div>
                <Button
                  type="submit"
                  data-testid="login-submit-button"
                  className="w-full bg-osner-red hover:bg-blue-700"
                  disabled={loading}
                >
                  {loading ? 'Connexion...' : 'Se connecter'}
                </Button>
              </form>
            </div>
          </TabsContent>

          {/* Register Tab */}
          <TabsContent value="register">
            <div className="bg-white p-8 border border-slate-200">
              <form onSubmit={handleRegister} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="register-prenom">Prénom</Label>
                    <Input
                      id="register-prenom"
                      data-testid="register-prenom-input"
                      value={registerForm.prenom}
                      onChange={(e) => setRegisterForm({ ...registerForm, prenom: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="register-nom">Nom</Label>
                    <Input
                      id="register-nom"
                      data-testid="register-nom-input"
                      value={registerForm.nom}
                      onChange={(e) => setRegisterForm({ ...registerForm, nom: e.target.value })}
                      required
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="register-email">Email</Label>
                  <Input
                    id="register-email"
                    type="email"
                    data-testid="register-email-input"
                    value={registerForm.email}
                    onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })}
                    required
                  />
                </div>
                <div>\n                  <Label htmlFor="register-telephone">Téléphone (optionnel)</Label>
                  <Input
                    id="register-telephone"
                    data-testid="register-telephone-input"
                    value={registerForm.telephone}
                    onChange={(e) => setRegisterForm({ ...registerForm, telephone: e.target.value })}
                  />
                </div>
                <div>
                  <Label htmlFor="register-sexe">Sexe</Label>
                  <select
                    id="register-sexe"
                    data-testid="register-sexe-select"
                    value={registerForm.sexe}
                    onChange={(e) => setRegisterForm({ ...registerForm, sexe: e.target.value })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-osner-red"
                  >
                    <option value="M">Masculin</option>
                    <option value="F">Féminin</option>
                  </select>
                </div>
                <div>
                  <Label htmlFor="register-password">Mot de passe</Label>
                  <Input
                    id="register-password"
                    type="password"
                    data-testid="register-password-input"
                    value={registerForm.password}
                    onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })}
                    required
                  />
                </div>
                <Button
                  type="submit"
                  data-testid="register-submit-button"
                  className="w-full bg-osner-red hover:bg-blue-700"
                  disabled={loading}
                >
                  {loading ? 'Inscription...' : 'S\'inscrire'}
                </Button>
              </form>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default CandidateAuth;