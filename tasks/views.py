from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Crear un nuevo usuario
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, password=password1)
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Las contraseñas no coinciden'
            })


# Listar las tareas pendientes, es la pagina principal de la aplicacion
@login_required
def tasks(request):
    # Filtramos las tareas por usuario y por fecha de completado, ordenamos por fecha de creacion
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True).order_by('-created')
    return render(request, 'tasks.html', {
        'tasks': tasks
    })


# Presentacion del proyecto en la pagina principal
def home(request):
    return render(request, 'home.html', {
        'user': request.user  # Pasamos el valor de la variable user a la plantilla
    })


# Cerrar sesion
@login_required
def signout(request):
    logout(request)
    return redirect('home')


# Iniciar sesion
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm

        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'El usuario o la contraseña no son correctos'

            })
        else:
            login(request, user)
            return redirect('tasks')


# Crear una nueva tarea, manejo de errores con try y except
@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            newtask = TaskForm(request.POST)
            newtask = newtask.save(commit=False)
            newtask.user = request.user
            newtask.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Datos incorrectos'
            })


# Mostrar el detalle de una tarea y permitir editarla
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        try:
            form = TaskForm(request.POST, instance=task)
            task.updated_at = timezone.now()
            form.save()
            # Mensaje de exito al actualizar una tarea, la enviamos para usarla en nuestro template tasks.html
            messages.success(request, 'La tarea con ID #' + str(task_id) + ' se ha actualizado correctamente.')
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Datos incorrectos'
            })


# Marcar una tarea como completada, guardar fecha de completado y ocultar de la lista de tareas
@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


# Listar las tareas completadas en la misma pagina de tasks.html pero con un filtro
@login_required
def completelist(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-created')
    return render(request, 'tasks.html', {
        'tasks': tasks
    })


# Eliminar una tarea
@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
