"""pos_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pos import views

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('',views.LoginFormView.as_view(),name='signin'),
    path('register/',views.SignupView.as_view(),name='register'),
    path('home/',views.HomeView.as_view(),name='home'),
    path('logout/',views.signout_view,name='signout'),
    path('category/',views.CategoryView.as_view(),name='category'),
    path('products/',views.ProductView.as_view(),name='products'),
    path('pos/',views.POSView.as_view(),name='pos'),
    path('bill/',views.BillView.as_view(),name='bill'),
    path('sales/saveall',views.SalesSaveView.as_view(),name='sales_saveall'),
    path('delete/<int:id>',views.SalesDeleteView.as_view(),name='sales_delete'),
    # path('sales/<int:id>',views.sales_view,name='sales'),
    path('sales/',views.SalesDetailView.as_view(),name='sales_details'),
    path('sales/delete/<int:id>',views.TransactionDeleteView.as_view(),name='t_delete'),
    path('products/<int:id>',views.ProductUpdateView.as_view(),name='edit_product'),
    path('category/<int:id>',views.CategoryUpdateView.as_view(),name='edit_category'),
    path('products/<int:id>/delete',views.ProductDeleteView.as_view(),name='delete_product'),
    path('category/<int:id>/delete',views.CategoryDeleteView.as_view(),name='delete_category'),    
    path('sales-report/',views.sales_report,name='sales_report'),
    path('sales/delete/',views.SalesAllDeleteView.as_view(),name='sales_deleteall'),
    path('pos/delete',views.SalesItemDeleteView.as_view(),name='salesitem_deleteall'),
]
