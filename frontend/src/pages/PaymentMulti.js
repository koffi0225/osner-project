import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { Coins, Check, CreditCard, Smartphone, Building, Landmark, Info } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/payments-multi`;

const PaymentMulti = () => {
  const { token, user } = useAuth();
  const [packages, setPackages] = useState([]);
  const [paymentMethods, setPaymentMethods] = useState([]);
  const [selectedPackage, setSelectedPackage] = useState(null);
  const [selectedMethod, setSelectedMethod] = useState(null);
  const [phoneNumber, setPhoneNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [paymentInstructions, setPaymentInstructions] = useState(null);
  const [showInstructionsDialog, setShowInstructionsDialog] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [packagesRes, methodsRes] = await Promise.all([
        axios.get(`${API}/packages`),
        axios.get(`${API}/methods`)
      ]);
      setPackages(packagesRes.data.packages);
      setPaymentMethods(methodsRes.data.methods);
    } catch (error) {
      toast.error('Erreur lors du chargement des données');
    }
  };

  const getMethodIcon = (iconName) => {
    const icons = {
      'credit-card': CreditCard,
      'smartphone': Smartphone,
      'building': Building,
      'bank': Landmark
    };
    return icons[iconName] || CreditCard;
  };

  const handlePayment = async () => {
    if (!selectedPackage || !selectedMethod) {
      toast.error('Veuillez sélectionner un package et une méthode de paiement');
      return;
    }

    // Vérifier le numéro de téléphone pour Mobile Money
    if (['orange_money', 'mtn_money', 'moov_money', 'wave_ci'].includes(selectedMethod) && !phoneNumber) {
      toast.error('Veuillez entrer votre numéro de téléphone');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        `${API}/initiate`,
        {
          package_id: selectedPackage,
          payment_method: selectedMethod,
          phone_number: phoneNumber || null
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setPaymentInstructions(response.data.payment_data);
      setShowInstructionsDialog(true);
      toast.success('Instructions de paiement générées !');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erreur lors de l\'initialisation du paiement');
    } finally {
      setLoading(false);
    }
  };

  const confirmPayment = async () => {
    if (!paymentInstructions) return;

    try {
      await axios.post(
        `${API}/confirm`,
        { transaction_id: paymentInstructions.transaction_id },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success('Paiement confirmé ! En attente de validation.');
      setShowInstructionsDialog(false);
      setPaymentInstructions(null);
    } catch (error) {
      toast.error('Erreur lors de la confirmation');
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-deep-navy text-white py-12">
        <div className="max-w-7xl mx-auto px-4 md:px-8">
          <div className="flex items-center space-x-3 mb-2">
            <Coins className="w-8 h-8" />
            <h1 className="font-playfair text-4xl font-bold">Recharger des crédits</h1>
          </div>
          <p className="font-inter text-slate-300">
            Choisissez votre mode de paiement préféré
          </p>
        </div>
      </div>

      {/* Current Credits */}
      <div className="max-w-7xl mx-auto px-4 md:px-8 py-8">
        <div className="bg-white p-6 border border-slate-200 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-inter text-sm text-slate-600 mb-1">Crédits actuels</p>
              <p className="font-playfair text-3xl font-bold text-deep-navy">
                {user?.credits || 0}
              </p>
            </div>
            <Coins className="w-12 h-12 text-amber-600" />
          </div>
        </div>

        {/* Packages */}
        <div className="mb-8">
          <h2 className="font-playfair text-2xl font-bold text-deep-navy mb-4">Choisissez votre package</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {packages.map((pkg) => (
              <div
                key={pkg.id}
                onClick={() => setSelectedPackage(pkg.id)}
                className={`bg-white border-2 p-6 cursor-pointer transition-all ${
                  selectedPackage === pkg.id ? 'border-osner-red shadow-lg' : 'border-slate-200 hover:border-osner-red'
                } ${pkg.popular ? 'relative' : ''}`}
              >
                {pkg.popular && (
                  <div className="absolute top-0 right-0 bg-osner-red text-white px-3 py-1 font-inter text-xs font-medium">
                    POPULAIRE
                  </div>
                )}
                
                <div className="text-center mb-4">
                  <h3 className="font-playfair text-xl font-bold text-deep-navy mb-2">
                    {pkg.name}
                  </h3>
                  <div className="flex items-baseline justify-center mb-2">
                    <span className="font-playfair text-3xl font-bold text-deep-navy">
                      {pkg.amount.toLocaleString()}
                    </span>
                    <span className="ml-2 text-slate-600">XOF</span>
                  </div>
                  <p className="font-inter text-sm text-slate-600">
                    {pkg.credits} crédit{pkg.credits > 1 ? 's' : ''}
                  </p>
                </div>

                <p className="font-inter text-sm text-slate-600 text-center">
                  {pkg.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Payment Methods */}
        <div className="mb-8">
          <h2 className="font-playfair text-2xl font-bold text-deep-navy mb-4">Mode de paiement</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {paymentMethods.map((method) => {
              const Icon = getMethodIcon(method.icon);
              return (
                <div
                  key={method.id}
                  onClick={() => setSelectedMethod(method.id)}
                  className={`bg-white border-2 p-4 cursor-pointer transition-all ${
                    selectedMethod === method.id ? 'border-osner-red shadow-lg' : 'border-slate-200 hover:border-osner-red'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                      selectedMethod === method.id ? 'bg-osner-red' : 'bg-slate-100'
                    }`}>
                      <Icon className={`w-5 h-5 ${
                        selectedMethod === method.id ? 'text-white' : 'text-slate-600'
                      }`} />
                    </div>
                    <div className="flex-1">
                      <p className="font-inter font-medium text-deep-navy">{method.name}</p>
                      {method.ussd_code && (
                        <p className="font-mono text-xs text-slate-500">{method.ussd_code}</p>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Phone Number for Mobile Money */}
        {selectedMethod && ['orange_money', 'mtn_money', 'moov_money'].includes(selectedMethod) && (
          <div className="bg-white p-6 border border-slate-200 mb-8">
            <Label htmlFor="phone-number">Numéro de téléphone Mobile Money</Label>
            <Input
              id="phone-number"
              type="tel"
              placeholder="+225 XX XX XX XX XX"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              className="mt-2"
            />
          </div>
        )}

        {/* Pay Button */}
        <Button
          onClick={handlePayment}
          disabled={!selectedPackage || !selectedMethod || loading}
          className="w-full md:w-auto bg-osner-red hover:bg-red-700 py-6 text-lg"
        >
          {loading ? 'Traitement...' : 'Procéder au paiement'}
        </Button>

        {/* Info */}
        <div className="mt-8 bg-blue-50 border border-blue-200 p-6">
          <div className="flex items-start space-x-3">
            <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-1" />
            <div>
              <h3 className="font-playfair text-lg font-bold text-blue-900 mb-2">
                Modes de paiement disponibles
              </h3>
              <ul className="space-y-2 font-inter text-sm text-blue-800">
                <li>💳 <strong>Carte Bancaire</strong> : Visa, Mastercard (paiement sécurisé Stripe)</li>
                <li>📱 <strong>Mobile Money</strong> : Orange, MTN, Moov (validation instantanée)</li>
                <li>🏛️ <strong>Trésor Money</strong> : Paiement en bureau de poste</li>
                <li>🏦 <strong>Virement Bancaire</strong> : Traitement sous 24-48h</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Instructions Dialog */}
      <Dialog open={showInstructionsDialog} onOpenChange={setShowInstructionsDialog}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="font-playfair text-2xl">
              {paymentInstructions?.instructions?.title || 'Instructions de paiement'}
            </DialogTitle>
          </DialogHeader>
          
          {paymentInstructions && (
            <div className="space-y-4">
              {/* Transaction ID */}
              <div className="bg-slate-50 p-4 rounded">
                <p className="font-inter text-sm text-slate-600 mb-1">Référence de transaction</p>
                <p className="font-mono font-bold text-deep-navy">{paymentInstructions.transaction_id}</p>
              </div>

              {/* Steps */}
              {paymentInstructions.instructions?.steps && (
                <div>
                  <h3 className="font-playfair font-bold text-deep-navy mb-3">Étapes à suivre :</h3>
                  <ol className="space-y-2">
                    {paymentInstructions.instructions.steps.map((step, idx) => (
                      <li key={idx} className="flex items-start space-x-3">
                        <span className="flex-shrink-0 w-6 h-6 bg-osner-red text-white rounded-full flex items-center justify-center text-sm font-bold">
                          {idx + 1}
                        </span>
                        <span className="font-inter text-sm text-slate-700">{step}</span>
                      </li>
                    ))}
                  </ol>
                </div>
              )}

              {/* Bank Details */}
              {paymentInstructions.bank_details && (
                <div className="bg-blue-50 border border-blue-200 p-4">
                  <h3 className="font-playfair font-bold text-blue-900 mb-3">Coordonnées bancaires :</h3>
                  <div className="space-y-2 font-inter text-sm">
                    <p><strong>Bénéficiaire :</strong> {paymentInstructions.bank_details.beneficiary}</p>
                    <p><strong>Banque :</strong> {paymentInstructions.bank_details.bank}</p>
                    <p><strong>IBAN :</strong> <span className="font-mono">{paymentInstructions.bank_details.iban}</span></p>
                    <p><strong>SWIFT :</strong> <span className="font-mono">{paymentInstructions.bank_details.swift}</span></p>
                    <p className="text-osner-red"><strong>Montant :</strong> {paymentInstructions.bank_details.amount}</p>
                    <p className="text-osner-red"><strong>Référence :</strong> {paymentInstructions.bank_details.reference}</p>
                  </div>
                </div>
              )}

              {/* Note */}
              {paymentInstructions.instructions?.note && (
                <div className="bg-amber-50 border border-amber-200 p-4">
                  <p className="font-inter text-sm text-amber-900">
                    <strong>Note :</strong> {paymentInstructions.instructions.note}
                  </p>
                </div>
              )}

              {/* Action Button */}
              <div className="flex justify-end space-x-3">
                <Button variant="outline" onClick={() => setShowInstructionsDialog(false)}>
                  Fermer
                </Button>
                <Button onClick={confirmPayment} className="bg-osner-red hover:bg-red-700">
                  J'ai effectué le paiement
                </Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default PaymentMulti;
