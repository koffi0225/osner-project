from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import qrcode
import io
import os
from pathlib import Path

class ReceiptGenerator:
    """Générateur de reçus PDF pour les paiements"""
    
    def __init__(self):
        self.output_dir = Path("/app/receipts")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_qr_code(self, data: str) -> io.BytesIO:
        """Génère un QR code"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to BytesIO
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return img_io
    
    def generate_receipt(
        self,
        user_data: dict,
        payment_data: dict,
        package_data: dict
    ) -> str:
        """
        Génère un reçu PDF
        
        Args:
            user_data: {nom, prenom, sexe, email, code_inscription}
            payment_data: {transaction_id, amount, currency, payment_method, date}
            package_data: {name, credits, description}
        
        Returns:
            str: Chemin du fichier PDF généré
        """
        # Nom du fichier
        filename = f"recu_{user_data['code_inscription']}_{payment_data['transaction_id'][:8]}.pdf"
        filepath = self.output_dir / filename
        
        # Créer le document
        doc = SimpleDocTemplate(str(filepath), pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Styles personnalisés
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#DC2626'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#0F172A'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#475569'),
            alignment=TA_LEFT
        )
        
        # Header avec logo (utiliser texte si pas de logo)
        story.append(Paragraph("<b>OSNER-GROUP</b>", title_style))
        story.append(Paragraph("Plateforme Actualité, Formation & Emploi", normal_style))
        story.append(Paragraph("Abidjan, Côte d'Ivoire", normal_style))
        story.append(Paragraph("Tél: +225 07 07 592 286 | +225 05 44 498 515", normal_style))
        story.append(Spacer(1, 0.5*cm))
        
        # Ligne de séparation
        story.append(Paragraph("_" * 100, normal_style))
        story.append(Spacer(1, 0.5*cm))
        
        # Titre du reçu
        story.append(Paragraph("<b>REÇU DE PAIEMENT</b>", heading_style))
        story.append(Spacer(1, 0.3*cm))
        
        # Informations du reçu
        receipt_info = [
            ["N° Reçu:", payment_data['transaction_id']],
            ["Date:", payment_data['date'].strftime("%d/%m/%Y %H:%M")],
            ["Méthode:", payment_data['payment_method']]
        ]
        
        receipt_table = Table(receipt_info, colWidths=[5*cm, 10*cm])
        receipt_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#475569')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(receipt_table)
        story.append(Spacer(1, 0.5*cm))
        
        # Informations client
        story.append(Paragraph("<b>INFORMATIONS CLIENT</b>", heading_style))
        
        client_info = [
            ["Code d'inscription:", user_data['code_inscription']],
            ["Nom & Prénoms:", f"{user_data['nom']} {user_data['prenom']}"],
            ["Sexe:", user_data['sexe']],
            ["Email:", user_data['email']],
            ["Date d'inscription:", user_data.get('date_inscription', 'N/A')]
        ]
        
        client_table = Table(client_info, colWidths=[5*cm, 10*cm])
        client_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#475569')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(client_table)
        story.append(Spacer(1, 0.5*cm))
        
        # Détails du paiement
        story.append(Paragraph("<b>DÉTAILS DU PAIEMENT</b>", heading_style))
        
        payment_details = [
            ["Package:", package_data['name']],
            ["Description:", package_data.get('description', '')],
            ["Crédits obtenus:", str(package_data['credits'])],
            ["", ""],
            ["Montant:", f"{payment_data['amount']:,.0f} {payment_data['currency']}"],
        ]
        
        payment_table = Table(payment_details, colWidths=[5*cm, 10*cm])
        payment_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#475569')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            # Ligne de séparation
            ('LINEABOVE', (0, 3), (-1, 3), 1, colors.HexColor('#E2E8F0')),
            # Montant en gras
            ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 4), (-1, 4), 12),
            ('TEXTCOLOR', (0, 4), (-1, 4), colors.HexColor('#DC2626')),
        ]))
        story.append(payment_table)
        story.append(Spacer(1, 1*cm))
        
        # QR Code pour vérification
        qr_data = f"OSNER-{user_data['code_inscription']}-{payment_data['transaction_id']}"
        qr_img_io = self.generate_qr_code(qr_data)
        qr_img = Image(qr_img_io, width=3*cm, height=3*cm)
        
        qr_table = Table([["QR Code de vérification:", qr_img]], colWidths=[5*cm, 4*cm])
        qr_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, 0), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ]))
        story.append(qr_table)
        story.append(Spacer(1, 1*cm))
        
        # Footer
        story.append(Paragraph("_" * 100, normal_style))
        story.append(Spacer(1, 0.3*cm))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#94A3B8'),
            alignment=TA_CENTER
        )
        story.append(Paragraph(
            "Ce reçu est généré automatiquement et constitue une preuve de paiement valide.<br/>"
            "Pour toute question, contactez-nous: contact@osner-group.com<br/>"
            "© 2025 Osner-Group. Tous droits réservés.",
            footer_style
        ))
        
        # Générer le PDF
        doc.build(story)
        
        return str(filepath)