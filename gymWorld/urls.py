"""gymWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from mainApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Index),
    path('login/',views.loginPage),
    path('logout/',views.logout),
    path('signup/',views.signup),
    path('profile/',views.profile),
    path('shop/<str:mc>/<str:sc>/<str:br>/',views.shopPage),
    path('sellerProfile/',views.sellerProfile),
    path('superuserProfile/',views.SuperuserProfile),
    path('addProduct/',views.addProduct),
    path('editProduct/<int:num>/',views.editProduct),
    path('deleteProduct/<int:num>/',views.deleteProduct),
    path('crudcategory/',views.crudCategory),
    path('deleteMainCategory/<int:num>/',views.deleteMainCategory),
    path('deleteSubCategory/<int:num>/',views.deleteSubCategory),
    path('deleteBrand/<int:num>/',views.deleteBrand),
    path('editMainCategory/<int:num>/',views.editMainCategory),
    path('editSubCategory/<int:num>/',views.editSubCategory),
    path('editBrand/<int:num>/',views.editBrand),
    path('productapi/',views.Product_api),
    path('maincatapi/',views.Maincat_api),
    path('subcatapi/',views.Subcat_api),
    path('brand/',views.Brand_api),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
