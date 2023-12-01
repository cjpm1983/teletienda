from django.contrib import admin
from .models import Tienda, Producto, Rating
from django.contrib.auth.models import User
from .models import UserProfile
from django.db import models



class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombreProducto', 'tienda', 'visible')
    list_editable = ('visible',)
    list_filter = ('tienda','visible')
    actions = ['update_visible']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Check if the user is a superuser or has specific permissions
        if request.user.is_superuser or request.user.has_perm('tienda_app.can_manage_all_productos'):
            return qs  # Superusers and users with specific permissions can manage all productos
        
        # Get the tiendas that the user is allowed to manage
        allowed_tiendas = Tienda.objects.filter(managers=request.user)
        
        # Filter the productos based on the allowed tiendas
        return qs.filter(tienda__in=allowed_tiendas)
    @admin.action(description='Actualizar visibilidad')
    def update_visible(self, request, queryset):
        updated_count = queryset.update(visible=True)
        self.message_user(request, '{} productos actualizados'.format(updated_count))
    #update_visible.short_description = 'Actualizar visibilidad'

class TiendaAdmin(admin.ModelAdmin):
    filter_horizontal = ('managers',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_username')  # Campos a mostrar en la lista de usuarios
    # Otros ajustes y configuraciones adicionales, si los necesitas

class RatingAdmin(admin.ModelAdmin):
   pass

# Register your models here.


admin.site.register(Tienda, TiendaAdmin)

admin.site.register(Producto, ProductoAdmin)

admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(Rating, RatingAdmin)