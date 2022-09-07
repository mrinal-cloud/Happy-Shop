from django.contrib import admin
from .models import Blogpost,postsHide

admin.site.register(Blogpost)

@admin.register(postsHide)       #means, register karne ke sath sath admin ko vi change kar rahe hai. injected javaScript in Post admin

class PostAdmin(admin.ModelAdmin):
    class Media:
        js= ('tinyInject.js',)

