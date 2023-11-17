from django.shortcuts import render
from typing import Tuple
from PIL import Image

import logging
logger = logging.getLogger('django')
#logger = logging.getLogger('__name__')




# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .models import Tienda, Producto
from .forms import TiendaForm, ProductoForm
from django.contrib.auth.forms import UserCreationForm

from .serializers import TiendaSerializer, ProductoSerializer


from django.core.paginator import Paginator, EmptyPage


from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.decorators import login_required

from django.http.response import HttpResponse
from django.views.decorators.http import require_GET, require_POST

def crear_tienda(request):
    if request.method == 'POST':
        form = TiendaForm(request.POST)
        if form.is_valid():
            tienda = form.save()
            return redirect('listar_tienda')
    else:
        form = TiendaForm()
    return render(request, 'crear_tienda.html', {'form': form})

def editar_tienda(request, tienda_id):
   
    tienda = get_object_or_404(Tienda, pk=tienda_id)
    if request.method == 'POST':
        form = TiendaForm(request.POST, instance=tienda)
        if form.is_valid():
            form.save()
            return redirect('listar_tienda')
    else:
        form = TiendaForm(instance=tienda)
    return render(request, 'editar_tienda.html', {'form': form, 'tienda': tienda})

def eliminar_tienda(request, tienda_id):
    tienda = get_object_or_404(Tienda, pk=tienda_id)
    if request.method == 'POST':
        tienda.delete()
        return redirect('listar_tienda')
    return render(request, 'eliminar_tienda.html', {'tienda': tienda})

def listar_tienda(request):
    tiendas = Tienda.objects.all()
    return render(request, 'listar_tienda.html', {'tiendas': tiendas})

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            #producto = form.save()
            post: Post = form.save(commit=False)
           
            post.save()
            return redirect('listar_producto')
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})

import os

def editar_producto(request, producto_id):
    logger.info("Hello world")
    print("hello")
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            post: Post = form.save(commit=False)
              
            post.save()
            return redirect('listar_producto')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_producto')
    return render(request, 'eliminar_producto.html', {'producto': producto})

def listar_producto(request):
    productos = Producto.objects.all()
    mostrar = int(request.GET.get('mostrar', 5))
    paginator = Paginator(productos, mostrar)  # Muestra 4 productos por página
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(1)
    return render(request, 'listar_producto.html', {'page_obj': page_obj, 'mostrar': mostrar})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})

from .forms import CustomUserCreationForm
from .models import UserProfile
from .forms import ProfileForm




@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('listar_producto')
    else:
        form = ProfileForm(instance=request.user.userprofile)
    return render(request, 'registration/edit_profile.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            user_profile = UserProfile.objects.create(user=user)

            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email_from = 'noreply@teletienda.com'  # Reemplaza con tu dirección de correo electrónico
            recipient_list = [user.email]
            email = EmailMessage(mail_subject, message, email_from, recipient_list)
            email.send()

            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
@login_required
def profile(request):
    return render(request, 'registration/profile.html')

from django.contrib.auth import logout

def milogout_view(request):
    logout(request)
    return redirect('logout') 

class TiendaViewSet(viewsets.ModelViewSet):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
  

#Utils
def get_new_image_dimensions(
    original_dimensions: Tuple[int, int], new_width: int
) -> Tuple[int, int]:
    original_width, original_height = original_dimensions

    if original_width < new_width:
        return original_dimensions

    aspect_ratio = original_height / original_width

    new_height = round(new_width * aspect_ratio)

    return (new_width, new_height)

def resize_image(original_image: Image, width: int) -> Image:

    image = Image.open(original_image)
    image = image.convert('RGB')

    new_size = get_new_image_dimensions(image.size, width)
    #logger.info("original-> %s new size-> %s".format(image.size,new_size))
    
    if new_size == image.size:
        return

    return image.resize((100,100), Image.ANTIALIAS) 



class ImageWidth:
    THUMBNAIL = 150
    LARGE = 150



def confirmEmail(request):    
    subject = 'Teletienda: Confirmación de Registro'
    message = ' Para confirmar su registro, por favor haga click en el siguiente enlace \
    <a href=#>Confirmar registro</a> '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['cjpm1983@gmail.com',]    
    send_mail( subject, message, email_from, recipient_list )    
    #return redirect('listar_tienda')

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/activation_success.html')
    else:
        return render(request, 'registration/activation_failed.html')
    
from webpush import send_user_notification
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse
import json

@require_GET
def pushhome(request):
   webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
   vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
   user = request.user
   return render(request, 'webpush/pushhome.html', {user: user, 'vapid_key': vapid_key})

@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)

        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        user_id = data['id']
        user = get_object_or_404(User, pk=user_id)
        payload = {'head': data['head'], 'body': data['body']}
        send_user_notification(user=user, payload=payload, ttl=1000)

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})