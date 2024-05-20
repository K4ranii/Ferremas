from django.shortcuts import render, redirect
from .forms import ProductoForm, RegistroUserForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from app_obras.compra import Carrito
from django.shortcuts import render
from django.http import HttpResponse
import random
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction
from rest_framework import generics
from .models import Categoria, Producto, Boleta, detalle_boleta
from .serializers import CategoriaSerializer, ProductoSerializer, BoletaSerializer, DetalleBoletaSerializer
from django.http import HttpResponseBadRequest


def index(request):
	productos= Producto.objects.all()
	
	return render(request, 'index.html',context={'datos':productos})


def nosotros(request):
	productos= Producto.objects.all()
	
	return render(request, 'nosotros.html',context={'datos':productos})

def galeria(request):
	productos= Producto.objects.all()
	
	return render(request, 'galeria.html',context={'datos':productos})

def administracion(request):
	productos= Producto.objects.all()
	
	return render(request, 'administracion.html',context={'datos':productos})

@login_required
def crear(request):
    if request.method=="POST":
        productoform=ProductoForm(request.POST,request.FILES)
        if productoform.is_valid():
            productoform.save()     #similar al insert en función
            return redirect ('administracion')
    else:
        productoform=ProductoForm()
    return render (request, 'crear.html', {'productoform': productoform})

def mostrar(request):
	productos= Producto.objects.all()
	
	return render(request, 'mostrar.html',context={'datos':productos})

@login_required
def eliminar(request, producto_id): 
    productoEliminada = Producto.objects.get(idProducto=producto_id) #similar a select * from... where...
    productoEliminada.delete()
    return redirect ('administracion')

@login_required
def modificar(request, producto_id): 
    productoModificada = Producto.objects.get(idProducto=producto_id) # Buscamos el objeto
    
    if request.method == "POST":
        formulario = ProductoForm(data=request.POST, instance=productoModificada)
        if formulario.is_valid():
            formulario.save()
            return redirect('administracion')
    else:
        # Crear el formulario con el atributo readonly
        form = ProductoForm(instance=productoModificada)
        form.fields['idProducto'].widget.attrs['readonly'] = 'readonly'

    datos = {
        'form': form
    }
    
    return render(request, 'modificar.html', datos)


def mostrar(request):
    productos = Producto.objects.all()
    datos={
        'productos':productos
    }
    return render(request, 'mostrar.html', datos)


def webpay_plus_create(request):
    if request.method == 'GET':
        buy_order = str(random.randrange(1000000, 99999999))
        session_id = str(random.randrange(1000000, 99999999))
        amount = random.randrange(10000, 1000000)
        return_url = request.build_absolute_uri('/webpay-plus/commit')

        create_request = {
            "buy_order": buy_order,
            "session_id": session_id,
            "amount": amount,
            "return_url": return_url
        }

        response = Transaction().create(buy_order, session_id, amount, return_url)

        return render(request, 'webpay/plus/create.html', {'request': create_request, 'response': response})

def webpay_plus_commit(request):
    if request.method == 'GET':
        token = request.GET.get("token_ws")
        if token is None:
            return HttpResponseBadRequest("El parámetro 'token_ws' es requerido en la URL.")

        print("commit for token_ws: {}".format(token))

        response = Transaction().commit(token=token)
        print("response: {}".format(response))

        return render(request, 'webpay/plus/commit.html', {'token': token, 'response': response})
    elif request.method == 'POST':
        token = request.POST.get("token_ws")
        print("commit error for token_ws: {}".format(token))
        response = {
            "error": "Transacción con errores"
        }

        return render(request, 'webpay/plus/commit.html', {'token': token, 'response': response})

def webpay_plus_commit_error(request):
    # Lógica para manejar errores en la transacción de pago
    return HttpResponse("Error en la transacción de pago")

def webpay_plus_refund(request):
    if request.method == 'POST':
        token = request.POST.get("token_ws")
        amount = request.POST.get("amount")
        print("refund for token_ws: {} by amount: {}".format(token, amount))

        try:
            response = Transaction().refund(token, amount)
            print("response: {}".format(response))

            return render(request, "webpay/plus/refund.html", {'token': token, 'amount': amount, 'response': response})
        except TransbankError as e:
            print(e.message)

def webpay_plus_refund_form(request):
    # Lógica para mostrar el formulario de reembolso
    return render(request, 'webpay/plus/refund-form.html')

def show_create(request):
    # Lógica para mostrar el formulario de estado
    return render(request, 'webpay/plus/status-form.html')

def status(request):
    token_ws = request.POST.get('token_ws')
    tx = Transaction()
    resp = tx.status(token_ws)
    return render(request, 'webpay/plus/status.html', {'response': resp, 'token': token_ws, 'req': request.POST})

# Create your views here.



def agregar_producto(request,id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(idProducto=id)
    carrito_compra.agregar(producto=producto)
    return redirect('mostrar')

def eliminar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(idProducto=id)
    carrito_compra.eliminar(producto=producto)
    return redirect('mostrar')

def restar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(idProducto=id)
    carrito_compra.restar(producto=producto)
    return redirect('mostrar')

def limpiar_carrito(request):
    carrito_compra= Carrito(request)
    carrito_compra.limpiar()
    return redirect('mostrar')    


def generarBoleta(request):
    if request.method == 'GET':
        # Verificar si el carrito está vacío
        if not request.session.get('carrito'):
            return render(request, 'webpay/plus/error.html', {'error': 'El carrito está vacío'})
        
        # Generar Boleta
        precio_total = 0
        for key, value in request.session['carrito'].items():
            precio_total += int(value['precio']) * int(value['cantidad'])
        
        boleta = Boleta(total=precio_total)
        boleta.save()
        
        productos = []
        for key, value in request.session['carrito'].items():
            producto = Producto.objects.get(idProducto=value['producto_id'])
            cant = value['cantidad']
            subtotal = cant * int(value['precio'])
            detalle = detalle_boleta(id_boleta=boleta, id_producto=producto, cantidad=cant, subtotal=subtotal)
            detalle.save()
            productos.append(detalle)
        
        # Guardar detalles de la boleta en la sesión
        request.session['boleta'] = boleta.id_boleta
        
        # Limpiar el carrito
        carrito = Carrito(request)
        carrito.limpiar()

        # Iniciar Transacción con Webpay Plus
        buy_order = str(random.randrange(1000000, 99999999))
        session_id = str(random.randrange(1000000, 99999999))
        amount = boleta.total
        return_url = request.build_absolute_uri('/webpay-plus/commit')

        create_request = {
            "buy_order": buy_order,
            "session_id": session_id,
            "amount": amount,
            "return_url": return_url
        }

        try:
            response = Transaction().create(buy_order, session_id, amount, return_url)
            return render(request, 'webpay/plus/create.html', {'request': create_request, 'response': response})
        except Exception as e:
            # Manejo de errores
            return render(request, 'webpay/plus/error.html', {'error': str(e)})
    else:
        # Método HTTP no permitido
        return render(request, 'webpay/plus/error.html', {'error': 'Método HTTP no permitido'})
    







class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoList(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class BoletaList(generics.ListCreateAPIView):
    queryset = Boleta.objects.all()
    serializer_class = BoletaSerializer

class BoletaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Boleta.objects.all()
    serializer_class = BoletaSerializer

class DetalleBoletaList(generics.ListCreateAPIView):
    queryset = detalle_boleta.objects.all()
    serializer_class = DetalleBoletaSerializer

class DetalleBoletaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = detalle_boleta.objects.all()
    serializer_class = DetalleBoletaSerializer