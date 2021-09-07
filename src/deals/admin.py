from django.contrib import admin

from .models import Deal, ProductCategory, Advertiser, City

admin.site.register(Deal)
admin.site.register(ProductCategory)
admin.site.register(Advertiser)
admin.site.register(City)