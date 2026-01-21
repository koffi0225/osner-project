import { useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/candidate`;

const CVUpload = () => {
  const { token } = useAuth();
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.name.endsWith('.pdf') || selectedFile.name.endsWith('.docx')) {
        setFile(selectedFile);
        setResult(null);
      } else {
        toast.error('Seuls les fichiers PDF et DOCX sont acceptés');
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      toast.error('Veuillez sélectionner un fichier');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API}/cv/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${token}`
        }
      });

      setResult(response.data);
      toast.success(response.data.message);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erreur lors de l\'upload');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-deep-navy text-white py-12">
        <div className="max-w-4xl mx-auto px-4 md:px-8">
          <h1 className="font-playfair text-4xl font-bold mb-2">Uploader mon CV</h1>
          <p className="font-inter text-slate-300">
            Analysez votre CV et obtenez des suggestions pour l'optimiser
          </p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 md:px-8 py-12">
        {/* Upload Section */}
        <div className="bg-white p-8 border border-slate-200 mb-8">
          <div className="text-center mb-6">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-electric-blue rounded-none mb-4">
              <FileText className="w-8 h-8 text-white" />
            </div>
            <h2 className="font-playfair text-2xl font-bold text-deep-navy mb-2">
              Sélectionnez votre CV
            </h2>
            <p className="font-inter text-sm text-slate-600">
              Formats acceptés : PDF, DOCX
            </p>
          </div>

          <div className="max-w-md mx-auto">
            <div className="border-2 border-dashed border-slate-300 p-8 text-center mb-4">
              <input
                type="file"
                id="cv-file"
                data-testid="cv-file-input"
                accept=".pdf,.docx"
                onChange={handleFileChange}
                className="hidden"
              />
              <label
                htmlFor="cv-file"
                className="cursor-pointer inline-flex flex-col items-center"
              >
                <Upload className="w-12 h-12 text-slate-400 mb-4" />
                <span className="font-inter text-sm text-slate-600">
                  {file ? file.name : 'Cliquez pour sélectionner un fichier'}
                </span>
              </label>
            </div>

            <Button
              onClick={handleUpload}
              data-testid="upload-cv-button"
              disabled={!file || uploading}
              className="w-full bg-electric-blue hover:bg-blue-700"
            >
              {uploading ? 'Analyse en cours...' : 'Analyser mon CV'}
            </Button>
          </div>
        </div>

        {/* Results Section */}
        {result && (
          <div className="bg-white p-8 border border-slate-200">
            <div className="flex items-center space-x-3 mb-6">
              <CheckCircle className="w-6 h-6 text-green-600" />
              <h2 className="font-playfair text-2xl font-bold text-deep-navy">
                Analyse complète
              </h2>
            </div>

            {result.parsed_data && (
              <div className="space-y-6">
                {/* Compétences */}
                {result.parsed_data.competences && result.parsed_data.competences.length > 0 && (
                  <div>
                    <h3 className="font-playfair text-lg font-bold text-deep-navy mb-3">
                      Compétences identifiées
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {result.parsed_data.competences.map((comp, idx) => (
                        <span
                          key={idx}
                          className="px-3 py-1 bg-electric-blue text-white font-inter text-sm"
                        >
                          {comp}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Expérience */}
                {result.parsed_data.experience && result.parsed_data.experience.length > 0 && (
                  <div>
                    <h3 className="font-playfair text-lg font-bold text-deep-navy mb-3">
                      Expérience professionnelle
                    </h3>
                    <div className="space-y-3">
                      {result.parsed_data.experience.map((exp, idx) => (
                        <div key={idx} className="p-4 bg-slate-50 border border-slate-200">
                          <p className="font-inter font-medium text-deep-navy">{exp.poste}</p>
                          <p className="font-inter text-sm text-slate-600">
                            {exp.entreprise} | {exp.duree}
                          </p>
                          {exp.description && (
                            <p className="font-inter text-sm text-slate-600 mt-2">
                              {exp.description}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Formation */}
                {result.parsed_data.formation && result.parsed_data.formation.length > 0 && (
                  <div>
                    <h3 className="font-playfair text-lg font-bold text-deep-navy mb-3">
                      Formation
                    </h3>
                    <div className="space-y-2">
                      {result.parsed_data.formation.map((form, idx) => (
                        <div key={idx} className="p-3 bg-slate-50 border border-slate-200">
                          <p className="font-inter font-medium text-deep-navy">{form.diplome}</p>
                          <p className="font-inter text-sm text-slate-600">
                            {form.etablissement} | {form.annee}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {result.parsed_data && result.parsed_data.error && (
              <div className="flex items-start space-x-3 p-4 bg-amber-50 border border-amber-200">
                <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-inter text-sm text-amber-800">
                    L'analyse complète n'a pas pu être effectuée. Vous pouvez toujours utiliser votre CV pour le matching.
                  </p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default CVUpload;