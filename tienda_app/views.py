from django.shortcuts import render
from typing import Tuple
from PIL import Image

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .models import Tienda, Producto
from .forms import TiendaForm, ProductoForm

from .serializers import TiendaSerializer, ProductoSerializer


from django.core.paginator import Paginator, EmptyPage


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
            if post.foto:
                img: Image = utils.resize_image(
                    post.foto, ImageWidth.THUMBNAIL
                )
                img.save(post.foto.path)

            post.save()
            return redirect('listar_producto')
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            #form.save()
            post: Post = form.save(commit=False)
            if post.foto:
                img: Image = utils.resize_image(
                    post.foto, ImageWidth.THUMBNAIL
                )
                img.save(post.foto.path)

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

class TiendaViewSet(viewsets.ModelViewSet):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
  

'''
from django.shortcuts import rendct_or_404, redirect
from .models import Tienda, Productoer, get_obje
from .forms import TiendaForm, ProductoForm

def listar_tiendas(request):
    tiendas = Tienda.objects.all()
    return render(request, 'listar_tiendas.html', {'tiendas': tiendas})

def detalle_tienda(request, tienda_id):
    tienda = get_object_or_404(Tienda, id=tienda_id)
    productos = Producto.objects.filter(tienda=tienda)
    return render(request, 'detalle_tienda.html', {'tienda': tienda, 'productos': productos})

def crear_tienda(request):
    if request.method == 'POST':
        form = TiendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_tienda')
    else:
        form = TiendaForm()
    return render(request, 'crear_tienda.html', {'form': form})

def editar_tienda(request, tienda_id):
    tienda = get_object_or_404(Tienda, id=tienda_id)
    if request.method == 'POST':
        form = TiendaForm(request.POST, instance=tienda)
        if form.is_valid():
            form.save()
            return redirect('detalle_tienda', tienda_id=tienda_id)
    else:
        form = TiendaForm(instance=tienda)
    return render(request, 'editar_tienda.html', {'form': form, 'tienda': tienda})

def eliminar_tienda(request, tienda_id):
    tienda = get_object_or_404(Tienda, id=tienda_id)
    tienda.delete()
    return redirect('lista_tiendas')

def crear_producto(request, tienda_id):
    tienda = get_object_or_404(Tienda, id=tienda_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.tienda = tienda
            producto.save()
            return redirect('detalle_tienda', tienda_id=tienda_id)
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form, 'tienda': tienda})

def editar_producto(request, tienda_id, producto_id):
    tienda = get_object_or_404(Tienda, id=tienda_id)
    producto = get_object_or_404(Producto, id=producto_id, tienda=tienda)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('detalle_tienda', tienda_id=tienda_id)
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form, 'tienda': tienda, 'producto': producto})

def eliminar_producto(request, tienda_id, producto_id):
    tienda = get_object_or_404(Tienda, id=tienda_id)
    producto = get_object_or_404(Producto, id=producto_id, tienda=tienda)
    producto.delete()
    return redirect('detalle_tienda', tienda_id=tienda_id)

'''

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

    new_size = get_new_image_dimensions(image.size, width)

    if new_size == image.size:
        return

    return image.resize(new_size, Image.ANTIALIAS)

class ImageWidth:
    THUMBNAIL = 150
    LARGE = 1100