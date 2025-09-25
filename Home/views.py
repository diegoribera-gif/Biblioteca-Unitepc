from django.shortcuts import render, redirect, get_object_or_404
from .forms import LibroForm
from .models import Libro
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Libro, Prestamo, Devolucion
from datetime import date
from .models import Notificacion
from .models import Libro, Prestamo
from django.utils import timezone



def inicio(request):
    return render(request, 'inicio.html')


USUARIOS = {
    "Admin_Biblioteca": {"password": "admin123", "rol": "administrador"},
    "Bibliotecario_Unitepc": {"password": "bibliotecario123", "rol": "bibliotecario"}
}

def inicio(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username in USUARIOS and USUARIOS[username]["password"] == password:
            rol = USUARIOS[username]["rol"]
            if rol == "administrador":
                return redirect("admin_dashboard")
            elif rol == "bibliotecario":
                return redirect("bibliotecario_dashboard")
        else:
            # Si no es administrador ni bibliotecario, permitimos el ingreso como estudiante
            return redirect("estudiante_dashboard", username=username)

    return render(request, "inicio.html")
    

# Panel administrador
def admin_dashboard(request):
    libros = Libro.objects.all()
    return render(request, "admin_dashboard.html", {"libros": libros})


# Registrar libro
def registrar_libro(request):
    if request.method == "POST":
        if "guardar" in request.POST:
            titulo = request.POST.get("titulo")
            editorial = request.POST.get("editorial")
            autor = request.POST.get("autor")
            cantidad = request.POST.get("cantidad")
            categoria = request.POST.get("categoria")

            Libro.objects.create(
                titulo=titulo,
                editorial=editorial,
                autor=autor,
                cantidad=cantidad,
                categoria=categoria
            )
            messages.success(request, "Libro agregado correctamente")
            return redirect("admin_dashboard")

        elif "cancelar" in request.POST:
            messages.warning(request, "Cancelado exitosamente")
            return redirect("admin_dashboard")

    return render(request, "registrar_libro.html")


# Editar libro
def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if request.method == "POST":
        libro.titulo = request.POST.get("titulo")
        libro.editorial = request.POST.get("editorial")
        libro.autor = request.POST.get("autor")
        libro.cantidad = request.POST.get("cantidad")
        libro.categoria = request.POST.get("categoria")
        libro.save()
        messages.success(request, "Libro editado correctamente")
        return redirect("admin_dashboard")

    return render(request, "editar_libro.html", {"libro": libro})


# Eliminar libro
def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    libro.delete()
    messages.error(request, "Libro eliminado correctamente")
    return redirect("admin_dashboard")


# Supervisar préstamos
def supervisar_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, "supervisar_prestamos.html", {"prestamos": prestamos})


# Cerrar sesión (solo limpia y vuelve al inicio)
def cerrar_sesion(request):
    return redirect("inicio")



def bibliotecario_dashboard(request):
    libros = Libro.objects.all()
    return render(request, "bibliotecario_dashboard.html", {"libros": libros})


def registrar_prestamo(request):
    if request.method == "POST":
        libro_obj = Libro.objects.filter(titulo=request.POST.get("titulo")).first()
        if libro_obj:
            Prestamo.objects.create(
                codigo_estudiante=request.POST.get("codigo"),
                nombre_estudiante=request.POST.get("nombre"),
                libro=libro_obj,
                fecha_prestamo=request.POST.get("fecha_prestamo"),
                fecha_devolucion=request.POST.get("fecha_devolucion"),
            )
            # Crear notificación para bibliotecario
            Notificacion.objects.create(
                mensaje=f"Nuevo préstamo: {request.POST.get('nombre')} solicitó '{libro_obj.titulo}'"
            )
            messages.success(request, "Solicitud enviada, pasa por la Biblioteca a recoger el libro")
            return redirect("estudiante_dashboard", username=request.POST.get("nombre"))
    return render(request, "registrar_prestamo.html")


def libros_prestados(request):
    prestamos = Prestamo.objects.all()
    return render(request, "libros_prestados.html", {"prestamos": prestamos})


def marcar_devolucion(request):
    if request.method == "POST":
        Devolucion.objects.create(
            codigo_estudiante=request.POST.get("codigo"),
            nombre_estudiante=request.POST.get("nombre"),
            titulo=request.POST.get("titulo"),
            fecha_devolucion=date.today(),
            estado=request.POST.get("estado"),
        )
        # marcar préstamo como devuelto
        prestamo = Prestamo.objects.filter(
            codigo_estudiante=request.POST.get("codigo"),
            titulo=request.POST.get("titulo"),
            devuelto=False
        ).first()
        if prestamo:
            prestamo.devuelto = True
            prestamo.save()
        messages.success(request, "Devolución registrada correctamente")
        return redirect("marcar_devolucion")

    devoluciones = Devolucion.objects.all()
    return render(request, "marcar_devolucion.html", {"devoluciones": devoluciones})


def consultar_disponibles(request):
    disponibilidad = None
    if request.method == "POST":
        titulo = request.POST.get("consulta_libro")
        libro = Libro.objects.filter(titulo__icontains=titulo).first()
        if libro:
            # contar préstamos no devueltos para este libro
            prestados = Prestamo.objects.filter(libro=libro, devuelto=False).count()
            disponibilidad = libro.cantidad - prestados
    return render(request, "consultar_disponibilidad.html", {"disponibilidad": disponibilidad})

# Dashboard del estudiante
def estudiante_dashboard(request, username):
    # Todos los préstamos del estudiante
    prestamos = Prestamo.objects.filter(nombre_estudiante=username)
    context = {
        "username": username,
        "prestamos": prestamos
    }
    return render(request, "estudiante_dashboard.html", context)


# Registrar préstamo desde estudiante
def registrar_prestamo_estudiante(request, username):
    libros = Libro.objects.all()
    today = timezone.now().date()

    if request.method == "POST":
        libro_id = request.POST.get("libro")
        libro = Libro.objects.get(id=libro_id)
        prestamo = Prestamo.objects.create(
            codigo_estudiante=request.POST.get("codigo"),
            nombre_estudiante=request.POST.get("nombre"),
            libro=libro,
            fecha_prestamo=request.POST.get("fecha_prestamo") or today,
            fecha_devolucion=request.POST.get("fecha_devolucion")
        )

        # Crear notificación para el bibliotecario
        Notificacion.objects.create(
            codigo_estudiante=prestamo.codigo_estudiante,
            nombre_estudiante=prestamo.nombre_estudiante,
            mensaje=f"Préstamo de libro solicitado: {prestamo.libro.titulo}"
        )

        messages.success(request, "Préstamo realizado, pasa por la Biblioteca a recoger el libro")
        return redirect("estudiante_dashboard", username=username)

    return render(request, "registrar_prestamo_estudiante.html", {
        "libros": libros,
        "today": today,
        "username": username
    })


# Consultar disponibilidad de libros
def consultar_disponibilidad(request):
    username = request.user.username
    libro = None
    disponibilidad = 0
    libros_similares = []

    if request.method == "POST":
        titulo = request.POST.get("consulta_libro", "").strip()
        autor = request.POST.get("consulta_autor", "").strip()
        editorial = request.POST.get("consulta_editorial", "").strip()

        qs = Libro.objects.all()
        if titulo:
            qs = qs.filter(titulo__icontains=titulo)
        if autor:
            qs = qs.filter(autor__icontains=autor)
        if editorial:
            qs = qs.filter(editorial__icontains=editorial)

        libro = qs.first()
        if libro:
            # Contar cantidad de libros disponibles
            prestamos_activos = Prestamo.objects.filter(libro=libro, devuelto=False).count()
            disponibilidad = libro.cantidad - prestamos_activos

            # Libros similares si no está disponible
            if disponibilidad <= 0:
                libros_similares = Libro.objects.exclude(id=libro.id)
        else:
            # Si no hay coincidencia exacta
            libros_similares = Libro.objects.all()

    return render(request, "estudiante_dashboard.html", {
        "username": username,
        "libro": libro,
        "disponibilidad": disponibilidad,
        "libros_similares": libros_similares
    })



