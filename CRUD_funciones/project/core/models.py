from django.db import models

# clase que tiene los datos de la persona
class DatosPerson(models.Model):
    name = models.CharField(max_length=30, verbose_name='nombre de la persona')
    cedula = models.IntegerField(verbose_name='cedula', null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='fecha de creacion')
    updated = models.DateTimeField(auto_now=True, verbose_name='fecha de actualizacion')
    
    # clase meta
    class Meta:
        verbose_name = 'Dato persona'
        verbose_name_plural = 'Datos personas'
        ordering = ['-created']
        
    def __str__(self):
        return self.name 
    
# clase perfil
class Profile(models.Model):
    perfil = models.OneToOneField(DatosPerson, on_delete=models.CASCADE)
    email = models.EmailField(verbose_name='email')
    confirm_email = models.EmailField(verbose_name='confirmacion correo')
    password = models.CharField(max_length=20, verbose_name='contraseña')
    password_confirm = models.CharField(max_length=20, verbose_name='confirmar contraseña', null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='fecha de creacion')
    updated = models.DateTimeField(auto_now=True, verbose_name='fecha de actualizacion')
    
    # clase meta
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        ordering = ['-created']
        
    def __str__(self):
        return f'{self.perfil.name}'
