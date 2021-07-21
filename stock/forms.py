from django import forms
from .models import ItemDist, ItemModel


class item_list_create(forms.ModelForm):
    class Meta:
        model = ItemDist
        fields = '__all__'

class DateInput(forms.DateInput):
    input_type = 'date'

class Create_ItmDist_Form(forms.ModelForm):
    class Meta:
        model = ItemDist
        fields = '__all__'

        widgets = {
            'purchase_date': DateInput(attrs={'type': 'date'})
                  }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_model'].queryset = ItemModel.objects.none()

        # self.fields['item_sl'].widget.attrs['placeholder'] = 'Item Sl'
        # self.fields['item_configuration'].widget.attrs['placeholder'] = 'Item Configuration'
        for field_name, field in self.fields.items():  # use place holder
            self.fields[field_name].widget.attrs['placeholder'] = field.label

        if 'item_name' in self.data:
            try:
                item_name_id = int(self.data.get('item_name'))
                self.fields['item_model'].queryset = ItemModel.objects.filter(item_name_id=item_name_id).order_by(
                    'model_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['item_model'].queryset = self.instance.item_name.item_model_set.order_by('item_model')
