from django.contrib import admin
from .models import *


class item_display(admin.ModelAdmin):
    list_display = ('item_name', 'item_configuration', 'item_price', 'item_qty')
    list_filter = ("item_name", "item_configuration")
    search_fields = ['item_name', 'item_configuration']


class item_instock_display(admin.ModelAdmin):

    list_display = ('item_name', 'item_model','acblock', 'inst',  'room', 'item_qty')
    list_filter = ('item_name', 'room')
    search_fields = ['item_name__item_name', 'room']


admin.site.register(ItemName)
admin.site.register(ItemModel)
admin.site.register(ItemDist, item_instock_display)
admin.site.register(RoomType)
admin.site.register(InstituteName)
admin.site.register(ac_block)
admin.site.site_header = 'GLA Item Management'
