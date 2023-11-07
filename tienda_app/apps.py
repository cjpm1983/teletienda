from django.apps import AppConfig
from django.db.models.signals import post_migrate
#from .permissions import create_manage_all_productos_permission
#from django.contrib.auth.models import Permission
#from django.contrib.contenttypes.models import ContentType

'''
def create_manage_all_productos_permission():
    content_type = ContentType.objects.get(app_label='tienda_app', model='Producto')
    permission, created = Permission.objects.get_or_create(
        codename='can_manage_all_productos',
        name='Can manage all productos',
        content_type=content_type,
    )
    return permission
'''
class TiendaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tienda_app'
'''    def ready(self):
        post_migrate.connect(self.create_permissions, sender=self)

    def create_permissions(self, **kwargs):
        create_manage_all_productos_permission()'''