from django.contrib import admin
from pos.models import MyUser,Products,Category,SalesItems,Sales
# Register your models here.

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Sales)
admin.site.register(SalesItems)
admin.site.register(MyUser)