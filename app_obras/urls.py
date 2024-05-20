from django.urls import path, include
from app_obras.views import *

urlpatterns = [
    path('', index,name='index'),
    path('nosotros.html', nosotros,name='nosotros'),
    path('galeria.html', galeria,name='galeria'),
    path('administracion.html', administracion,name='administracion'),
    path('crear.html', crear,name='crear'),
    path('mostrar.html', mostrar,name='mostrar'),
    path('eliminar/<producto_id>', eliminar, name="eliminar"),
    path('modificar/<producto_id>', modificar, name="modificar"),


    path('generarBoleta/', generarBoleta,name="generarBoleta"),
    path('agregar/<id>', agregar_producto, name="agregar"),
    path('eliminar/<id>', eliminar_producto, name="eliminar"),
    path('restar/<id>', restar_producto, name="restar"),
    path('limpiar/', limpiar_carrito, name="limpiar"),
    path('webpay-plus/create', webpay_plus_create, name='webpay_plus_create'),
    path('webpay-plus/commit', webpay_plus_commit, name='webpay_plus_commit'),
    path('webpay-plus/commit-error', webpay_plus_commit_error, name='webpay_plus_commit_error'),
    path('webpay-plus/refund', webpay_plus_refund, name='webpay_plus_refund'),
    path('webpay-plus/refund-form', webpay_plus_refund_form, name='webpay_plus_refund_form'),
    path('webpay-plus/status-form', show_create, name='webpay_plus_status_form'),
    path('webpay-plus/status', status, name='webpay_plus_status'),

    #URLS de la api creada para los datos de los productos
    path('api/categorias/', CategoriaList.as_view(), name='categoria-list'),
    path('api/categorias/<int:pk>/', CategoriaDetail.as_view(), name='categoria-detail'),
    path('api/productos/', ProductoList.as_view(), name='producto-list'),
    path('api/productos/<str:pk>/', ProductoDetail.as_view(), name='producto-detail'),
    path('api/boletas/', BoletaList.as_view(), name='boleta-list'),
    path('api/boletas/<int:pk>/', BoletaDetail.as_view(), name='boleta-detail'),
    path('api/detalles_boleta/', DetalleBoletaList.as_view(), name='detalle_boleta-list'),
    path('api/detalles_boleta/<int:pk>/', DetalleBoletaDetail.as_view(), name='detalle_boleta-detail'),
    
]