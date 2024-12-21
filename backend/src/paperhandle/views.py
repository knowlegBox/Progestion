import datetime
import pandas as pd
from django.db.models import Sum, Prefetch, F
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from weasyprint import HTML

from customers.models import Customer
from product.models import Product, VenteJournaliere
from transactions.models import Versement


def dette_clients():
    # Précharger les versements associés aux clients, triés par date décroissante
    versements_prefetch = Prefetch('client_versmt',
                                   queryset=Versement.objects.order_by('-date'),
                                   to_attr='dernier_versment')

    # Récupérer les clients avec un solde supérieur à 0 et leurs derniers versements
    clients = Customer.objects.filter(solde__gt=0).prefetch_related(versements_prefetch)

    # Créer une liste contenant les informations du client, son dernier versement et le montant
    clients_dette = []
    for client in clients:
        # Récupérer le dernier versement du client (s'il existe)
        dernier_versement = client.dernier_versment[0] if client.dernier_versment else None

        # Extraire la date et le montant du dernier versement
        date_dernier_versement = dernier_versement.date if dernier_versement else None
        montant_dernier_versement = dernier_versement.amount if dernier_versement else None

        # Ajouter les informations dans la liste
        clients_dette.append({
            'name': client.name,
            'prenom': client.prenom,
            'solde': client.solde,
            'date_dernier_versement': date_dernier_versement,
            'montant_dernier_versement': montant_dernier_versement
        })

    return clients_dette


def inventaire():
    product_list = Product.objects.only("name", "quantity").filter(quantity__gt=0)
    return product_list


def ventes_par_mois_pandas(request):
    # Récupérer les données depuis la base
    ventes = VenteJournaliere.objects.select_related('product').values(
        'product__name', 'date', 'quantity', 'totalprice'
    )
    dette_client = dette_clients()
    print(dette_client)
    inventory = inventaire()

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
    context = {'solds': ventes_dict,
               "dette_client": dette_client,
               "inventory": inventory
               }
    html = render(request, 'pdf/ventes_par_mois.html',
                  context).content.decode("utf-8")
    pdf = HTML(string=html).write_pdf()
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Dispostion"] = "attachment; filename=rapport mensuel.pdf"
    return response


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


#####################################################
def sold_per_month(request):
    solds = VenteJournaliere.objects.annotate(
        mois=TruncMonth('add_date')
    ).values('product', 'mois').annotate(
        total_quantite=Sum('quantity'),
        total_montant=Sum('totalprice')
    ).order_by('product__name', 'mois')
    context = {'solds': solds}
    html_content = render(request, 'pdf/ventes_par_mois.html', context).content.decode("utf-8")
    pdf_file = HTML(string=html_content).write_pdf()
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Dispostion"] = "inline; filename=mon rapport.pdf"
    return response


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
