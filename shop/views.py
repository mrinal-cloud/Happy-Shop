from django.shortcuts import render,redirect
from .models import Product,Contact,Order,OrderUpdate
from math import ceil
import json
from django.contrib import messages 
from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate,  login, logout



# Create your views here.
from django.http import HttpResponse

def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    thank=False
    if request.method=="POST":
        print(request)
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        desc=request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        messages.success(request, "Your message has been successfully sent")
        thank=True
    
    return render(request, "shop/contact.html" )





def search(request):
    query=request.GET['query']
    
    if len(query)>78:
        allPosts=Product.objects.none()
    else:
        allPostsName= Product.objects.filter(product_name__icontains=query)
        allPostsCategory= Product.objects.filter(category__icontains=query)
        allPostsSubCategory =Product.objects.filter(sub_category__icontains=query)
        allPosts=  allPostsName.union(allPostsCategory, allPostsSubCategory)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'shop/search.html', params)







def productView(request, myid):
    product=Product.objects.filter(id=myid)
    print(product)
    return render(request, "shop/prodView.html", {'product':product[0]})

def checkout(request):
    
    if request.method=="POST":
        items_json= request.POST.get('itemsJson', '')
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        phone=request.POST.get('phone', '')

        order = Order(items_json= items_json, name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()

        update= OrderUpdate(order_id= order.order_id, update_desc="The order has been placed")
        update.save()

        thank=True
        id=order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'shop/checkout.html')
    



def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if len(username)<10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('/shop')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('/shop')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('/shop')
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect('/shop')

    else:
        return HttpResponse("404 - Not found")




def handleLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/shop")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/shop")

    return HttpResponse("404- Not found")  

    


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/shop')


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    # response = json.dumps(updates, default=str)
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')