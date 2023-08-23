from django.contrib import admin

from .models import PaymentLink, Product


class ProductAdmin(admin.ModelAdmin):
    pass


class PaymentLinkAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(PaymentLink, PaymentLinkAdmin)
