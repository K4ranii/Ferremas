from distutils.command.upload import upload
from django.db import models
import datetime
# Create your models here.
class Categoria (models.Model):
    idCategoria = models.IntegerField (primary_key=True, verbose_name= 'Id de Categoria')
    nombreCategoria = models.CharField(max_length=50,verbose_name='Nombre de Categoria')

    def __str__(self):
        return self.nombreCategoria
    
class Producto (models.Model):
    idProducto= models.CharField(max_length=6, primary_key=True, verbose_name='Id de Producto')
    marca= models.CharField(max_length=20,verbose_name='Marca')
    nombre= models.CharField(max_length=40, verbose_name='Nombre de producto')
    imagen= models.ImageField(upload_to='imagenes', null=True, blank=True,verbose_name='Imagen')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoria")
    precio=models.IntegerField(blank=True, null=True, verbose_name="Precio")

    def __str__(self):
        return self.idProducto



class Boleta(models.Model):
    id_boleta=models.AutoField(primary_key=True)
    total=models.BigIntegerField()
    fechaCompra=models.DateTimeField(blank=False, null=False, default = datetime.datetime.now)
    
    def __str__(self):
        return str(self.id_boleta)

class detalle_boleta(models.Model):
    id_boleta = models.ForeignKey('Boleta', blank=True, on_delete=models.CASCADE)
    id_detalle_boleta = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.BigIntegerField()

    def __str__(self):
        return str(self.id_detalle_boleta)

