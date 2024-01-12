from django.contrib import admin
from .models import Tienda, Producto, Rating, UserProfile, Comment, Preferencia
from django.contrib.auth.models import User
from django.db import models



class ProductoAdmin(admin.ModelAdmin):
    fields = ['nombreProducto','image_tag','foto','precio','unidad','descripcion', 'tienda','cantidad'
              ,'visible','created','updated',]
    list_display = ('image_tag','nombreProducto', 'tienda', 'visible')
    list_display_links = ('image_tag','nombreProducto',)
    
    readonly_fields = ('image_tag',)
    search_fields = ('nombreProducto', 'tienda')
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
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        This method is used to override the default formfield_for_foreignkey method
        in order to restrict the list of tiendas that are displayed in the form field
        for the tienda field on the producto model.
        """
        if request.user.is_superuser:
            # Do something for superusers
            allowed_tiendas = Tienda.objects.all()
        else:
            # Do something for regular users
            # Get the list of allowed tiendas for the user
            allowed_tiendas = Tienda.objects.filter(managers=request.user)

        # Create a new formfield for the tienda field
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)

        # Set the queryset for the formfield to the list of allowed tiendas
        formfield.queryset = allowed_tiendas

        return formfield
        
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ( 'created','updated','rating_avg','rating_cnt','likes')
        return self.readonly_fields + ( 'created','updated','rating_avg','rating_cnt','likes')
    
    @admin.action(description='Actualizar visibilidad')
    def update_visible(self, request, queryset):
        updated_count = queryset.update(visible=True)
        self.message_user(request, '{} productos actualizados'.format(updated_count))
    #update_visible.short_description = 'Actualizar visibilidad'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('producto', 'usuario','text','parent_comment')
    actions = ['update_aprobado']
    #search_fields = ('usuario')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Check if the user is a superuser or has specific permissions
        if request.user.is_superuser or request.user.has_perm('tienda_app.can_manage_all_productos'):
            return qs  # Superusers and users with specific permissions can manage all productos
        
        # Get the tiendas that the user is allowed to manage
        allowed_tiendas = Tienda.objects.filter(managers=request.user)
        
        # Filter the productos based on the allowed tiendas
        return qs.filter(producto__tienda__in=allowed_tiendas)


    @admin.action(description='Aprobar Comentarios')

    def update_aprobado(self, request, queryset):
        updated_count = queryset.update(approved_comment=True)
        self.message_user(request, '{} comentarios actualizados'.format(updated_count))

class TiendaAdmin(admin.ModelAdmin):
    fields = ['nombre','image_tag','imagen','ciudad','provincia','direccion','descripcion','correo','telefono','encargado','managers']
    list_display = ('image_tag', 'nombre','provincia',)
    list_display_links= ('image_tag', 'nombre',)
    readonly_fields = ['image_tag']
    autocomplete_fields = ('managers',)
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

admin.site.register(Comment, CommentAdmin)
admin.site.register(Preferencia)
