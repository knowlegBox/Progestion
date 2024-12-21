# import openpyxl
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from customers.models import Customer
from facture.models import MyInvoice
from mysearches.forms import UploadFileForm
from product.models import Product
from supplier.models import SupplierInvoices, Supplier


# Create your views here.
# def invoice_search_supplier(request):
#     my_keyword = request.POST.get("search-supplier")
#     try:
#         search_supplier = int(my_keyword)
#         supplier_invoice = SupplierInvoices.objects.filter(
#             Q(number__icontains=search_supplier) | Q(total_price__icontains=search_supplier)
#         )
#         print(supplier_invoice)
#         return render(request, "search_invoice_supplier.html", {"supplier": supplier_invoice})
#     except ValueError as E:
#         supplier_invoice_liste = []
#         suppliers= Supplier.objects.filter(
#             Q(name__icontains=my_keyword)
#         )
#         for supplier in suppliers:
#             supplier_in = supplier.supplier_invoice.all()
#             supplier_invoice_liste.append(supplier_in)
#         return render(request, "search_invoice_supplier.html", {"supplier": supplier_invoice_liste})
#
#     # return HttpResponse("bad response", status=405)


def invoice_search_supplier(request):
    my_keyword = request.POST.get("search-supplier")

    if my_keyword.isdigit():  # If the keyword is numeric (e.g., invoice number or price)
        try:
            search_supplier = int(my_keyword)
            supplier_invoice = SupplierInvoices.objects.filter(
                Q(number__icontains=str(search_supplier)) | Q(total_price__icontains=search_supplier)
            )
            return render(request, "search_invoice_supplier.html", {"supplier": supplier_invoice})
        except ValueError as e:
            # Handle any value error, but this should not occur because `my_keyword` is checked to be numeric
            supplier_invoice_liste = []
            return render(request, "search_invoice_supplier.html", {"supplier": supplier_invoice_liste})

    else:  # If the keyword is not numeric, search by supplier name
        supplier_invoice_liste = []

        # Search suppliers by name
        suppliers = Supplier.objects.filter(name__icontains=my_keyword)

        for supplier in suppliers:
            # For each supplier, find related invoices
            supplier_invoices = supplier.supplier_invoice.all()  # Get related SupplierInvoices via the related_name
            supplier_invoice_liste.extend(supplier_invoices)  # Add all invoices to the list

        return render(request, "search_invoice_supplier.html", {"supplier": supplier_invoice_liste})


def invoice_search_client(request):
    my_keyword = request.POST.get("search-client")
    if my_keyword.isdigit():
        try:
            seach_client = int(my_keyword)
            client_invoice =  MyInvoice.objects.filter(
            Q(number__icontains=str(seach_client)) | Q(total_price__icontains=seach_client))
            return render(request, "search_invoice_client.html", {"client": client_invoice})
        except ValueError as e:
            client_invoice_liste = []
            return render(request, "search_invoice_client.html", {"client": client_invoice_liste})
    else:
        client_invoice_liste = []
        clients = Customer.objects.filter(name__icontains=my_keyword)
        for client in clients:
            client_invoices = client.custom_invoice.all()
            client_invoice_liste.extend(client_invoices)
        return render(request, "search_invoice_client.html", {"client": client_invoice_liste})


def product_search(request):
    product = request.POST.get("search")
    produit = Product.objects.filter(Q(name__icontains=product))[:10]
    return render(request, "invoice_partial.html", context={"products": produit})


def product_list_seach(request):
    product = request.POST.get("search")
    produit = Product.objects.filter(Q(name__icontains=product))[:10]
    return render(request, "prod/partial/product_list.html", context={"product": produit})

# def upload_products(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = request.FILES['file']
#             try:
#                 wb = openpyxl.load_workbook(file)
#                 sheet = wb.active
#
#                 for row in sheet.iter_rows(min_row=10, values_only=True):
#                     category, products, unity, price, quantity = row
#                     print("row:", row)
#                     product, created = Product.objects.get_or_create(
#                         name=products,
#                         defaults={
#                             "category": category,
#                             "product": products,
#                             "unity": unity,
#                             "price": price,
#                             "quantity": quantity,
#                         }
#                     )
#                     if not created:
#                         product.price = price
#                         product.quantity = quantity
#
#                         product.save()
#                 messages.success(request, 'Products imported successfully!')
#             except Exception as e:
#                 messages.error(request, f'Error importing products: {e}')
#             return redirect('product:liste')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload_products.html', {'form': form})
# def upload_products(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = request.FILES['file']
#             try:
#                 wb = openpyxl.load_workbook(file)
#                 sheet = wb.active
#
#                 for row in sheet.iter_rows(min_row=2, values_only=True):
#                     row_data = [cell if cell is not None else '' for cell in row]
#                     if len(row_data) >= 5:
#                         category, products, unity, price, quantity = row_data[:5]
#                         print("row:", row_data[:5])
#                         product, created = Product.objects.get_or_create(
#                             name=products,
#                             defaults={
#                                 "category": product.category,
#                                 "product": product.pk,
#                                 "unity": unity,
#                                 "price": price,
#                                 "quantity": quantity,
#                             }
#                         )
#                         print()
#                         if not created:
#                             product.price = price
#                             product.quantity = quantity
#                             product.save()
#                 messages.success(request, 'Products imported successfully!')
#             except Exception as e:
#                 messages.error(request, f'Error importing products: {e}')
#             return redirect('product:liste')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload_products.html', {'form': form})
