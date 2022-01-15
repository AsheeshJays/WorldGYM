from email.utils import collapse_rfc2231_value
from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
import io
from rest_framework.parsers import JSONParser
from rest_framework.serializers import Serializer
from .serializers import *
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def Index(request):
    mainCat = MainCategory.objects.all()
    subCat = SubCategory.objects.all()
    brand = Brand.objects.all()
    product = Product.objects.all()
    
    return render(request, 'index.html',{'MainCat':mainCat,'SubCat':subCat,'Brand':brand,'Product':product})


def loginPage(request):
    if(request.method=="POST"):
        uname = request.POST.get('name')
        pward = request.POST.get('password')
        user = authenticate(username=uname,password=pward) 
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect('/admin/')
            else:
                return HttpResponseRedirect("/profile/")
        else:
            messages.error(request,"Invalid UserName or Password")       
    return render(request,"login.html")

def signup(request):
    if(request.method=="POST"):
        if(request.POST.get('accountType')=="seller"):
            s = Seller()
            s.name = request.POST.get("name")
            uname= s.username = request.POST.get("username")
            pward = request.POST.get("password")
            s.email = request.POST.get("email")
            s.phone = request.POST.get("phone")
            user = User.objects.create_user(username=uname,password=pward)
            user.save()
            s.save()
        else:
            b = Superuser()
            b.name = request.POST.get("name")
            uname= b.username = request.POST.get("username")
            pward = request.POST.get("password")
            b.email = request.POST.get("email")
            b.phone = request.POST.get("phone")
            user = User.objects.create_user(username=uname,password=pward)
            user.save()
            b.save()
        return HttpResponseRedirect('/profile/')
    return render(request,"signup.html")

@login_required(login_url='/login/')
def profile(request):
    user = User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect('/admin/')
    else:
        try:
            seller = Seller.objects.get(username=request.user)
            return HttpResponseRedirect("/sellerProfile/")
        except:
            buyer = Superuser.objects.get(username=request.user)
            return HttpResponseRedirect("/superuserProfile/")

@login_required(login_url='/login/')
def sellerProfile(request):
    seller = Seller.objects.get(username=request.user)
    product = Product.objects.all()
    return render(request,"sellerprofile.html",{"User":seller,"Product":product})

@login_required(login_url='/login/')
def SuperuserProfile(request):
    suser = Superuser.objects.get(username=request.user)
    product = Product.objects.all()
    return render(request,"superuserprofile.html",{"User":suser,"Product":product})


@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def addProduct(request):
    if(request.method=="POST"):
        p = Product()
        p.name = request.POST.get("name")
        p.pro_code = request.POST.get("pro_code")
        p.price = int(request.POST.get("price"))
        p.mainCat = MainCategory.objects.get(name=request.POST.get("mc"))
        p.subCat = SubCategory.objects.get(name=request.POST.get("sc"))
        p.brand = Brand.objects.get(name=request.POST.get("brand"))
        p.superuser = Superuser.objects.get(username=request.user)
        p.mfcdate = request.POST.get("mfcdate")
        p.expdate = request.POST.get("expdate")
        p.pro_owner = request.POST.get("pro_owner")
        p.pic1 = request.FILES.get("pic1")
        p.save()
        return HttpResponseRedirect('/profile/')
    mc = MainCategory.objects.all()
    sc = SubCategory.objects.all()
    brand = Brand.objects.all()
    return render(request,"addproduct.html",{
                                            "MC":mc,
                                            "SC":sc,
                                            "Brand":brand
                                             })
@login_required(login_url='/login/')
def editProduct(request,num):
    p = Product.objects.get(pid=num)
    if(request.method=="POST"):
        p.name = request.POST.get("name")
        p.pro_code = request.POST.get("pro_code")
        p.price = int(request.POST.get("price"))
        p.mainCat = MainCategory.objects.get(name=request.POST.get("mc"))
        p.subCat = SubCategory.objects.get(name=request.POST.get("sc"))
        p.brand = Brand.objects.get(name=request.POST.get("brand"))
        p.seller = Seller.objects.get(username=request.user)
        p.mfcdate = request.POST.get("mfcdate")
        p.expdate = request.POST.get("expdate")
        p.pro_owner = request.POST.get("pro_owner")
        if(not request.FILES.get("pic1")==None):
            p.pic1 = request.FILES.get("pic1")
        p.save()
        return HttpResponseRedirect('/profile/')
    mc = MainCategory.objects.all()
    sc = SubCategory.objects.all()
    brand = Brand.objects.all()
    return render(request,"editproduct.html",{"Product":p,
                                            "MC":mc,
                                            "SC":sc,
                                            "Brand":brand})

@login_required(login_url='/login/')
def deleteProduct(request,num):
    product = Product.objects.get(pid=num)
    seller  = Seller.objects.get(username=request.user)
    if(product.seller==seller):
        product.delete()
        return HttpResponseRedirect("/sellerProfile/")
    else:
        return HttpResponseRedirect("/")

def shopPage(request,mc,sc,br):
    mainCat = MainCategory.objects.all()
    subCat = SubCategory.objects.all()
    brand = Brand.objects.all()
    if(mc=="None" and sc=="None" and br=="None"):
        products = Product.objects.all()
    elif(mc!="None" and sc=="None" and br=="None"):
        products = Product.objects.filter(mainCat=mc)
    elif(mc=="None" and sc!="None" and br=="None"):
        products = Product.objects.filter(subCat=sc)
    elif(mc=="None" and sc=="None" and br!="None"):
        products = Product.objects.filter(brand=br)
    elif(mc!="None" and sc!="None" and br=="None"):
        products = Product.objects.filter(mainCat=mc,subCat=sc)
    elif(mc!="None" and sc=="None" and br!="None"):
        products = Product.objects.filter(mainCat=mc,brand=br)
    elif(mc=="None" and sc!="None" and br!="None"):
        products = Product.objects.filter(subCat=sc,brand=br)
    else:
        products = Product.objects.filter(mainCat=mc,subCat=sc,brand=br)
    return render(request,'shop.html',{"MainCat":mainCat,
                                        "SubCat":subCat,
                                        "Brand":brand,
                                        "MC":mc,
                                        "SC":sc,
                                        "BR":br,
                                        "Product":products})
@login_required(login_url='/login/')  
def crudCategory(request):
    if(request.method=="POST"):
        m = MainCategory()
        s = SubCategory()
        b = Brand()
        m.name = request.POST.get("mname")
        s.name = request.POST.get("sname")
        b.name = request.POST.get("bname")
        m.save()
        s.save()
        b.save()
    mc = MainCategory.objects.all()
    sc = SubCategory.objects.all()
    brand = Brand.objects.all()
    return render(request, 'crudcategory.html',{'mainCat':mc,'subCat':sc,'Brand':brand})

@login_required(login_url='/login/')
def deleteMainCategory(request,num):
    m = MainCategory.objects.get(mcid=num)
    m.delete()
    return HttpResponseRedirect('/crudcategory/')

@login_required(login_url='/login/')
def deleteSubCategory(request,num):
    s = SubCategory.objects.get(scid=num)
    s.delete()
    return HttpResponseRedirect('/crudcategory/')

@login_required(login_url='/login/')
def deleteBrand(request,num):
    b = Brand.objects.get(bid=num)
    b.delete()
    return HttpResponseRedirect('/crudcategory/')

@login_required(login_url='/login/')
def editMainCategory(request,num):
    m = MainCategory.objects.get(mcid=num)
    if(request.method=="POST"):
        m.name = request.POST.get("name")
        m.save()
        return HttpResponseRedirect('/crudcategory/')
    return render(request,"editmaincategory.html",{'MainCategory':m})

@login_required(login_url='/login/')
def editSubCategory(request,num):
    s = SubCategory.objects.get(scid=num)
    if(request.method=="POST"):
        s.name = request.POST.get("name")
        s.save()
        return HttpResponseRedirect('/crudcategory/')
    return render(request,"editsubcategory.html",{'SubCategory':s})

@login_required(login_url='/login/')
def editBrand(request,num):
    b = Brand.objects.get(bid=num)
    if(request.method=="POST"):
        b.name = request.POST.get("name")
        b.save()
        return HttpResponseRedirect('/crudcategory/')
    return render(request,"editsubcategory.html",{'Brand':b})


@csrf_exempt
def Product_api(request):
    if request.method == 'GET':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id', None)
        if id is not None:
            pro = Product.objects.get(pid=id)
            serializer = ProductSerializer(pro)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')

        pro = Product.objects.all()
        serializer = ProductSerializer(pro, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

@csrf_exempt
def Maincat_api(request):
    if request.method == 'GET':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id', None)
        if id is not None:
            pro = MainCategory.objects.get(mcid=id)
            serializer = MainCatSerializer(pro)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')

        pro = MainCategory.objects.all()
        serializer = MainCatSerializer(pro, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

@csrf_exempt
def Subcat_api(request):
    if request.method == 'GET':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id', None)
        if id is not None:
            pro = SubCategory.objects.get(scid=id)
            serializer = SubCatSerializer(pro)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')

        pro = SubCategory.objects.all()
        serializer = SubCatSerializer(pro, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

@csrf_exempt
def Brand_api(request):
    if request.method == 'GET':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id', None)
        if id is not None:
            pro = Brand.objects.get(bid=id)
            serializer = BrandSerializer(pro)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')

        pro = Brand.objects.all()
        serializer = BrandSerializer(pro, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')
    
