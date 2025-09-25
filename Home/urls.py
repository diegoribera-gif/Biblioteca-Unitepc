from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('bibliotecario_dashboard/', views.bibliotecario_dashboard, name='bibliotecario_dashboard'),
    path('estudiante/<str:username>/', views.estudiante_dashboard, name='estudiante_dashboard'),

    path('registrar_libro/', views.registrar_libro, name='registrar_libro'),
    path('editar_libro/<int:libro_id>/', views.editar_libro, name='editar_libro'),
    path('eliminar_libro/<int:libro_id>/', views.eliminar_libro, name='eliminar_libro'),
    path('supervisar_prestamos/', views.supervisar_prestamos, name='supervisar_prestamos'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),

     path('registrar_prestamo/', views.registrar_prestamo, name='registrar_prestamo'),
    path('libros_prestados/', views.libros_prestados, name='libros_prestados'),
    path('marcar_devolucion/', views.marcar_devolucion, name='marcar_devolucion'),
    path('consultar_disponibilidad/', views.consultar_disponibles, name='consultar_disponibilidad'),

     path('estudiante/<str:username>/registrar/', views.registrar_prestamo_estudiante, name="registrar_prestamo_estudiante"),
    path('estudiante/<str:username>/consultar/', views.consultar_disponibilidad, name="consultar_disponibilidad"),
    path('estudiante/<str:username>/registrar_prestamo/', 
         views.registrar_prestamo_estudiante, 
         name='registrar_prestamo_estudiante'),

    path('consultar_disponibilidad/', views.consultar_disponibilidad, name='consultar_disponibilidad'),

    

]
