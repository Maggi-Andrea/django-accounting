from django.forms import ModelForm, BaseInlineFormSet
from django.forms.models import inlineformset_factory

from .models import (
    Organization,
    Invoice,
    InvoiceLine,
    Bill,
    BillLine)


class RequiredInlineFormSet(BaseInlineFormSet):
    """
    Used to make empty formset forms required
    See http://stackoverflow.com/questions/2406537/django-formsets-\
        make-first-required/4951032#4951032
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.forms) > 0:
            first_form = self.forms[0]
            first_form.empty_permitted = False


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = (
            "display_name",
            "legal_name",
        )


class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = (
            "number",
            "organization",
            "client",

            "draft",
            "sent",
            "paid",
            "date_issued",
            "date_paid",
        )


class InvoiceLineForm(ModelForm):
    class Meta:
        model = InvoiceLine
        fields = (
            "label",
            "description",
            "unit_price",
            "quantity",
        )


InvoiceLineFormSet = inlineformset_factory(Invoice,
                                           InvoiceLine,
                                           form=InvoiceLineForm,
                                           formset=RequiredInlineFormSet,
                                           extra=1)
