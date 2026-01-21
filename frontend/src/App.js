import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from '@/components/ui/sonner';
import { Layout } from '@/components/Layout';
import { AuthProvider } from '@/context/AuthContext';
import { ProtectedRoute } from '@/components/ProtectedRoute';
import Home from '@/pages/Home';
import Actualite from '@/pages/Actualite';
import ArticleDetail from '@/pages/ArticleDetail';
import Formation from '@/pages/Formation';
import FormationDetail from '@/pages/FormationDetail';
import Emploi from '@/pages/Emploi';
import EmploiDetail from '@/pages/EmploiDetail';
import Admin from '@/pages/Admin';
import CandidateAuth from '@/pages/CandidateAuth';
import CandidateDashboard from '@/pages/CandidateDashboard';
import CVUpload from '@/pages/CVUpload';
import JobMatching from '@/pages/JobMatching';
import Payment from '@/pages/Payment';
import PaymentMulti from '@/pages/PaymentMulti';
import PaymentSuccess from '@/pages/PaymentSuccess';
import '@/App.css';

function App() {
  return (
    <AuthProvider>
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
            
            {/* Candidate Routes */}
            <Route path="/candidate/auth" element={<CandidateAuth />} />
            <Route path="/candidate/dashboard" element={<ProtectedRoute><CandidateDashboard /></ProtectedRoute>} />
            <Route path="/candidate/cv-upload" element={<ProtectedRoute><CVUpload /></ProtectedRoute>} />
            <Route path="/candidate/matching" element={<ProtectedRoute><JobMatching /></ProtectedRoute>} />
            <Route path="/candidate/payment" element={<ProtectedRoute><PaymentMulti /></ProtectedRoute>} />
            <Route path="/candidate/payment-success" element={<ProtectedRoute><PaymentSuccess /></ProtectedRoute>} />
          </Routes>
        </Layout>
      </BrowserRouter>
      <Toaster position="top-right" />
    </AuthProvider>
  );
}

export default App;