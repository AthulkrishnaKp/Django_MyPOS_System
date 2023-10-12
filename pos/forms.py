from django import forms
from django.contrib.auth.forms import UserCreationForm
from pos.models import MyUser,Category,Products,SalesItems


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control border border-info","PlaceHolder":"..."}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control border border-info","PlaceHolder":"..."}))



class RegistrationForm(UserCreationForm):
    
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control border border-info ","placeholder":"enter password"}))  
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control border border-info","placeholder":"confirm password"}))              
    
   
    class Meta:
        model = MyUser
        fields = ['first_name','last_name','username','email','role']

        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control border border-info","placeholder":"enter firstname"}),
            "last_name":forms.TextInput(attrs={"class":"form-control border border-info","placeholder":"enter lastname"}),
            "username":forms.TextInput(attrs={"class":"form-control border border-info","placeholder":"enter username"}),
            "email":forms.EmailInput(attrs={"class":" form-control border border-info","placeholder":"enter email"}),
            "role":forms.Select(attrs={"class":"form-select form-control border border-primary"})
    }



class CategoryForm(forms.ModelForm):
    class Meta():
        model=Category
        fields=[
            "name",
            "description",
        ]
        
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control border border-warning mt-2","rows":3}),
            "description":forms.TextInput(attrs={"class":"form-control border border-warning mt-2","rows":3}),
        }



class ProductForm(forms.ModelForm):
    class Meta():
        model=Products
        fields=[
            "code","category_id","name","description","price","status"          
        ]

        widgets={
            "code":forms.NumberInput(attrs={"class":"form-control border border-warning mt-2","rows":3}),
            "description":forms.TextInput(attrs={"class":"form-control border border-warning mt-2","rows":3}),
            "status":forms.Select(attrs={"class":"form-select form-select-sm rounded-0","style":"max-width:200px"}),
            "name":forms.TextInput(attrs={"class":"form-control border border-warning mt-2","rows":3}),
            "price":forms.NumberInput(attrs={"class":"form-control border border-warning mt-2","rows":3}),
            "category_id":forms.Select(attrs={"class":"form-select form-select-sm rounded-0","style":"max-width:400px"})
        
        }


class SalesItemsForm(forms.ModelForm):
    class Meta():
        model=SalesItems
        fields=[
            "product_id","qty"          
        ]

        widgets={
            "qty":forms.NumberInput(attrs={"class":"form-control form-control-sm border border-warning ","rows":3,"style":"max-width:200px"}),
            "product_id":forms.Select(attrs={"class":"form-select form-select-sm rounded-0","style":"max-width:200px"}),
        }

 