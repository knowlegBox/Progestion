from facture.models import MyInvoice


def last_invoice_id(resquest):
    try:
        return {"my_invoice": MyInvoice.get_last_id()}
    except Exception as E:
        print("last_invoice_id: ", E)
        return {"my_invoice": ""}

