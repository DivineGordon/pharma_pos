from django import forms
from .models import Sales, StockedItem,Product,Sale


class SaleForm(forms.ModelForm):
    def save(self,**kwargs):
        instance=super().save(commit=False)
        product=instance.product
        product.stock_quantity-=instance.quantity
        product.save()
        instance.save()
        return instance
        
    def clean_quantity(self):
        product,form_quantity=self.cleaned_data['product'],self.cleaned_data['quantity']
        if form_quantity <= 0:
            raise forms.ValidationError("order quantity cannot be zero %(value)",
            params={'value':product.product_name}, code="INV_PURCHASE_QTY")
        if form_quantity > product.stock_quantity:
            raise forms.ValidationError("order quantity %(o_qty) is more than available stock %(a_qty) for %(value)",
            params={'value':product.product_name,
            'o_qty':form_quantity ,'a_qty':product.stock_quantity},
            code="INV_PURCHASE_QTY")
        return form_quantity

    def clean_amount(s):
        product,form_quantity,form_amount=(s.cleaned_data.get('product'),
        s.cleaned_data.get('quantity'),s.cleaned_data.get('amount'))
        if form_quantity and product:
            calc_amount=product.price*form_quantity
            if calc_amount != form_amount:
                raise forms.ValidationError("invalid purchase amount for %(value)",
                params={'value',product.product_name}) 
        return form_amount
    class Meta:
        model=Sale
        fields=('product','quantity','amount')

class SalesForm(forms.ModelForm):
    class  Meta:
        model=Sales
        fields=('amount',)
    def clean(self):
        amount=self.cleaned_data.get('amount')
        if amount and amount<=0:
            raise forms.ValidationError('total amount must be above 0.00')
        secondary_forms=self.secondary_forms
        if not secondary_forms.is_valid():
            raise forms.ValidationError("invalid data")
        total=0
        for form in secondary_forms:
            sub_total=form.cleaned_data.get('amount')
            if sub_total is None:
                raise forms.ValidationError("invalid total")
            total+=sub_total
        else:
            if total != amount:
                raise forms.ValidationError("invalid total")
        return super().clean()
    def save(self,**kwargs):
        instance=super().save(commit=False)
        instance.contact_person=self.request_class.user
        instance.save()
        secondary_forms=self.secondary_forms
        for form in secondary_forms:
            form.instance.unit_price=form.instance.product.price
            form.instance.sales_record=instance
        else:
            secondary_forms.save()
        return instance



    
class StockForm(forms.ModelForm):
    product=forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model=StockedItem
        fields=('product','unit_quantity','package_quantity','unit_price',
        'package_price','location')

class ProductViewForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=('product_name','brand_name','unit_quantity','package_quantity')