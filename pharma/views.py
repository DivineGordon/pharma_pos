# Create your views here.

from calendar import month
from dataclasses import dataclass
from django.http import  HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404,get_list_or_404,render
from .models import Product,Supplier,Customer,StockEntry,Sale,Sales
from django.views import generic
from django.views.generic import View ,CreateView,UpdateView,DeleteView,ListView,DetailView
from .forms import SaleForm, StockForm,SalesForm
from  django.utils.cache import patch_cache_control
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
class LazyEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o,Product):
            return o.product_name
        return super().default(o)

class JsonListRender:
    response_class=HttpResponse
    def render_to_response(self,context,**kwargs):
        from django.core import serializers
        kwargs['content_type']='application/json'
        if self.request.GET.get('use_pk'):
            serializer_options={}
        else:
            serializer_options={"use_natural_foreign_keys":True,
        "use_natural_primary_keys":True}
        if context.get('paginator'):
            data=serializers.serialize('json',context['page_obj'],
            **serializer_options)
            response={'data':data}
            response['last_page']=context['paginator'].num_pages
            return JsonResponse(response,**kwargs)
        data_list=self.object_list
        if  self.__dict__.get('psycop2_data') is not None  and len(data_list)==0:
            data_list=self.psycop2_data
            return JsonResponse({'data':data_list,"last_page":1},**kwargs)
        data=serializers.serialize('json',data_list,
        **serializer_options)
        return self.response_class(data,**kwargs)


#login
class PharmaLoginView(LoginView):
    template_name='pharma/registration/login.html'
    def get_context_data(self, **kwargs) :
        context= super().get_context_data(**kwargs)
        context['next']='/static/index.html'
        return context

class PharmaLogoutView(LogoutView):
    next_page='/pharma/accounts/login/?next=/static/index.html'

class  UsersList(JsonListRender,ListView):
    model=User
#user authentication
def home(request):
    if request.user.is_authenticated:
        user=request.user
        data={'username':user.username}
    else:
        data={'username':None}
    return JsonResponse(data)

#get_js
def get_js(req):
    with open(r"C:\Users\Vivien\Documents\gordon work\react-redux\static\pharma\static\output\index.compiled2.js",
    mode='rb') as fd:
        data=fd.read()
        resp=HttpResponse(data,content_type='text/javascript')
        patch_cache_control(resp,max_age=3)
    return resp

#product   
class ProductCreate(CreateView):
    #template_name=product_form.html
    model=Product
    fields=('product_name','brand_name',
    'location','unit_quantity','package_quantity','description','price')
    success_url="/static/index.html"

class ProductUpdate(UpdateView):
    model=Product
    template_name='pharma/product_form_update.html'
    fields=('product_name','brand_name','location','price',
    'description','unit_quantity','package_quantity')
    success_url="/static/index.html"
class ProductDelete(DeleteView):
    model=Product
    #success_url = reverse_lazy('product-deleted')

# Create your views here.
class ProductDetail(DetailView):
    model=Product
    context_object_name='product'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.request.GET.get('caller')=='sales':
            context['sale']=True
        return context
    #def get_object(self):
        #obj=super().get_object()
        #return Product.objects.filter(product_id=self.kwargs['pk'])

#/searching for a product
#/product/search/category/serch_name
class ProductSearchResult( JsonListRender, ListView):
    template_name='pharma/product_search_result.html'
    def get_queryset(self,**kwargs):
        category=self.kwargs['category']
        search_name=self.kwargs['search_name']
        if category=='product_name':
            products=Product.objects.filter(product_name__icontains=search_name)
        elif category=='brand_name':
            products=Product.objects.filter(brand_name__icontains=search_name)
        return products

        
class StockEntryCreate(LoginRequiredMixin, CreateView):
    model=StockEntry
    fields=('stock_quantity','comments','supplier')
    success_url="/static/index.html"
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['product']=Product.objects.get(pk=self.kwargs['pk'])
        return context
    def form_valid(self, form) -> HttpResponse:
        #from django.utils import timezone
        form.instance.person=self.request.user
        #form.instance.date=timezone.now()
        #can youse get_object_or404
        product=Product.objects.get(pk=self.kwargs['pk'])
        product.stock_quantity=product.stock_quantity+form.cleaned_data['stock_quantity']
        product.save()
        form.instance.product=product
        return super().form_valid(form)


class StockEntryList(JsonListRender, ListView):
    model=StockEntry
    paginate_by=12
"""def get_product(request):
    search=request.POST.search
    search_name=request.POST.get('product_name') or request.POST.get('brand_name')
    if search=='product_name':
        products=Product.objects.filter(product_name__icontains=search_name)
    elif search=='brand_name':
        products=Product.objects.filter(brand_name__icontains=search_name)

    stocked_items=get_list_or_404(
        StockedItem,product__in=list(products.values_list('pk',flat=True)))
    context={'stocked_items':stocked_items}
    return render(request,'polls/search.html',context)"""

"""
#edit product
#get product | search product
#/product/stocked_item/<int:pk>
class StockedItemDetail(DetailView):
    template_name='stockedItemDetail.html'
    def get_queryset(self,*args,**kwargs):
        return StockedItem.objects.filter(product_id=self.kwargs['pk'])
class StockedItemList(ListView):
    def get_queryset(self,*args,**kwargs):
        return StockedItem.objects.filter(product_id=self.kwargs['pk'])"""

        
      
#supplier
class SupplierCreate(CreateView):
    model=Supplier
    fields=('company','phone','contact_person','address')
    template_name='pharma/product_form.html'

#Customer
class CustomerCreate(CreateView):                                                                                                              
    model=Customer
    fields=('name','birth_date','phone','identity')
    template_name='pharma/product_form.html'
    success_url='/static/index.html'

class CustomersSearch(JsonListRender, ListView):
    def get_queryset(self,**kwargs):
        category=self.kwargs['category']
        search_name=self.kwargs['search_name']
        if category=='phone':
            customers=Customer.objects.filter(phone__icontains=search_name)
        elif category=='name':
            customers=Customer.objects.filter(name__icontains=search_name)
        return customers

class CustomerDetail(DetailView):
    model=Customer
    def render_to_response(self,context,**kwargs):
        from django.core import serializers
        serializer_options={"use_natural_foreign_keys":True,
        "use_natural_primary_keys":True}
        data=serializers.serialize('json',[self.object],**serializer_options)
        kwargs['content_type']='application/json'
        return HttpResponse(data,**kwargs)
 

#create a stoked item
#/product/stock/create/product_id/product_name
def create_stock(request,product_id,product_name):
    if request.method=='POST':
        data=request.POST.copy()
        data['product']=int(data['product'])     
        form=StockForm(data)
        if form.is_valid():
            form.save()
            return HttpResponse(product_name+" has been successfully saved ")
        else:
            context={'form':form,'product_name':product_name}
            
    else:
        initial={'product':product_id}
        form=StockForm(initial=initial)
        context={'form':form,'product_name':product_name}
    return render(request,'create_stock.html',context)
    

#create a sale
class SalesCreate(CreateView):
    model=Sales
    form_class=SalesForm
    def get_form(self, form_class=None):
        if self.request.method!='POST':
            return super().get_form()
        from .forms import SaleForm
        from django.forms import modelformset_factory
        POST=self.request.POST
        SaleFormSet =modelformset_factory(Sale,form=SaleForm,
        extra=int(POST.get('form-TOTAL_FORMS')))
        saleforms=SaleFormSet(POST)
        form_class = self.get_form_class()
        form_class.secondary_forms=saleforms
        form_class.request_class=self.request
        return super().get_form(form_class)
        #return form_class(secondary_forms=saleforms,**self.get_form_kwargs())
    def form_valid(self, form) -> HttpResponse:
        form.save()
        return HttpResponse("operation successful")
        #from django.views.generic.edit import ModelFormMixin
    def form_invalid(self, form) -> HttpResponse:
        data={'total':form.error.get_json_data(escape=True),
        'lines':form.secondary_forms.errors}
        return JsonResponse(data,status=400)
    
        
    """def post(self,*args,**kwargs):
        from django.core import serializers
        D_objects=serializers.deserialize('json',self.request.body,
        ignorenonexistent=True)
        for d_object in D_objects:
            if isinstance(d_object.object,Sales):
                d_object.save()
                sales_record=d_object.object
                break
        for d_object in D_objects:
            if isinstance(d_object.object,Sales):
                continue
            d_object.object.sales_record=sales_record
            d_object.save()
        return JsonResponse({'status':'successful'})"""


    
    #def form_valid(self, form) -> HttpResponse:
        #from django.views.generic.edit import ModelFormMixin
        #self.object=form.save()
        #todo: save all the sales
        #return super().form_valid(form)
        #return super(ModelFormMixin,self).form_valid(form)


class SaleList(JsonListRender, ListView):
    model=Sale


#see sales list
class SalesList (JsonListRender, ListView): 
    model=Sales
    paginate_by=12
    def get_queryset(self,**kwargs):
        GET=self.request.GET
        user=GET.get('user')
        month=GET.get('month')
        day=GET.get('day')
        filters={}
        if user:
            filters['contact_person_id']=int(user)
        if month:
            filters['date__month']=int(month)
        if day:
            filters['date__day']=int(day)
        if len(filters)==0:
            return super().get_queryset(**kwargs)
        return self.model.objects.filter(**filters)
class SalesDetail(DetailView):
    model=Sales
    #context_object_name='sales'
    def render_to_response(self,context,**kwargs):
        from django.core import serializers
        serializer_options={"use_natural_foreign_keys":True,
        "use_natural_primary_keys":True}
        data={'main':serializers.serialize('json',[self.object],**serializer_options)}
        data['items']=serializers.serialize('json',self.object.sale_set.all(),
        **serializer_options)
        return JsonResponse(data)
import psycopg2

class ProductSaleTotal(JsonListRender, ListView):
    model=Sale
    def get_queryset(self):#-> _SupportsPagination[_M]:
        month=self.request.GET.get('month')
        day=self.request.GET.get('day')
        data=[]
        if not month:
            import datetime
            month=datetime.date.today().month
        if month or day:
            conn=psycopg2.connect("dbname=postgres user=postgres host=localhost")
        else:
            return data
        
        query="""SELECT p.id as PN,p.product_name,s.unit_price,"Total Sales" FROM
        """
        e_q="""
        INNER JOIN pharma_product p ON p.id=s.product_id;
        """
        if month and day:
            query+="""
        ( SELECT product_id,unit_price,SUM(amount) AS "Total Sales"
        FROM pharma_sale
        WHERE EXTRACT(DAY FROM date) = %s 
        AND EXTRACT(MONTH FROM date) = %s  
        GROUP BY product_id,unit_price 
        ORDER BY "Total Sales" DESC ) AS s
        """
            params=(int(day),int(month))
        elif not day and month:
            query+="""
        ( SELECT product_id,unit_price,
        SUM(amount) AS "Total Sales"
         FROM pharma_sale  
        WHERE EXTRACT(MONTH FROM date) = %s 
        GROUP BY product_id,unit_price 
        ORDER BY "Total Sales" DESC) AS s
        """
            params=(int(month),)
        query+=e_q
        with conn:
            with conn.cursor() as  cur:
                cur.execute(query,params)
                data=cur.fetchall()
        self.psycop2_data=data
        return []

#reverse a sale
#see total sales