from django.contrib import admin
from .models import *

admin.site.register((MainCategory,
                    SubCategory,
                    Brand,
                    Product,
                    Seller,
                    Superuser,
                    ))