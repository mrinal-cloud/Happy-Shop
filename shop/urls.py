from django.contrib import admin

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    # path('<str:slug>', views.searchResults, name="searchResults"),
    path("products/<int:myid>", views.productView, name="ProductView"),  #for quick view purpose 
    path("checkout/", views.checkout, name="Checkout"),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handleLogin, name="handleLogin"),
    path('logout', views.handleLogout, name="handleLogout"),

    
]
 