from django.db import models

#IMPORTANTE AGREGAR ESTO EN SETTINGS.PY 
#AUTH_USER_MODEL = 'users.User'
#ES LA RUTA Y MODELO

#para poder personalizar el modelo usuario
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioManager(BaseUserManager):

    def _create_user( self, email, username, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db) #usa la bd actual configurada
        return user

    def create_user( self, email, username, password=None, **extra_fields ):    
        return self._create_user( email, username, password, False, False, **extra_fields )

    def create_superuser( self, email, username, password=None, **extra_fields ):    
        return self._create_user( email, username, password, True, True, **extra_fields )



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField( 'Nombre de usuario', unique=True, max_length=100 )
    email = models.EmailField( 'Correo electronico', unique=True, max_length=200  )
    name = models.CharField( 'Nombres', max_length=150, blank=True, null=True)
    photo = models.ImageField('Imagen de perfil', upload_to='assets/upload', height_field=None, width_field=None, max_length=200, blank=True, null=True )
    is_active = models.BooleanField( default=True )
    is_staff = models.BooleanField( default=False )
    # enlazamos la clase usuarioManager
    objects = UsuarioManager()

    #campos unicos para este usuario 
    USERNAME_FIELD = 'username'

    #campos obliglatorios, por consola
    REQUIRED_FIELDS = ['email']
  

    def __str__(self):
        return f'{self.username}'

"""
    #AbstractBaseUser necesita estos metodos para que se pueda utilizar el modelo usuario en el administrador de django para que aparezca

    en la actualizacion video 75 se quito    

    # def has_perm(self, perm, obj=None):
    #     return True

    # def has_module_perms(self, app_label):
    #     return True        

    # @property
    # def is_staff(self):
    #     return self.usuario_administrador
"""
