from .models import Tienda, Producto, Rating, UserProfile, Comment
from .forms import TiendaForm, ProductoForm, CustomUserCreationForm, ProfileForm

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

from typing import Tuple
from PIL import Image
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets

from django.contrib.auth.forms import UserCreationForm
from .serializers import TiendaSerializer, ProductoSerializer
from django.core.paginator import Paginator, EmptyPage
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from webpush import send_user_notification
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse
from django.contrib.auth import logout
import json
import os
import logging

logger = logging.getLogger('django')
#logger = logging.getLogger('__name__')

# Create your views here.

def crear_tienda(request):
    if request.method == 'POST':
        form = TiendaForm(request.POST)  # Crear formulario con datos recibidos en la solicitud POST
        if form.is_valid():  # Verificar si el formulario es válido
            tienda = form.save()  # Guardar los datos del formulario en la base de datos
            return redirect('listar_tienda')  # Redireccionar a la página de listar tiendas
    else:
        form = TiendaForm()  # Crear formulario vacío

    return render(request, 'crear_tienda.html', {'form': form})  # Renderizar la plantilla 'crear_tienda.html' con el formulario como contexto

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

##Productos##################################################################

def listar_producto(request):
    # Definir el orden por defecto
    orderby = 'id'
    
    # Obtener valores de los filtros de precio y calificación
    cprecio = request.GET.get('cprecio') if request.GET.get('cprecio') else "off"
    ccalif = request.GET.get('ccalif') if request.GET.get('ccalif') else "off"
    
    # Obtener termino de busqueda si se a proporcionado
    termino_busqueda = request.GET.get('search')

    # Filtrar por tienda si se especifica
    if request.GET.get('tienda'):
        tienda = Tienda.objects.filter(nombre=request.GET.get('tienda')).first()
        if cprecio == 'on':
            # Ordenar por precio
            productos = Producto.objects.filter(visible=True, tienda__nombre=request.GET.get('tienda')).order_by('precio')
            if ccalif == 'on':
                # Ordenar por precio y calificación
                productos = Producto.objects.filter(visible=True,tienda__nombre=request.GET.get('tienda')).order_by('precio', '-rating_avg')
        elif ccalif == 'on':
            # Ordenar solo por calificación
            productos = Producto.objects.filter(visible=True,tienda__nombre=request.GET.get('tienda')).order_by('-rating_avg')
        else:
            # Ordenar por ID
            productos = Producto.objects.filter(visible=True,tienda__nombre=request.GET.get('tienda')).order_by('id')
    else:
        # Si no se especifica tienda, mostrar todos los productos
        tienda = Tienda(nombre="Todas las tiendas", id=-1)
        if cprecio == 'on':
            # Ordenar por precio
            productos = Producto.objects.filter(visible=True).order_by('precio')
            if ccalif == 'on':
                # Ordenar por precio y calificación
                productos = Producto.objects.filter(visible=True).order_by('precio', '-rating_avg')
        elif ccalif == 'on':
            # Ordenar solo por calificación
            productos = Producto.objects.filter(visible=True).order_by('-rating_avg')
        else:
            # Ordenar por ID
            productos = Producto.objects.filter(visible=True).order_by('id')

    if termino_busqueda:
        productos = productos.filter(visible=True, nombreProducto__icontains=termino_busqueda)
    else:
        termino_busqueda = "" # por razon de que se escibe None en la query del browser

    # Paginar resultados
    mostrar = int(request.GET.get('mostrar', 5))
    paginator = Paginator(productos, mostrar)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(1)
    
    # Obtener todas las tiendas para mostrar en la página
    tiendas = Tienda.objects.all()
    
    # Renderizar la página con los resultados y filtros
    return render(request, 'listar_producto.html', {'page_obj': page_obj, 'mostrar': mostrar, 'tiendas': tiendas, 'shop': tienda, 'cprecio': cprecio, 'ccalif': ccalif, 'search': termino_busqueda})


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

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    stars = 0
    if request.user.is_authenticated:
        ratings = producto.rating_set.filter(usuario=request.user)
        stars = 0 if len(ratings) < 1 else (ratings[0].stars)
    
    return render(request, 'detalle_producto.html', {'producto': producto,'rating':stars})


def submit_rating(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    rating = int(request.POST.get('rating', -1))
    comment = request.POST.get('comment', "")
    # Create or update the rating for the current user and product
    
    if (rating>=0):
        rating_obj, created = Rating.objects.update_or_create(
            producto=producto,
            usuario=request.user,
            defaults={'stars': rating}
        )
        
    if (comment!=""):  
        # Create or update the comment for the current user and product
        main_c = Comment.objects.filter(parent_comment__isnull=True,usuario=request.user,producto=producto).first()
        commentario = Comment(producto=producto, usuario=request.user, text=comment)

        if not main_c:
                commentario.save()
            #si no actualizar
        else:
                main_c.producto = commentario.producto
                main_c.usuario = commentario.usuario
                main_c.text = commentario.text
                main_c.created_date = commentario.created_date
                main_c.save()
              

    # Calculate the new average rating for the product
    #new_average_rating = Rating.objects.filter(producto=producto).aggregate(avg_rating=Avg('stars'))['avg_rating']
    # Update the average rating of the product
    #producto.comment_cnt = producto.comment_count
    producto.rating_avg = producto.rating_average
    producto.rating_cnt = producto.rating_count
    producto.save()

    return JsonResponse({'success': True})
'''
@login_required(login_url='login')
def like(request):
    producto_id = request.GET['producto_id']
    producto = get_object_or_404(Producto, identifier=producto_id)
    if request.user in producto.likes.all():
        producto.likes.remove(request.user)
        liked=False
    else:
        producto.likes.add(request.user)
        liked=True
    producto.save
    likes = producto.likes.count()
    response = JsonResponse({'liked': liked, 'likes': likes})
    return response'''


@login_required(login_url='login')
def comment(request,producto_id):
    
    # TODO Limitar el numero de comentarios para evitar exploit
    

    producto = get_object_or_404(Producto, id=producto_id)
    
    propios = Comment.objects.filter(producto=producto,usuario=request.user).count() 
    
    #producto.filter(nombreProducto__icontains=termino_busqueda)
    #limitamos los propios para que no haya spamers llenando de comentarios cada lugar
    if (propios < 15):
        comment_data = request.POST['comentario']
        comment = Comment(producto=producto, usuario=request.user, text=comment_data)
        
        #si tiene parent_coment es una respuesta, sino se trata del comentario principal donde se califica, 
        #debe existir solo uno por usuario y producto
        main_c = None
        if request.POST.get('parent_comment') is not None:
            comment.parent_comment = Comment.objects.get(id=request.POST['parent_comment'])
            comment.save()
        else:
            #como comprobar los vacios
            main_c = Comment.objects.filter(parent_comment__isnull=True,usuario=request.user,producto=producto).first()

            if not main_c:
                comment.save()
            #si no actualizar
            else:
                main_c.producto = comment.producto
                main_c.usuario = comment.usuario
                main_c.text = comment.text
                main_c.created_date = comment.created_date
                main_c.save()

        #response = JsonResponse({'comment': comment_data})
        #return response
        return redirect("detalle_producto",producto_id=producto_id)
    else:
        return redirect("listar_producto")

######################## REGISTRO ###############################################################

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

            return redirect('checkmail')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def checkmail(request):
    return render(request, 'registration/checkyourmail.html')

@login_required
def profile(request):
    return redirect('listar_producto') 
    #return render(request, 'registration/profile.html')


def milogout_view(request):
    logout(request)
    #return redirect('logout') 
    return redirect('listar_producto') 


def confirmEmail(request):    
    subject = 'Teletienda: Confirmación de Registro'
    message = ' Para confirmar su registro, por favor haga click en el siguiente enlace \
    <a href=#>Confirmar registro</a> '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['cjpm1983@gmail.com',]    
    send_mail( subject, message, email_from, recipient_list )    
    #return redirect('listar_tienda')



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

######################### TARTAMIENTO DE IMAGENES #################################

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


######################## PUSH NOTIFICATIONS #############################    

@require_GET
def pushhome(request):
   webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
   vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
   user = request.user
   return render(request, 'notificationspush/pushhome.html', {user: user, 'vapid_key': vapid_key})

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
    
##########################mapas#############################################
import folium
def make_markers_and_add_to_map(map, tienda):
    shop_icon = folium.Icon(color='blue', # The color of the marker 
                        icon_color='white', # The color of the drawing on the marker
                        icon='shopping-bag', # The name of the marker sign (checkout Font-Awesome v4 for more icon signs)
                        prefix='fa',
                        angle=0)
    folium.Marker(
            location = [tienda.latitude, tienda.longitude],
            popup = tienda.descripcion,
            tooltip = tienda.nombre,
            icon = shop_icon
            #draggable=True
        ).add_to(map)
    
def map_view(request, tienda_id):
        tienda = get_object_or_404(Tienda, pk=tienda_id)
        map = folium.Map(location=[22.398, -79.960], # lat and lon of the starting point
                 width="50%", # width of the map
                 height="50%", # height of the map
                 zoom_start=15, # the staring zoom
                 tiles="OpenStreetMap", # desired tile for the map respresentation
                 zoom_control=True) # controls for zoom level (True by default)
        
        make_markers_and_add_to_map(map, tienda)
        
        map = map._repr_html_()
        context = {
            'map': map,

            }
        return render(request, 'map/maps.html', context)
        
def maps(request):
        #coordenadas = list(Coordenadas.objects.values_list('lat','lon'))[-1]

        # map = folium.Map(coordenadas)
        # folium.Marker(coordenadas).add_to(map)
        # folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
        # folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
        # folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
        # folium.LayerControl().add_to(map)
        cloud_icon = folium.Icon(color='blue', # The color of the marker 
                        icon_color='white', # The color of the drawing on the marker
                        icon='shopping-bag', # The name of the marker sign (checkout Font-Awesome v4 for more icon signs)
                        prefix='fa',
                        angle=0) # Rotation for the marker sign

        first_marker = folium.Marker(location=[22.398, -79.960], # Latitude and Longitude of Marker
                    popup='mipyme Fe del valle ', # Label for the Marker
                    tooltip='first marker', # Display a text when hovering over the object
                    icon=cloud_icon, # The Icon plugin to use to render the marker
                    draggable=True) # Set to True to be able to drag the marker around the map


        map = folium.Map(location=[22.398, -79.960], # lat and lon of the starting point
                 width="50%", # width of the map
                 height="50%", # height of the map
                 zoom_start=15, # the staring zoom
                 tiles="OpenStreetMap", # desired tile for the map respresentation
                 zoom_control=True) # controls for zoom level (True by default)
        
        first_marker.add_to(map)

        map = map._repr_html_()
        context = {
            'map': map,

            }
        return render(request, 'map/maps.html', context)


##################### Utils ##################################################################

class TiendaViewSet(viewsets.ModelViewSet):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
