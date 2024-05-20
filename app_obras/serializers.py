from rest_framework import serializers
from .models import Categoria, Producto, Boleta, detalle_boleta

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class BoletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleta
        fields = '__all__'

class DetalleBoletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = detalle_boleta
        fields = '__all__'