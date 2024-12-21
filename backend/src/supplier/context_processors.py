from supplier.models import SupplierInvoices


def last_supplier_invoice(request):
    try:
        return {"supplier_invoice": SupplierInvoices.get_last_id()}
    except Exception as E:
        print("last_supplier_invoice_id: ", E)
        return {"supplier_invoice":""}