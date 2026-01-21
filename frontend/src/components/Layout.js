import { Link, useLocation } from 'react-router-dom';
import { Newspaper, GraduationCap, Briefcase, Menu, X, Mail, User } from 'lucide-react';
import { useState } from 'react';
import { useAuth } from '@/context/AuthContext';

export const Layout = ({ children }) => {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { user } = useAuth();

  const navItems = [
    { path: '/', label: 'Accueil', icon: null },
    { path: '/actualite', label: 'Actualité', icon: Newspaper },
    { path: '/formation', label: 'Formation', icon: GraduationCap },
    { path: '/emploi', label: 'Emploi & Carrière', icon: Briefcase },
    { path: '/admin', label: 'Admin', icon: null },
  ];

  const isActive = (path) => {
    if (path === '/') return location.pathname === '/';
    return location.pathname.startsWith(path);
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      {/* Header */}
      <header className="sticky top-0 z-50 backdrop-blur-md bg-white/90 border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 md:px-8">
          <div className="flex items-center justify-between h-20">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-3">
              <img 
                src="https://customer-assets.emergentagent.com/job_newsedujobs/artifacts/e8d397x7_Osner%20logo.png" 
                alt="Osner-Group Logo" 
                className="h-12 w-auto"
              />
              <span className="font-playfair text-2xl font-bold text-deep-navy tracking-tight">
                Osner-Group
              </span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center space-x-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    data-testid={`nav-link-${item.label.toLowerCase().replace(/\s/g, '-')}`}
                    className={`px-4 py-2 rounded-none font-inter text-sm font-medium transition-colors ${
                      isActive(item.path)
                        ? 'bg-osner-red text-white'
                        : 'text-slate-700 hover:text-osner-red hover:bg-slate-100'
                    }`}
                  >
                    <div className="flex items-center space-x-2">
                      {Icon && <Icon className="w-4 h-4" />}
                      <span>{item.label}</span>
                    </div>
                  </Link>
                );
              })}
              
              {/* Candidate Space Button */}
              {user ? (
                <Link
                  to="/candidate/dashboard"
                  data-testid="candidate-dashboard-link"
                  className="px-4 py-2 bg-deep-navy text-white rounded-none font-inter text-sm font-medium transition-colors hover:bg-slate-800 flex items-center space-x-2"
                >
                  <User className="w-4 h-4" />
                  <span>Mon Espace</span>
                </Link>
              ) : (
                <Link
                  to="/candidate/auth"
                  data-testid="candidate-auth-link"
                  className="px-4 py-2 bg-deep-navy text-white rounded-none font-inter text-sm font-medium transition-colors hover:bg-slate-800"
                >
                  Espace Candidat
                </Link>
              )}
            </nav>

            {/* Mobile menu button */}
            <button
              data-testid="mobile-menu-button"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 text-slate-700 hover:text-electric-blue transition-colors"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

          {/* Mobile Navigation */}
          {mobileMenuOpen && (
            <nav className="md:hidden py-4 border-t border-slate-200">
              {navItems.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    data-testid={`mobile-nav-link-${item.label.toLowerCase().replace(/\s/g, '-')}`}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`flex items-center space-x-3 px-4 py-3 font-inter text-sm font-medium transition-colors ${
                      isActive(item.path)
                        ? 'bg-osner-red text-white'
                        : 'text-slate-700 hover:bg-slate-100'
                    }`}
                  >
                    {Icon && <Icon className="w-4 h-4" />}
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </nav>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">{children}</main>

      {/* Footer */}
      <footer className="bg-deep-navy text-white mt-24">
        <div className="max-w-7xl mx-auto px-4 md:px-8 py-16">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
            {/* Brand */}
            <div className="col-span-1">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-electric-blue rounded-none flex items-center justify-center">
                  <Newspaper className="w-6 h-6 text-white" />
                </div>
                <span className="font-playfair text-xl font-bold">E1 Platform</span>
              </div>
              <p className="font-inter text-sm text-slate-400 leading-relaxed">
                Votre plateforme de référence pour l'actualité, la formation et l'emploi.
              </p>
            </div>

            {/* Navigation */}
            <div>
              <h3 className="font-playfair text-lg font-bold mb-4">Navigation</h3>
              <ul className="space-y-2">
                {navItems.slice(0, 4).map((item) => (
                  <li key={item.path}>
                    <Link
                      to={item.path}
                      data-testid={`footer-link-${item.label.toLowerCase().replace(/\s/g, '-')}`}
                      className="font-inter text-sm text-slate-400 hover:text-electric-blue transition-colors"
                    >
                      {item.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Resources */}
            <div>
              <h3 className="font-playfair text-lg font-bold mb-4">Ressources</h3>
              <ul className="space-y-2 font-inter text-sm text-slate-400">
                <li>
                  <a href="#" className="hover:text-electric-blue transition-colors">
                    À propos
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-electric-blue transition-colors">
                    Contact
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-electric-blue transition-colors">
                    Mentions légales
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-electric-blue transition-colors">
                    Politique de confidentialité
                  </a>
                </li>
              </ul>
            </div>

            {/* Newsletter */}
            <div>
              <h3 className="font-playfair text-lg font-bold mb-4">Newsletter</h3>
              <p className="font-inter text-sm text-slate-400 mb-4">
                Restez informé de nos dernières publications.
              </p>
              <div className="flex items-center space-x-2">
                <Mail className="w-5 h-5 text-slate-400" />
                <span className="font-inter text-sm text-slate-400">
                  Inscription disponible sur la page d'accueil
                </span>
              </div>
            </div>
          </div>

          {/* Bottom bar */}
          <div className="border-t border-slate-800 mt-12 pt-8">
            <p className="font-mono text-xs text-slate-400 text-center">
              © {new Date().getFullYear()} E1 Platform. Tous droits réservés.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};