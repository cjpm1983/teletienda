from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def create_manage_all_productos_permission():
    content_type = ContentType.objects.get(app_label='tienda_app', model='Producto')
    permission, created = Permission.objects.get_or_create(
        codename='can_manage_all_productos',
        name='Can manage all productos',
        content_type=content_type,
    )
    return permission