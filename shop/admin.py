
from django.contrib import admin
from .models import Contact, Product, Order, OrderUpdate


admin.site.register(Product)
admin.site.register(Order)  
admin.site.register(OrderUpdate)


@admin.register(Contact)
     #means, register karne ke sath sath admin ko vi change kar rahe hai. injected javaScript in Post admin

class PostAdmin(admin.ModelAdmin):
    class Media:
        js= ('tinyInject.js',)





