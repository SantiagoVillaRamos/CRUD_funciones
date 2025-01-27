from django import forms 

# formulario con el campo name y logica para validar que el nombre no sea name
class DataFormName(forms.Form):
    # campo name
    name = forms.CharField(
        # widget que se encarga de mostrar el campo de texto
        max_length=30,
        widget=forms.TextInput(attrs={'id':'name_id', 'class':'form-control', 'placeholder':'Nombre'}), 
        label='Nombre', 
    )
        
    # funcion que se encarga de validar que el nombre no sea name
    def clean_name(self): 
        # obtener el nombre
        name = self.cleaned_data.get('name')
        # si el nombre es name, se lanza un error
        if name == 'name':
            # lanzar un error
            raise forms.ValidationError('Coloca un nombre de verdad')
        # retornar el nombre
        return name
    
# formulario cedula
class CedulaForms(forms.Form):
    # campo cedula
    cedula = forms.DecimalField(
        # widget que se encarga de mostrar el campo de texto
        widget=forms.NumberInput(attrs={'id':'cedula_id', 'class':'form-control', 'placeholder':'ingrese su cedula'}), 
        label='cedula', 
        max_digits=10,
        error_messages={'max_digits':'La cedula debe tener 10 digitos'}
    )
    

# formulario que tiene el nombre y el correo y los valida
class Emailperson(forms.Form):
    # campo email
    email = forms.EmailField(
        # widget que se encarga de mostrar el campo de texto
        widget=forms.EmailInput(attrs={'id':'email_id','class':'form-control', 'placeholder':'Correo'}), 
        label='correo', 
    )
    # campo confirmacion de correo
    confirm_email = forms.EmailField(
        # widget que se encarga de mostrar el campo de texto
        widget=forms.EmailInput(attrs={'id':'confirm_email_id','class':'form-control', 'placeholder':'Confirmacion correo'}), 
        label='confirmacion correo', 
        
    )
    
    # funcion que valida si el correo no termina en @gmail.com o @hotmail.com da un error
    def clean_email(self):
        # obtener el correo
        email = self.cleaned_data.get('email')
        # si el correo no termina en @gmail.com o @hotmail.com, se lanza un error
        if not email.endswith('@gmail.com') and not email.endswith('@hotmail.com'):
            raise forms.ValidationError('incorrecto, debe de terminar en "@gmail.com" o "@hotmail.com"')
        # retornar el correo
        return email
    
    # funcion que compara que si los correos coinciden
    def clean(self):
        # obtener los datos limpios
        cleaned_data = super().clean()
        # obtener el correo
        email = cleaned_data.get('email')
        # obtener la confirmacion de correo
        confirm_email = cleaned_data.get('confirm_email')
        # si el correo y la confirmacion de correo existen
        if email and confirm_email:
            # si los correos no coinciden, se lanza un error
            if email != confirm_email:
                raise forms.ValidationError('¡Los correos no coinciden, intentalo de nuevo')
            # retornar los datos limpios
        return cleaned_data
    
# formulario que valida las contraseñas 
class PasswordPersona(forms.Form):
    # campo contraseña
    password = forms.CharField(
        # widget que se encarga de mostrar el campo
        widget=forms.PasswordInput(attrs={'id':'password_id','class':'form-control', 'placeholder':'Contraseña'}), 
        label='contraseña', 
        help_text='La contraseña no puede ser igual al nombre, No se permiten numeros, No puede comenzar con admin ni terminar con admin'
    )
    # campo confirmacion de contraseña
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'id':'password_confirm_id','class':'form-control', 'placeholder':'Confirmacion contraseña'}), 
        label='confirma tu contraseña',
    )
    
    # funcion que valida las contraseñas 
    def clean_password(self):
        # obtener la contraseña
        password = self.cleaned_data.get('password')
        # si la contraseña existe
        if password:
            # si la contraseña es son numeros, se lanza un error
            if password.isdigit():
                raise forms.ValidationError('No se permiten numeros en la contraseña')
            # si la contraseña comienza con admin, se lanza un error
            elif password.startswith('admin'):
                raise forms.ValidationError('La contraseña comienza con admin')
            # si la contraseña termina con admin, se lanza un error
            elif password.endswith('admin'):
                raise forms.ValidationError('La contraseña finaliza en admin') 
        # retornar la contraseña
        return password
    
    # funcion que compara la contraseña y la confirmacion de contraseña 
    def clean_password_confirm(self):
        # obtener la contraseña
        password = self.cleaned_data.get('password')
        # obtener la confirmacion de contraseña
        password_confirm = self.cleaned_data.get('password_confirm')
        # si la contraseña y la confirmacion de contraseña existen
        if password and password_confirm:
            # si la contraseña y la confirmacion de contraseña no coinciden, se lanza un error
            if password != password_confirm:
                raise forms.ValidationError('Las contraseñas no coinciden')
        # retornar la confirmacion de
        return password_confirm
    
# formulario que hereda de los formularios anteriores y tiene los campos de la persona y la contraseña los los valida y tiene un widget personalizado
class FormularyPerson(DataFormName, CedulaForms, Emailperson, PasswordPersona):
    
    # sobreescribimos el constructor para personalizar los widgets
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # iteramos sobre todos los campos del formulario
        for field_name, field in self.fields.items():
            # asignamos widget personalizados con el atributo required
            field.widget.attrs.update({
                'class':'form-control',
                'required':'required',
                'placeholder':field.label
            })  
    
    # funcion que valida que la contraseña no sea igual al nombre
    def clean(self):
        # obtener los datos limpios
        cleaned_data = super().clean()
        # obtener el nombre
        name = cleaned_data.get('name')
        # obtener la contraseña
        password = cleaned_data.get('password')
        # si el nombre y la contraseña existen  y son iguales, se lanza un error    
        if name and password and name == password:
            raise forms.ValidationError('La contrasela es igual al nombre')
        # retornar los datos limpios
        return cleaned_data
    
# formulario que actualiza los datos de la persona
class FormularyPersonUpdate(DataFormName, CedulaForms, Emailperson):
    pass