'''
Created on 2013. 7. 14.

@author: lacidjun
'''
from django.contrib import admin
from app.models import *

class AdminApp(admin.ModelAdmin):
    list_display = ('id', 'created', 'Title', 'Content', 'Files')
class AdminTitle(admin.ModelAdmin):
    list_display = ('Title',)    
class AdminComment(admin.ModelAdmin):
    list_display = ('Name','Password', 'Content')
    
admin.site.register(Categories, AdminTitle)
admin.site.register(TagModel, AdminTitle)
admin.site.register(Entries, AdminApp)
admin.site.register(Comments, AdminComment)
admin.site.register(Files)