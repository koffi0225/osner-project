"""
Système de paiement multi-méthodes pour Côte d'Ivoire
Supporte: Stripe (cartes), Mobile Money (Orange, MTN, Moov), Trésor Money
"""

from enum import Enum
from typing import Dict, Any, Optional
import uuid
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class PaymentMethod(str, Enum):
    STRIPE = "stripe"
    ORANGE_MONEY = "orange_money"
    MTN_MONEY = "mtn_money"
    MOOV_MONEY = "moov_money"
    TRESOR_MONEY = "tresor_money"
    BANK_TRANSFER = "bank_transfer"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

class PaymentProcessor:
    """Processeur de paiements multi-méthodes"""
    
    def __init__(self):
        self.payment_methods = {
            PaymentMethod.STRIPE: StripePaymentHandler(),
            PaymentMethod.ORANGE_MONEY: MobileMoneyHandler("Orange Money"),
            PaymentMethod.MTN_MONEY: MobileMoneyHandler("MTN Money"),
            PaymentMethod.MOOV_MONEY: MobileMoneyHandler("Moov Money"),
            PaymentMethod.TRESOR_MONEY: TresorMoneyHandler(),
            PaymentMethod.BANK_TRANSFER: BankTransferHandler(),
        }
    
    async def initiate_payment(
        self,
        method: PaymentMethod,
        amount: float,
        currency: str,
        user_data: Dict[str, Any],
        package_data: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Initie un paiement avec la méthode spécifiée"""
        
        if method not in self.payment_methods:
            raise ValueError(f"Méthode de paiement non supportée: {method}")
        
        handler = self.payment_methods[method]
        
        try:
            result = await handler.process_payment(
                amount=amount,
                currency=currency,
                user_data=user_data,
                package_data=package_data,
                **kwargs
            )
            return result
        except Exception as e:
            logger.error(f"Error processing {method} payment: {str(e)}")
            raise

class StripePaymentHandler:
    """Gestionnaire Stripe (déjà implémenté)"""
    async def process_payment(self, **kwargs):
        # Déjà implémenté dans candidate_routes.py
        return {"type": "redirect", "method": "stripe"}

class MobileMoneyHandler:
    """Gestionnaire générique Mobile Money (Orange, MTN, Moov)"""
    
    def __init__(self, provider_name: str):
        self.provider_name = provider_name
    
    async def process_payment(
        self,
        amount: float,
        currency: str,
        user_data: Dict[str, Any],
        package_data: Dict[str, Any],
        phone_number: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Traite un paiement Mobile Money
        
        Note: En production, intégrer avec l'API réelle du provider
        Pour le moment, retourne des instructions de paiement manuel
        """
        
        transaction_id = f"MM-{str(uuid.uuid4())[:8]}"
        
        # Générer code de paiement
        payment_code = f"*144*4*6*{transaction_id[-6:]}#"
        
        # Instructions selon le provider
        instructions = self._get_payment_instructions(amount, currency, transaction_id)
        
        return {
            "type": "ussd",
            "method": self.provider_name.lower().replace(' ', '_'),
            "transaction_id": transaction_id,
            "status": PaymentStatus.PENDING,
            "instructions": instructions,
            "payment_code": payment_code,
            "amount": amount,
            "currency": currency,
            "expires_in": 900,  # 15 minutes
            "phone_number": phone_number
        }
    
    def _get_payment_instructions(self, amount: float, currency: str, transaction_id: str) -> Dict[str, Any]:
        """Génère les instructions de paiement"""
        
        if "Orange" in self.provider_name:
            return {
                "title": "Paiement Orange Money",
                "steps": [
                    "Composez *144# sur votre téléphone",
                    "Sélectionnez 'Paiement Marchand'",
                    "Entrez le code marchand: OSNER225",
                    f"Montant: {amount:,.0f} {currency}",
                    f"Référence: {transaction_id}",
                    "Validez avec votre code PIN"
                ],
                "alternative": "Ou envoyez le montant au numéro: +225 07 07 592 286"
            }
        elif "MTN" in self.provider_name:
            return {
                "title": "Paiement MTN Money",
                "steps": [
                    "Composez *133# sur votre téléphone",
                    "Sélectionnez 'Payer un marchand'",
                    "Entrez le code: OSNER225",
                    f"Montant: {amount:,.0f} {currency}",
                    f"Référence: {transaction_id}",
                    "Confirmez avec votre code secret"
                ],
                "alternative": "Ou transférez au: +225 05 44 498 515"
            }
        else:  # Moov Money
            return {
                "title": "Paiement Moov Money",
                "steps": [
                    "Composez *155# sur votre téléphone",
                    "Sélectionnez 'Paiement'",
                    "Choisissez 'Marchand'",
                    "Code marchand: OSNER225",
                    f"Montant: {amount:,.0f} {currency}",
                    f"Référence: {transaction_id}",
                    "Validez avec votre code PIN"
                ],
                "alternative": "Contact: +225 07 07 592 286"
            }

class TresorMoneyHandler:
    """Gestionnaire Trésor Money (Poste Côte d'Ivoire)"""
    
    async def process_payment(
        self,
        amount: float,
        currency: str,
        user_data: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        
        transaction_id = f"TM-{str(uuid.uuid4())[:8]}"
        
        return {
            "type": "tresor_money",
            "method": "tresor_money",
            "transaction_id": transaction_id,
            "status": PaymentStatus.PENDING,
            "instructions": {
                "title": "Paiement Trésor Money",
                "steps": [
                    "Rendez-vous dans un bureau de poste",
                    "Demandez un paiement Trésor Money",
                    "Bénéficiaire: OSNER-GROUP",
                    f"Montant: {amount:,.0f} {currency}",
                    f"Référence: {transaction_id}",
                    "Conservez votre reçu de paiement"
                ],
                "note": "Envoyez une photo du reçu par WhatsApp au +225 07 07 592 286"
            },
            "amount": amount,
            "currency": currency
        }

class BankTransferHandler:
    """Gestionnaire virement bancaire"""
    
    async def process_payment(
        self,
        amount: float,
        currency: str,
        user_data: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        
        transaction_id = f"BT-{str(uuid.uuid4())[:8]}"
        
        return {
            "type": "bank_transfer",
            "method": "bank_transfer",
            "transaction_id": transaction_id,
            "status": PaymentStatus.PENDING,
            "bank_details": {
                "beneficiary": "OSNER-GROUP SARL",
                "bank": "Banque Atlantique Côte d'Ivoire",
                "iban": "CI93 CI 01 234567890123456789 01",
                "swift": "ATCICIX",
                "account_number": "01234567890",
                "reference": transaction_id,
                "amount": f"{amount:,.0f} {currency}"
            },
            "instructions": {
                "title": "Virement Bancaire",
                "steps": [
                    "Effectuez un virement vers notre compte bancaire",
                    "Utilisez OBLIGATOIREMENT la référence indiquée",
                    "Le traitement prend 24-48h ouvrées",
                    "Vous recevrez une confirmation par email"
                ],
                "note": "Conservez votre bordereau de virement"
            },
            "amount": amount,
            "currency": currency
        }