from django.urls import include, path
from rest_framework import routers
from tienda_app.forms import MyAuthenticationForm
from .views import TiendaViewSet, ProductoViewSet
from django.contrib.auth import views as auth_views

from . import views

from .views import pushhome, send_push

router = routers.DefaultRouter()
router.register(r'tiendas', TiendaViewSet)
router.register(r'productos', ProductoViewSet)

from django.views.generic import TemplateView

urlpatterns = [
    path('', views.listar_producto, name='listar_producto_1'),
    path('api/', include(router.urls)),
    path('crear_tienda/', views.crear_tienda, name='crear_tienda'),
    path('editar_tienda/<int:tienda_id>/', views.editar_tienda, name='editar_tienda'),
    path('eliminar_tienda/<int:tienda_id>/', views.eliminar_tienda, name='eliminar_tienda'),
    path('listar_tienda/', views.listar_tienda, name='listar_tienda'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('editar_producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('listar_producto/', views.listar_producto, name='listar_producto'),
    path('detalle_producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),

    
    #path('login/', auth_views.LoginView.as_view(), {'template_name': 'registration/login.html', 'authentication_form': MyAuthenticationForm}),
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('logout/', views.milogout_view, name='milogout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('checkmail/', views.checkmail, name='checkmail'),

    path('pushhome', pushhome),
    path('send_push', send_push),

    #path('webpush/', include('webpush.urls')),


    path('sw.js', TemplateView.as_view(template_name='notificationspush/sw.js', content_type='application/x-javascript')),

    path('submit_rating/<int:producto_id>/', views.submit_rating, name='submit_rating'),

]