



# myapp/views.py
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from product.models import Product


# Assurez-vous d'importer votre modèle

def generate_pdf(request):
    # Création d'un objet HttpResponse avec le type de contenu approprié
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # Création d'un document PDF
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    # En-tête
    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Ajout de l'en-tête avec le logo et le nom de l'entreprise
    # c.drawImage('path/to/logo.png', 40, height - 80, width=2*inch, preserveAspectRatio=True)  # Changez le chemin de l'image
    c.setFont("Helvetica-Bold", 16)
    c.drawString(3*inch, height - 50, "Nom de l'entreprise")

    # Pied de page
    c.setFont("Helvetica", 10)
    footer_text = "Informations sur l'entreprise - Adresse, Téléphone, Email"
    c.drawString(40, 30, footer_text)

    # Données du tableau
    items = Product.objects.all()
    data = [["Nom", "Quantité", "Unité", "Prix", "Date"]]  # En-têtes
    total_general = 0

    for item in items:
        data.append([item.name, item.quantity, item.unity, item.price, item.date.strftime('%d-%m-%Y')])
        total_general += item.price

    # Ajouter le total général
    data.append(["", "", "", "Total", total_general])

    # Création du tableau
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    # Finalisation du document PDF
    doc.build(elements)

    return response


import datetime
import openpyxl
import pandas as pd
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from weasyprint import HTML

from product.models import Product, VenteJournaliere


def pdf_generator(request):
    product = Product.objects.only("category",
                                   "name",
                                   "quantity",
                                   "price", )
    context = {"produits": product}
    # Rendre le template HTML avec les données
    html_content = render(request, "pdf/pdf_template.html", context).content.decode("utf-8")

    pdf_file = HTML(string=html_content).write_pdf()
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Dispostion"] = f"inline; filename= rapport du {datetime.datetime.today()}.pdf"
    return response


def sold_per_month(request):
    solds = VenteJournaliere.objects.annotate(
        mois=TruncMonth('add_date')
    ).values('product', 'mois').annotate(
        total_quantite=Sum('quantity'),
        total_montant=Sum('totalprice')
    ).order_by('product', 'mois')
    context = {'solds': solds}
    html_content = render(request, 'pdf/ventes_par_mois.html', context).content.decode("utf-8")
    pdf_file = HTML(string=html_content).write_pdf()
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Dispostion"] = "inline; filename=mon rapport.pdf"
    return response


def ventes_par_mois_pandas(request):
    # Récupérer les données depuis la base
    ventes = VenteJournaliere.objects.select_related('product').values(
        'product__name', 'date', 'quantity', 'totalprice'
    )

    # Convertir les données en DataFrame Pandas
    df = pd.DataFrame(ventes)

    # Vérifier si le DataFrame contient des données
    if not df.empty:
        # Convertir la colonne 'date' en datetime
        df['date'] = pd.to_datetime(df['date'])

        # Extraire le mois et l'année
        df['mois_annee'] = df['date'].dt.to_period('M')

        # Grouper par produit et mois_annee et calculer les totaux
        vue = df.groupby(['product__name', 'mois_annee']).agg(
            total_quantite=('quantity', 'sum'),
            total_montant=('totalprice', 'sum')
        ).reset_index()

        # Renommer les colonnes pour un affichage plus clair
        vue.rename(columns={'product__name': 'produit', 'mois_annee': 'mois'}, inplace=True)
    else:
        # Si aucun enregistrement, créer un DataFrame vide
        vue = pd.DataFrame(columns=['produit', 'mois', 'total_quantite', 'total_montant'])

    # Convertir le DataFrame en dictionnaire pour le passer au template
    ventes_dict = vue.to_dict('records')

    return render(request, 'pdf/ventes_par_mois.html', {'solds': ventes_dict})


def file_data(request):
    if request.method == "POST" and request.FILES.get("excel_file"):
        excel_file = request.FILES["excel_file"]
        try:
            df = pd.read_excel(excel_file)

            colonnes_requises = {'Category', 'Product', 'Price', 'Quantity', 'unity'}
            print(df.columns)
            if not colonnes_requises.issubset(df.columns):
                return JsonResponse({
                    "success": False,
                    "message": f"Colonnes requises manquantes. Attendu : {', '.join(colonnes_requises)}"
                })
            produit_bulk = [
                Product(
                    name=row["Product"],
                    price=row["Price"],
                    quantity=row["Quantity"],
                    unity=row["unity"]
                ) for _, row in df.iterrows()
                if not Product.objects.filter(name=row["Product"]).exists()
            ]
            if produit_bulk:
                Product.objects.bulk_create(produit_bulk)
                return JsonResponse({"success": True, "message": f"{len(produit_bulk)} produits importés avec succès."})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Erreur lors de l'import : {str(e)}"})
    return render(request, "data/importer_produits.html")
