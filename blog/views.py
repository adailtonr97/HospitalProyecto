from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from .models import Paciente, Doctor, Cita
from .forms import PostForm1, PostForm2
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required



def principal(request):
    return render(request, 'blog/principal.html')


def base(request):
    return render(request, 'blog/base.html')

def base2(request):
    return render(request, 'blog/base2.html')


def lista(request):
    pac = Paciente.objects.order_by('fecha_creacion')
    return render(request, 'blog/listar.html', {'pac': pac})

def lista2(request):
    doc = Doctor.objects.filter(fecha_publicacion2__lte=timezone.now()).order_by('fecha_publicacion2')
    return render(request, 'blog/listar2.html', {'doc': doc})


def detalle(request, pk):
    det = get_object_or_404(Paciente, pk=pk)
    return render(request, 'blog/detalle.html', {'det': det})

def detalle2(request, pk):
    det = get_object_or_404(Doctor, pk=pk)
    return render(request, 'blog/detalle2.html', {'det': det})


@login_required
def nuevo(request):
        if request.method == "POST":
            form = PostForm1(request.POST)
            if form.is_valid():
                paciente = Paciente.objects.create(nombre_paciente=form.cleaned_data['nombre_paciente'], direccion_paciente=form.cleaned_data['direccion_paciente'], telefono_paciente=form.cleaned_data['telefono_paciente'], correo_paciente=form.cleaned_data['correo_paciente'], sintomas_paciente=form.cleaned_data['sintomas_paciente'] )
                for doctor_id in request.POST.getlist('doctores'):
                    citas = Cita(doctor_id=doctor_id, paciente_id = paciente.id)
                    citas.save()
                    messages.add_message(request, messages.SUCCESS, 'Cita archivada correctamente')
        else:
            form = PostForm1()
        return render(request, 'blog/editar.html', {'form': form})

@login_required
def nuevo2(request):
        if request.method == "POST":
            form = PostForm2(request.POST)
            if form.is_valid():
                p = form.save(commit=False)
                p.save()
                return redirect('detalle2', pk=p.pk)
        else:
            form = PostForm2()
        return render(request, 'blog/editar2.html', {'form': form})

@login_required
def editar(request, pk):
        post = get_object_or_404(Paciente, pk=pk)
        if request.method == "POST":
            form = PostForm1(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect('lista')
        else:
            form = PostForm1(instance=post)
        return render(request, 'blog/editar.html', {'form': form})

@login_required
def editar2(request, pk):
        post = get_object_or_404(Doctor, pk=pk)
        if request.method == "POST":
            form = PostForm2(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect('detalle2', pk=post.pk)
        else:
            form = PostForm2(instance=post)
        return render(request, 'blog/editar2.html', {'form': form})


@login_required
def paciente(request, pk):
    pu = get_object_or_404(Paciente, pk=pk)
    pu.publish()
    return redirect('detalle', pk=pk)

@login_required
def doctor(request, pk):
    do = get_object_or_404(Doctor, pk=pk)
    do.publish()
    return redirect('detalle2', pk=pk)



def publish(self):
    self.fecha_publicacion = timezone.now()
    self.save()

def publish2(self):
    self.fecha_publicacion2 = timezone.now()
    self.save()


@login_required
def eliminar(request, pk):
    rv = get_object_or_404(Paciente, pk=pk)
    rv.delete()
    return redirect('/')

@login_required
def eliminar2(request, pk):
    rv = get_object_or_404(Doctor, pk=pk)
    rv.delete()
    return redirect('/')
