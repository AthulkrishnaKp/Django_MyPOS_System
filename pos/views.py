from typing import Any
from django.contrib.auth.mixins import UserPassesTestMixin

from django.http import HttpResponseForbidden
from django.shortcuts import render
from .models import MyUser,Products,Category,SalesItems,Sales
from django.views.generic import CreateView,FormView,ListView,View,UpdateView
from pos.forms import LoginForm,RegistrationForm,CategoryForm,ProductForm,SalesItemsForm
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.urls import reverse_lazy
from datetime import datetime
# Create your views here.


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)    
    return wrapper

decs=[signin_required,never_cache]


@signin_required
@never_cache
def signout_view(request,*args,**kwargs):
    logout(request)
    messages.success(request,"User Logged out")
    return redirect("signin")

@method_decorator(decs,name="dispatch")  
class SignupView(UserPassesTestMixin,CreateView):
    model=MyUser   
    form_class=RegistrationForm
    template_name='register.html'
    success_message="User has been created"
    success_url=reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_superuser


class LoginFormView(FormView):
    form_class=LoginForm
    template_name='login.html'

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)   
        if form.is_valid():
            uname=form.cleaned_data.get("username")   
            pwd=form.cleaned_data.get("password") 
            usr=authenticate(request,username=uname,password=pwd) 
            if usr:
                login(request,usr)
                messages.success(request,"Login Successfull")
                return redirect('home')
            else:
                messages.success(request,"Invalid Credentials")                            
                return render(request,"login.html",{"form":form})

@method_decorator(decs,name="dispatch")        
class BaseView(ListView):
    model=Products
    template_name='base.html'
    context_object_name="pro"
    pk_url_kwarg='id'           
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)      
        sales=Sales.objects.all()
        context['s']=sales
        return context            


@method_decorator(decs,name="dispatch")        
class HomeView(ListView):
    model=Products
    form_class=Products
    template_name='home.html'
    context_object_name="pro"
    success_url=reverse_lazy("home")
    pk_url_kwarg='id'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)      
        category=Category.objects.all()
        context['cat']=category
        sales=SalesItems.objects.all()
        context['s']=sales
        pro=Sales.objects.all()
        context['p']=pro
        today = datetime.now().strftime('%Y-%m-%d')
        s=Sales.objects.filter(date_added=today)
        context['sale_today']=s
        return context

@method_decorator(decs,name="dispatch")
class CategoryView(CreateView,ListView):
    model=Category
    form_class=CategoryForm
    template_name='category.html'
    context_object_name="category"
    success_url=reverse_lazy("category")
    pk_url_kwarg='id'

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)

@method_decorator(decs,name="dispatch")        
class ProductView(CreateView,ListView):
    model=Products
    form_class=ProductForm
    template_name='products.html'
    context_object_name="products"
    success_url=reverse_lazy("products")
    pk_url_kwarg='id'

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    

@method_decorator(decs,name="dispatch")        
class POSView(CreateView,ListView):
    model=SalesItems
    form_class=SalesItemsForm
    template_name='pos.html'
    context_object_name="pos"
    success_url=reverse_lazy("pos")
    pk_url_kwarg='id'

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)    
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)      
        sales=SalesItems.objects.all()
        context['sales']=sales
        return context

    def post(self, request, *args, **kwargs):
        form=SalesItemsForm(request.POST)
        if form.is_valid():  
            product_id=form.cleaned_data.get("product_id")
            qty=form.cleaned_data.get("qty")   
            if qty == 0:
                messages.error(self.request,'Enter quantity of Product !')   
            else:      
                existing_sale = SalesItems.objects.filter(product_id=product_id).exists() 
                if existing_sale:
                    messages.error(self.request,'Product already Added !')
                elif product_id.status == 1:
                    price = product_id.price
                    total = price * qty
                    SalesItems.objects.create(product_id=product_id, qty=qty, price=price, total=total)
                else:
                    messages.error(self.request, 'Product is inactive, Sales cant be proceeded !')
                    return redirect("pos")
            return redirect("pos")           
        else:
            return redirect("pos")
            
            # price=product_id.price
            # total=price*qty 
            # SalesItems.objects.create(product_id=product_id,qty=qty,price=price,total=total)                                         
            
            

@method_decorator(decs,name="dispatch")  
class BillView(ListView):        
    model=SalesItems
    template_name='bill.html'
    context_object_name="sales"
    success_url=reverse_lazy("pos")
    pk_url_kwarg='id'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)      
        return context
        
@method_decorator(decs,name="dispatch")
class SalesDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        SalesItems.objects.filter(id=id).delete()    
        return redirect("pos")  
      
# decs
# def sales_view(request,*args,**kwargs):
#     id=kwargs.get("id")
#     product_id=SalesItems.objects.get(id=id).product_id.name
#     total=SalesItems.objects.get(id=id).total
#     qty=SalesItems.objects.get(id=id).qty
#     Sales.objects.create(sales_items=product_id,total_amount=total,qty=qty)
#     return redirect("pos")         


@method_decorator(decs,name="dispatch")  
class SalesDetailView(ListView):        
    model=Sales
    template_name='sales.html'
    context_object_name="sales"
    pk_url_kwarg='id'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)    
        return context


@method_decorator(decs,name="dispatch")
class TransactionDeleteView(View):
    def get(self,request,*args,**kwargs):
        if request.user.role!=1:
            return HttpResponseForbidden("You do not have permission for performing this Action")           
        id=kwargs.get("id")
        Sales.objects.filter(id=id).delete()    
        return redirect("sales_details")


@method_decorator(decs,name="dispatch")       
class ProductUpdateView(UpdateView):
    model=Products
    form_class=ProductForm
    template_name="edit_product.html"
    pk_url_kwarg='id'
    success_url=reverse_lazy("products")

    def dispatch(self, request, *args, **kwargs):
        if request.user.role!=1:
            return HttpResponseForbidden("You do not have permission for performing this Action")           
        return super().dispatch(request, *args, **kwargs)

@method_decorator(decs,name="dispatch")       
class CategoryUpdateView(UpdateView):
    model=Category
    form_class=CategoryForm
    template_name="edit_category.html"
    pk_url_kwarg='id'
    success_url=reverse_lazy("category")

    def dispatch(self, request, *args, **kwargs):
        if request.user.role!=1:
            return HttpResponseForbidden("You do not have permission for performing this Action")           
        return super().dispatch(request, *args, **kwargs)

@method_decorator(decs,name="dispatch")
class ProductDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Products.objects.filter(id=id).delete()    
        return redirect("products") 
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.role!=1:
            return HttpResponseForbidden("You do not have permission for performing this Action")           
        return super().dispatch(request, *args, **kwargs)

@method_decorator(decs,name="dispatch")
class CategoryDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Category.objects.filter(id=id).delete()    
        return redirect("category") 
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.role!=1:
            return HttpResponseForbidden("You do not have permission for performing this Action")           
        return super().dispatch(request, *args, **kwargs)

@method_decorator(decs,name="dispatch")
class SalesAllDeleteView(View):
    def get(self,request,*args,**kwargs):
        Sales.objects.all().delete()    
        return redirect("sales_details") 
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.role!=1:
            return HttpResponseForbidden("You do not have permission for performing this Action")           
        return super().dispatch(request, *args, **kwargs)


@signin_required
@never_cache 
def sales_report(request):
    today = datetime.now().strftime('%Y-%m-%d')
    sales = Sales.objects.filter(date_added=today) 
    return render(request, 'sales_report.html', { 'sales': sales})


@method_decorator(decs,name="dispatch")
class SalesItemDeleteView(View):
    def get(self,request,*args,**kwargs):
        SalesItems.objects.all().delete()    
        return redirect("pos") 

@method_decorator(decs,name="dispatch")
class SalesSaveView(View):
    def get(self,request,*args,**kwargs):
        s=SalesItems.objects.all() 
        for i in s:
            if i.product_id:
                pro=i.product_id
                total=i.total
                qty=i.qty
                Sales.objects.create(sales_items=pro,total_amount=total,qty=qty)
        return redirect("pos")            
