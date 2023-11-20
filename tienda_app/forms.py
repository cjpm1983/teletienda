from django import forms
from .models import Tienda, Producto
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        #fields = '__all__'
        fields = ['telegram_username',]# 'first_name','last_name']  

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


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


#Este form no lo estoy usando, lo hice en el template login.html
class MyAuthenticationForm(AuthenticationForm):
    # add your form widget here
    widgets = {
    'username': forms.CharField(label= 'Usuario: ', max_length=20, 

                              widget=forms.TextInput(
                                  attrs={"placeholder": "Username", 'style': 'width: 300px;', 
                                         "class": "form-control"})),
    'password':forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'style': 'width: 300px;', 'class': 'form-control'}))
                                        
    }
    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
    