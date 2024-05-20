from django import forms
from .models import Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto 
        fields = ['idProducto', 'marca', 'nombre', 'categoria', 'imagen']
        labels ={
            'idProducto':'IdProducto',
            'marca' : 'Marca',
            'nombre': 'Nombre',
            'categoria':'Categoria',
            'imagen':'Imagen'
        }
        widgets={

            'idProducto':forms.TextInput(
                attrs={
                    'placeholder':'Ingrese el Id..',
                    'id': 'id',
                    'class': 'form-control',
                }
            ),
            'marca': forms.TextInput(
                attrs={
                    'placeholder':'Ingrese marca..',
                    'id':'marca',
                    'class':'form-control',
                }
            ),
            'nombre': forms.TextInput(
                attrs={
                    'placeholder':'Ingrese nombre..',
                    'id':'nombre',
                    'class':'form-control',
                }
            ),
            'categoria': forms.Select(
                attrs={
                    'id':'categoria',
                    'class':'form-control',
                }
            ),
            'imagen': forms.FileInput(
                attrs={
                    'class':'form-control',
                    'id': 'imagen',
                }
            )
        }