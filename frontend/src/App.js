import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from '@/components/ui/sonner';
import { Layout } from '@/components/Layout';
import Home from '@/pages/Home';
import Actualite from '@/pages/Actualite';
import ArticleDetail from '@/pages/ArticleDetail';
import Formation from '@/pages/Formation';
import FormationDetail from '@/pages/FormationDetail';
import Emploi from '@/pages/Emploi';
import EmploiDetail from '@/pages/EmploiDetail';
import Admin from '@/pages/Admin';
import '@/App.css';

function App() {
  return (
    <>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/actualite" element={<Actualite />} />
            <Route path="/actualite/:slug" element={<ArticleDetail />} />
            <Route path="/formation" element={<Formation />} />
            <Route path="/formation/:slug" element={<FormationDetail />} />
            <Route path="/emploi" element={<Emploi />} />
            <Route path="/emploi/:slug" element={<EmploiDetail />} />
            <Route path="/admin" element={<Admin />} />
          </Routes>
        </Layout>
      </BrowserRouter>
      <Toaster position="top-right" />
    </>
  );
}

export default App;