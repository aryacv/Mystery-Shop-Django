from django.contrib import admin
from .models import Item, PurchasedItem, CharacterClass 

admin.site.register(Item)
admin.site.register(PurchasedItem)
admin.site.register(CharacterClass)