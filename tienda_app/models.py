from django.db import models
from django.contrib.auth.models import User 

from django.db.models import Avg

from django_resized import ResizedImageField
from django.utils import timezone

from django.utils.html import mark_safe

# Create your models here.

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=255)

    def __str__(self):
        return self.nombre

class Tienda(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = ResizedImageField(size=[1000, 700], upload_to='tiendas/',default='tiendas/default.png', blank=True, null=True)
    descripcion = models.TextField(blank=True)
    direccion = models.CharField(max_length=100,blank=True)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20,blank=True)
    encargado = models.CharField(max_length=100,blank=True)
    ciudad = models.CharField(max_length=100,blank=True)
    provincia_choices = [
        ('pinar_del_rio','Pinar del Río'),
        ('artemisa','Artemisa'),
        ('la_habana','La Habana'),
        ('mayabeque','Mayabeque'),
        ('matanzas','Matanzas'),
        ('cienfuegos','Cienfuegos'),
        ('villa_clara','Villa Clara'),
        ('sancti_spiritus','Sancti Spíritus'),
        ('ciego_de_avila','Ciego de Ávila'),
        ('camaguey','Camagüey'),
        ('las_tunas', 'Las Tunas'),
        ('granma','Granma'),
        ('holguin','Holguín'),
        ('santiago_de_cuba', 'Santiago de Cuba'),
        ('guantanamo','Guantánamo'),
    ]
    provincia = models.CharField(max_length=100,blank=True, choices=provincia_choices)
    managers = models.ManyToManyField(User, related_name='managed_tiendas',blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)


    def image_tag(self):
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.imagen.url))

    image_tag.short_description = 'V. Previa'

    def __str__(self):
        return self.nombre
    
    
class Producto(models.Model):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
    etiquetas = models.ManyToManyField(Etiqueta)
    nombreProducto = models.CharField(max_length=100)
    foto = ResizedImageField(size=[1000, 700], upload_to='productos/',default='images/default.png', blank=True, null=True)
    cantidad = models.IntegerField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=20,blank=True)
    descripcion = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=True,
                                   verbose_name='Visible',
                                   help_text='Si el producto es visible se mostrará en la tienda online.',
                                   )
    
    def image_tag(self):
            return mark_safe('<img src="%s" width="48" height="48" />' % (self.foto.url))

    image_tag.short_description = 'V. Previa'
 
    rating_avg = models.FloatField(default=0)
    rating_cnt = models.IntegerField(default=0)

    likes = models.ManyToManyField(User, blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    @property
    def rating_average(self):
        return self.rating_set.aggregate(avg_rating=Avg('stars')).get('avg_rating', 0)
    
    @property
    def rating_count(self):
        return self.rating_set.count()
        

    @property
    def get_comentarios(self):
        own_commentarios = Comment.objects.filter(producto=self)
        return own_commentarios

    def __str__(self):
        return self.nombreProducto
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_username = models.CharField(max_length=50,blank=True)
    uri_token = models.CharField(max_length=255,blank=True)
    confirmation_token = models.CharField(max_length=255, blank=True)


class Rating(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField()

    def __str__(self):
        return f"Rating for {self.producto.nombreProducto} by {self.usuario.username}"  
    
class Comment(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='comentarios', null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    super_comment = models.IntegerField(blank=True, null=True)
    
    #super_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='super_comments')

    # def save(self, *args, **kwargs):
    #      if not self.super_comment:
    #          self.super_comment = self
    #      super().save(*args, **kwargs)
        
    def related_rating(self):
        return Rating.objects.filter(producto=self.producto,usuario=self.usuario).first()

    def approve(self):
        self.approved_comment = True
        self.save()
    
class Preferencia (models.Model):
    titulo = models.CharField(null=True,blank=True,max_length=100)
    descripcion = models.TextField(null=True,blank=True)
    vnumerico = models.IntegerField(null=True,blank=True,verbose_name="Valor si es un número") 
    vtexto = models.CharField(null=True,blank=True,verbose_name="Valor si es un texto",max_length=255)
    

    class Meta:
        verbose_name = ("")
        verbose_name_plural = ("Preferencias")

    def __str__(self):
        return self.name




'''
5. Para acceder al campo telegram_username de un usuario, puedes utilizar la relación inversa desde el modelo User al modelo UserProfile. Aquí hay un ejemplo usando el modelo User:

# Para obtener el perfil de un usuario
user_profile = user.userprofile

# Para acceder al campo telegram_username
telegram_username = user_profile.telegram_username
'''

'''
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
'''