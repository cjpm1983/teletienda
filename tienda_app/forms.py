from django import forms
from .models import Tienda, Producto
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        #fields = '__all__'
        fields = ['telegram_username','avatar']# 'first_name','last_name']  
        #fields = ['avatar']
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

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('El usuario no existe')
        return email
    
class SetPasswordForm(forms.Form):
    new_password1 = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    def clean_new_password2(self):
        new_password1 = self.cleaned_data['new_password1']
        new_password2 = self.cleaned_data['new_password2']
        if new_password1 != new_password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return new_password2

    def save(self, user):
        user.set_password(self.cleaned_data['new_password1'])
        user.save()