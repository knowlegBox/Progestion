"""from django.shortcuts import get_object_or_404

from product.models import Product


def command_product(product, sold_day, status, user):
    all_product = []
    # product = product[0]
    product_list = product.split(";")
    for element in product_list:
        one_prod = element.split(",")
        product_search(one_prod)
        all_product.append(one_prod)
    print(all_product)
    # return all_product


def product_search(prod):
    product = get_object_or_404(Product, name=prod[0])
    if prod[2]:
        print("prod[2]:", product.name, ":", product.price)

    else:
        print("pas de prod[2]", product.name, ":", product.price)
"""
import datetime

from django.db.models import Sum

from customers.models import Customer
from product.models import VenteJournaliere


# from django.db.models import Sum, F
#
# from customers.models import Customer
# from product.models import Category, VenteJournaliere
# import pandas as pd
#
#
# data = pd.read_excel("data.xls")
# print(data.head(100))

















def invoice_number(last_number=datetime.date.today()):
    number = str(last_number).split("-")
    increment_number = number[2]
    compresse_date = number[1]
    date = datetime.date.today()
    date_list = str(date).split("-")
    string_date = "".join(date_list[::-1])
    if compresse_date == string_date:
        increment_number = int(increment_number) + 1
        return f"BC-{string_date}-0{increment_number}"
    return f"BC-{string_date}-01"


def new_hold_compare(new, hold):
    """
    :param new: new value came from submit form
    :param hold: hold value came from database
    :return: bool
    """
    if new > hold:
        return False
    return True


def dette_client():
    total_invoice = []
    client_endte = []
    all_customer = Customer.objects.all()
    for customer in all_customer:
        invoice = customer.custom_invoice.aggregate(total=Sum("total_price"))["total"] or 0
        versmt = customer.versement_set.aggregate(total=Sum("amount"))["total"] or 0

        reste = invoice - versmt
        # print(f"versmt: {versmt} invoice {invoice} reste: {reste}")
        if invoice or versmt:
            client_endte.append({"customer": customer, "reste": reste})

        total_invoice.append(reste)
    return sum(total_invoice), client_endte, all_customer


def vente_mensuelle():
    """
        return: categorie and associate product the quantity and the price
    """
    current_month = f"{datetime.datetime.now().month}"
    # month_solde_quantity = VenteJournaliere.objects.filter(add_date__month=current_month).aggregate(total=Sum("quantity"))["total"]
    # month_solde_price = VenteJournaliere.objects.filter(add_date__month=current_month).aggregate(total=Sum("price"))["total"]
    # print(month_solde_quantity)
    # # sale_by_category = VenteJournaliere.objects.filter(add_date__month=current_month).values("product__category__name", "product__name").annotate(total_quantity=Sum("quantity")).order_by("product__category__name")
    # sales_by_category = VenteJournaliere.objects.filter(add_date__month=current_month) \
    #     .values('product__category__name', 'product__name') \
    #     .annotate(total_quantity=Sum('quantity')) \
    #     .order_by('product__category__name')
    # print(sales_by_category)
    month_solde_price = VenteJournaliere.objects.filter(add_date__month=current_month).aggregate(total=Sum("totalprice"))["total"]
    print(month_solde_price)


import logging
import time

# Configuration du logger
logging.basicConfig(
    filename='execution_time.log',  # Nom du fichier de log
    level=logging.INFO,  # Niveau de log
    format='%(asctime)s - %(message)s',  # Format des messages de log
)


def log_execution_time(func):
    """
    Décorateur pour mesurer et enregistrer le temps d'exécution d'une fonction.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()  # Début du chronométrage
        result = func(*args, **kwargs)
        end_time = time.time()  # Fin du chronométrage

        execution_time = end_time - start_time
        logging.info(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds.")
        return result

    return wrapper
