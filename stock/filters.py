from stock.models import ItemDist
import django_filters


class Item_dstFilter(django_filters.FilterSet):
    class Meta:
        model = ItemDist
        fields = ['item_name', 'item_model', 'acblock', 'inst','room_type', ]
