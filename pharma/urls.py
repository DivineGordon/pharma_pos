from  django.urls import path

#from .models import Product
from .views import (home,get_js,
PharmaLoginView,PharmaLogoutView,UsersList,
SupplierCreate,CustomerCreate,CustomerDetail,CustomersSearch,
ProductUpdate,ProductDetail,ProductCreate,ProductSearchResult,
StockEntryCreate,StockEntryList,
SalesList,SalesCreate,SalesDetail,ProductSaleTotal
)

urlpatterns=[
    path("user", home,name="check-user"),
    path("users/list/",UsersList.as_view(),name="users-list" ),
    path('accounts/login/',PharmaLoginView.as_view() , name='login'),
     path('accounts/logout/',PharmaLogoutView.as_view() , name='logout'),
    path('js/compiled2.js',get_js),

    path('product/add',ProductCreate.as_view(),name='product-create'),
    path('product/update/<int:pk>/',ProductUpdate.as_view(),name='product-update'),
     path('product/detail/<int:pk>/',ProductDetail.as_view(),name="product-detail"),
     path('product/search/<category>/<search_name>',ProductSearchResult.as_view(),
     name='product-search'),

     path('customer/add',CustomerCreate.as_view(),name='customer-create'),
     path('customer/detail/<int:pk>/',CustomerDetail.as_view(),name="customer-detail"),
     path('customer/search/<category>/<search_name>',CustomersSearch.as_view(),name="customer-search"),
    path('supplier/add',SupplierCreate.as_view(),name='supllier-create'),
   
    path("product/stockentry/add/<int:pk>/",StockEntryCreate.as_view() ,name='stockentry-create'),
    path("product/stockentry/list",StockEntryList.as_view(),name='stockentry-list'),
    #path("product/stockeditem/<int:pk>/",StockedItemDetail.as_view()),

    path("sales/list/",SalesList.as_view(),name='sales-list'),
    path("sales/detail/<int:pk>/",SalesDetail.as_view(),name='sales-detail'),
    path("sales/create",SalesCreate.as_view(),name='sales-create'),
    path("sales/product/list/",ProductSaleTotal.as_view(),name='sales-product-list')

    
]