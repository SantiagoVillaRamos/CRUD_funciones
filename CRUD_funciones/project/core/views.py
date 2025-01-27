from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import FormularyPerson, PasswordPersona, FormularyPersonUpdate
from .models import Profile, DatosPerson
from django.core.paginator import Paginator
# Create your views here.

# funcion encargada del registro y validacion y guardar en la base de datos
def confirmation_email(request):
    # si el metodo es POST
    if request.method == 'POST':
        # se crea el formulario
        form = FormularyPerson(request.POST)
        # si el formulario es valido
        if form.is_valid():
            # guardar nombre y cedula en DatosPerson()
            # crear el registro en DatosPerson
            datos_person = DatosPerson.objects.create(
                name = form.cleaned_data['name'],
                cedula = form.cleaned_data['cedula'],
            )
            # crear el registro en Profile, asociandolo a datos_person
            # y guardando el email y contraseña
            Profile.objects.create(
                perfil = datos_person,
                email = form.cleaned_data['email'],
                confirm_email = form.cleaned_data['confirm_email'],
                password = form.cleaned_data['password'],
                password_confirm = form.cleaned_data['password_confirm'],
            )
            # redireccionar a la lista de personas
            return redirect('lists_person')
    else:
        # si no es un metodo POST, se crea el formulario
        form = FormularyPerson()
        # renderizar el template y pasar el formulario al contexto
    return render(request, 'pages/formulary_register.html', {'form': form})



# funcion que muestra los datos del usuario
def person_data(request, id):
    # obtener el objeto de la base de datos
    model = get_object_or_404(Profile.objects.select_related('perfil'), id=id)
    # renderizar el template y pasar el objeto al contexto
    return render(request, 'pages/person_data.html', {'model':model})



# vista que muestra la lista de personas y la paginiacion
def lists_person(request):
    # Obtenemos todas las personas de la base de datos
    persons = Profile.objects.select_related('perfil').all()
    # Creamos un paginador con las personas, mostrando 10 por página
    paginator = Paginator(persons, 4)
    # Obtenemos el número de página desde los parámetros de la URL
    page_number = request.GET.get('page')
    # Obtenemos el objeto de la página actual
    page_obj = paginator.get_page(page_number)
    # Renderizamos el template y pasamos el objeto de la página al contexto
    return render(request, 'pages/list_person.html', {'page_obj': page_obj}) 



# funcion encargada de actualizar datos
def updated_person(request, updated_id):
    # obtener el objeto de la base de datos
    person = get_object_or_404(Profile.objects.select_related('perfil'), id=updated_id)
    
    # valores iniciales
    initial_data = {
        'name': person.perfil.name,
        'cedula': person.perfil.cedula,
        'email': person.email,
        'confirm_email': person.confirm_email,
    }
    # si el metodo es POST
    if request.method == 'POST':
        form = FormularyPersonUpdate(request.POST, initial=initial_data )
        # si el formulario es valido
        if form.is_valid():
            # si se han realizado cambios
            if form.has_changed():
                # actualizar la instancia de la base de datos DatosPerson
                datos_person = person.perfil
                datos_person.name = form.cleaned_data['name']
                datos_person.cedula = form.cleaned_data['cedula']
                # guardar los cambios
                datos_person.save()
                # actualizar la instancia de la base de datos Profile
                person.email = form.cleaned_data['email']
                person.confirm_email = form.cleaned_data['confirm_email']
                #guardar los cambios
                person.save()
                # redirecciona a la lista de personas
                return redirect('lists_person')
            else:
                # si no se han realizado cambios
                return render(request, 'pages/updated_person.html', {
                    'form': form, 
                    'person': person, 
                    'message':'No se han realizado cambios.'
                })
    else:
        # si no es un metodo POST, se crea el formulario con los valores iniciales
        form = FormularyPerson(initial=initial_data)
    # renderizar el template y pasar el formulario y el objeto al contexto
    return render(request, 'pages/updated_person.html', {'form': form, 'person': person})



# vista encargada de actualizar la contraseña
def password_updated(request, updated_id):
    # obtener el objeto de la base de datos
    person = get_object_or_404(Profile.objects.select_related('perfil'), id=updated_id)
    # valores iniciales
    inicial_data = {
        'password':person.password,
        'password_confirm':person.password_confirm,
    }
    # si el metodo es POST
    if request.method == 'POST':
        # se crea el formulario
        form = PasswordPersona(request.POST, initial=inicial_data)
        # si el formulario es valido
        if form.is_valid():
            # si se han realizado cambios
            if form.has_changed():
                # actualizar la contraseña
                person.password = form.cleaned_data['password']
                person.password_confirm = form.cleaned_data['password_confirm']
                # guardar los cambios
                person.save()
                # redireccionar a la lista de personas
                return redirect('lists_person')
            else:
                # si no se han realizado cambios
                return render(request, 'pages/password_updated.html',{
                    'form': form,
                    'person': person,
                    'message': 'No se han realizado cambios'
                })
    else:
        # si no es un metodo POST, se crea el formulario con los valores iniciales
        form = PasswordPersona(initial=inicial_data)
    # renderizar el template y pasar el formulario y el objeto al contexto
    return render(request, 'pages/password_updated.html', {'form': form, 'person': person})



# funcion que elimina los datos
def delete_person(request, id):
    # obtener el objeto de la base de datos
    person = get_object_or_404(Profile.objects.select_related('perfil'), id=id)
    # si el metodo es POST
    if request.method == 'POST':
        # eliminar el objeto de la base 
        person.delete()
        # redireccionar a la lista de personas
        return redirect('lists_person')
    # renderizar el template y pasar el objeto al contexto
    return render(request, 'pages/delete_person.html', {'person': person})

    