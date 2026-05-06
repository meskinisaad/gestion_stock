from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from io import BytesIO
from datetime import datetime
from django.db.models import Sum, Q
from produits.models import Produit
from stock.models import MouvementStock, SuggestionReapprovisionnement


def generer_rapport_valorisation_pdf():
    """Génère un rapport de valorisation du stock en PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4e78'),
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1f4e78'),
        spaceAfter=12,
    )
    
    # En-tête
    elements.append(Paragraph("RAPPORT DE VALORISATION DU STOCK", title_style))
    elements.append(Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 0.3 * inch))
    
    # Données produits
    produits = Produit.objects.all()
    valorisation_total = sum(p.valorisation_stock() for p in produits)
    
    data = [
        ['Produit', 'Quantité', 'Prix Unitaire', 'Valeur Totale', '% du Stock']
    ]
    
    for produit in sorted(produits, key=lambda p: p.valorisation_stock(), reverse=True):
        valeur = produit.valorisation_stock()
        pourcentage = (valeur / valorisation_total * 100) if valorisation_total > 0 else 0
        data.append([
            produit.nom[:30],
            str(produit.quantite),
            f"{produit.prix:.2f}DH",
            f"{valeur:.2f}DH",
            f"{pourcentage:.1f}%",
        ])
    
    # Ajouter total
    data.append(['', '', 'TOTAL', f"{valorisation_total:.2f}DH", '100%'])
    
    # Tableau
    table = Table(data, colWidths=[2*inch, 1*inch, 1.2*inch, 1.2*inch, 1.3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e78')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.grey),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f0f0f0')]),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3 * inch))
    
    # Résumé
    elements.append(Paragraph("RÉSUMÉ FINANCIER", heading_style))
    summary_data = [
        ['Valorisation Totale du Stock', f"{valorisation_total:.2f} DH"],
        ['Nombre de Produits', str(produits.count())],
        ['Valeur Moyenne par Produit', f"{valorisation_total / produits.count():.2f} DH" if produits.count() > 0 else "N/A"],
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(summary_table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer


def generer_rapport_mouvements_pdf(jours=30):
    """Génère un rapport des mouvements de stock en PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=0.5*inch, leftMargin=0.5*inch)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1f4e78'),
        spaceAfter=20,
        alignment=TA_CENTER,
    )
    
    # En-tête
    elements.append(Paragraph("RAPPORT DES MOUVEMENTS DE STOCK", title_style))
    elements.append(Paragraph(f"Période : {jours} derniers jours | Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Données mouvements
    from django.utils import timezone
    from datetime import timedelta
    date_debut = timezone.now() - timedelta(days=jours)
    mouvements = MouvementStock.objects.filter(date__gte=date_debut).order_by('-date')
    
    data = [
        ['Date', 'Produit', 'Type', 'Quantité', 'Utilisateur']
    ]
    
    for mv in mouvements[:100]:  # Limiter à 100 lignes
        data.append([
            mv.date.strftime('%d/%m/%Y %H:%M'),
            mv.produit.nom[:25],
            mv.get_type_display(),
            str(mv.quantite),
            mv.utilisateur.username if mv.utilisateur else 'Système',
        ])
    
    table = Table(data, colWidths=[1.2*inch, 2*inch, 0.8*inch, 0.8*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e78')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))
    
    elements.append(table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer


def generer_rapport_suggestions_pdf():
    """Génère un rapport des suggestions de réapprovisionnement en PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1f4e78'),
        spaceAfter=20,
        alignment=TA_CENTER,
    )
    
    # En-tête
    elements.append(Paragraph("RAPPORT DE RÉAPPROVISIONNEMENT", title_style))
    elements.append(Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Suggestions en attente
    suggestions = SuggestionReapprovisionnement.objects.filter(traitee=False).order_by('-priorite')
    
    # Compteurs par priorité
    elements.append(Paragraph("RÉSUMÉ", styles['Heading2']))
    summary_data = [
        ['Priorité', 'Nombre'],
        ['CRITIQUE', str(suggestions.filter(priorite='CRITIQUE').count())],
        ['HAUTE', str(suggestions.filter(priorite='HAUTE').count())],
        ['NORMALE', str(suggestions.filter(priorite='NORMALE').count())],
        ['BASSE', str(suggestions.filter(priorite='BASSE').count())],
    ]
    
    summary_table = Table(summary_data, colWidths=[2*inch, 1*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d32f2f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3 * inch))
    
    # Détails des suggestions
    elements.append(Paragraph("DÉTAILS DES SUGGESTIONS", styles['Heading2']))
    elements.append(Spacer(1, 0.1 * inch))
    
    data = [
        ['Produit', 'Quantité Suggérée', 'Priorité', 'Raison', 'Fournisseur']
    ]
    
    for suggestion in suggestions:
        data.append([
            suggestion.produit.nom[:20],
            str(suggestion.quantite_suggeree),
            suggestion.get_priorite_display(),
            suggestion.raison[:15],
            suggestion.produit.fournisseur.nom[:15],
        ])
    
    if len(data) > 1:
        table = Table(data, colWidths=[1.2*inch, 1.2*inch, 0.9*inch, 1.2*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e78')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("Aucune suggestion en attente.", styles['Normal']))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer


def generer_rapport_produits_expires_pdf():
    """Génère un rapport des produits expirés en PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#c62828'),
        spaceAfter=20,
        alignment=TA_CENTER,
    )
    
    # En-tête
    elements.append(Paragraph("RAPPORT PÉREMPTION & OBSOLESCENCE", title_style))
    elements.append(Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 0.2 * inch))
    
    from django.utils import timezone
    produits = Produit.objects.all()
    
    # Produits expirés
    elements.append(Paragraph("PRODUITS EXPIRÉS", styles['Heading2']))
    produits_expires = [p for p in produits if p.est_expire()]
    
    if produits_expires:
        data = [['Produit', 'Date Expiration', 'Quantité', 'Catégorie']]
        for p in produits_expires:
            data.append([
                p.nom[:25],
                p.date_expiration.strftime('%d/%m/%Y') if p.date_expiration else 'N/A',
                str(p.quantite),
                p.categorie.nom,
            ])
        
        table = Table(data, colWidths=[2.5*inch, 1.5*inch, 1*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#c62828')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("Aucun produit expiré.", styles['Normal']))
    
    elements.append(Spacer(1, 0.2 * inch))
    
    # Produits obsolètes
    elements.append(Paragraph("PRODUITS OBSOLÈTES", styles['Heading2']))
    produits_obsoletes = produits.filter(statut_obsolescence__in=['OBSOLETE', 'DISCONTINU'])
    
    if produits_obsoletes.exists():
        data = [['Produit', 'Statut', 'Date Obsolescence', 'Quantité']]
        for p in produits_obsoletes:
            data.append([
                p.nom[:25],
                p.get_statut_obsolescence_display(),
                p.date_obsolescence.strftime('%d/%m/%Y') if p.date_obsolescence else 'N/A',
                str(p.quantite),
            ])
        
        table = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f57c00')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("Aucun produit obsolète.", styles['Normal']))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
