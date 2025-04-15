from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
# Create your models here.


# DRF, Django rest Framework
class CustomUser3(AbstractUser):  
    email = models.EmailField(unique=True)  # Email obligatoire et unique
    is_verified = models.BooleanField(default=False)  # Vérification de l'utilisateur

    def __str__(self):
        return self.username
    
class Library(models.Model):
    id_lib = models.AutoField(primary_key=True)
    Name=models.CharField(max_length=100)

    class Meta:
        verbose_name = "Bibliothèque"
        verbose_name_plural = "Bibliothèques"


     
class Article(models.Model):
    titre=models.CharField(max_length=100)
    contenu=models.TextField()
    date_publication= models.DateTimeField(auto_now_add=True)
    pdf_path=models.CharField(max_length=255, blank=True, null=True)
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="articles",default=1)


    def __str__(self):
        return self.titre   
    




# Gestionnaire personnalisé pour le modèle utilisateur
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
    

    

# Modèle utilisateur personnalisé
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

   

    def __str__(self):
        return self.email



 