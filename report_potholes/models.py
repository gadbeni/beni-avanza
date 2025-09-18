from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

# Create your models here.
class Category(models.Model):
    name = models.CharField('nombre',max_length=255)
    icon = models.ImageField('icono',upload_to='category_icons/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Pothole(models.Model):
    reported_by = models.CharField('reportado por',max_length=255, null=True, blank=True)
    phone = models.CharField('teléfono',max_length=15, null=True, blank=True)
    title = models.CharField('título',max_length=255, null=True, blank=True)
    description = models.TextField('descripción', null=True, blank=True)
    approved = models.BooleanField('aprobado',default=False)
    photo = models.ImageField('foto',upload_to='potholes/')
    thumbnail = ImageSpecField(source='photo',
                               processors=[ResizeToFit(300)],  # Cambia el tamaño de la imagen para que encaje en un cuadro de 800x800, manteniendo la relación de aspecto
                               format='JPEG',
                               options={'quality': 60})
    display_image = ImageSpecField(source='photo',
                                   processors=[ResizeToFit(800)],  # Para la imagen a mostrar en grande
                                   format='JPEG',
                                   options={'quality': 80})
    year_management = models.IntegerField('Gestión', null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PotholeImage(models.Model):
    pothole = models.ForeignKey(Pothole, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pothole_images/')
    thumbnail = ImageSpecField(source='photo',
                               processors=[ResizeToFit(300)],  # Cambia el tamaño de la imagen para que encaje en un cuadro de 800x800, manteniendo la relación de aspecto
                               format='JPEG',
                               options={'quality': 60})
    display_image = ImageSpecField(source='photo',
                                   processors=[ResizeToFit(800)],  # Para la imagen a mostrar en grande
                                   format='JPEG',
                                   options={'quality': 80})
    

class CategoryPrivate(models.Model):
    name = models.CharField('nombre',max_length=255)
    icon = models.ImageField('icono',upload_to='category_picons/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Agent(models.Model):
    OPCIONES_PROVINCIA = [
        ('cercado', 'Cercado'),
        ('vacadiez', 'Vaca Díez'),
        ('ballivian', 'Ballivián'),
        ('yacuma', 'Yacuma'),
        ('moxos', 'Moxos'),
        ('marban', 'Marbán'),
        ('mamore', 'Mamoré'),
        ('itenez', 'Iténez'),
    ]
    full_name = models.CharField('nombre',max_length=255, null=True, blank=True)
    organization = models.TextField('organización', null=True, blank=True)
    province = models.CharField(
        max_length=20,  # O el tamaño máximo que necesites para los valores guardados
        choices=OPCIONES_PROVINCIA,
        default='cercado',  # Opcional: un valor predeterminado
        verbose_name="Provincia" # Opcional: nombre amigable para el formulario/admin
    )
    active = models.BooleanField('activo',default=True)
    photo = models.ImageField('foto',upload_to='agent/')
    thumbnail = ImageSpecField(source='photo',
                               processors=[ResizeToFit(300)],  # Cambia el tamaño de la imagen para que encaje en un cuadro de 800x800, manteniendo la relación de aspecto
                               format='JPEG',
                               options={'quality': 60})
    display_image = ImageSpecField(source='photo',
                                   processors=[ResizeToFit(800)],  # Para la imagen a mostrar en grande
                                   format='JPEG',
                                   options={'quality': 80})
    year_management = models.IntegerField('Gestión', null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    category = models.ForeignKey(CategoryPrivate, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)