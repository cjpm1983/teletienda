from django import forms
from .models import Tienda, Producto

class TiendaForm(forms.ModelForm):
    class Meta:
        model = Tienda
        fields = '__all__'

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }