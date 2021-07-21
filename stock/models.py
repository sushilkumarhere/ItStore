from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError


# Create your models here.

class YourBaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def validate_file_size(value):
    filesize = value.size
    if filesize > 102400:
        raise ValidationError("The maximum file size that can be uploaded is 100KB")
    else:
        return value


class ItemName(models.Model):
    item_name = models.CharField(max_length=100)

    def __str__(self):
        return self.item_name

    class Meta:
        ordering = ["item_name"]


class InstituteName(models.Model):
    Inst_name = models.CharField(max_length=100)

    def __str__(self):
        return self.Inst_name

    class Meta:
        ordering = ["Inst_name"]


class ItemModel(models.Model):
    item_name = models.ForeignKey(ItemName, on_delete=models.SET_NULL, null=True)
    model_name = models.CharField(max_length=100)

    def __str__(self):
        return self.model_name
        # return '%s %s' % (self.item_name, self.model_name)



class ac_block(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RoomType(models.Model):
    room_type = models.CharField(max_length=100)

    def __str__(self):
        return self.room_type


class ItemDist(models.Model):
    item_name = models.ForeignKey(ItemName, on_delete=models.CASCADE)
    item_model = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    #item_sl = models.CharField(max_length=100)
    item_configuration = models.CharField("Items Specifications", max_length=100)
    purchase_date = models.DateField(null=True,blank=True)
    acblock = models.ForeignKey(ac_block, on_delete=models.CASCADE, verbose_name="Academic Block", null=True)
    room = models.CharField(max_length=100, verbose_name="Room No")
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    inst = models.ForeignKey(InstituteName, on_delete=models.CASCADE, null=True, verbose_name="Institute Name")
    user = models.CharField(max_length=100, blank=True)
    item_qty = models.IntegerField()
    act = models.IntegerField(default=0,editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Item Distribution"



