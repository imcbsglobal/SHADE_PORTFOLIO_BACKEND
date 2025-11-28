from django.db import models
from django.contrib.auth.models import User as DjangoUser
import os

# --------------------- VISITOR/USER MODEL ---------------------
class User(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# --------------------- LOGIN HISTORY MODEL ---------------------
class LoginHistory(models.Model):
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, related_name='shade_login_history', null=True, blank=True)
    username = models.CharField(max_length=150)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='success')

    class Meta:
        ordering = ['-login_time']
        verbose_name_plural = "Login Histories"

    def __str__(self):
        return f"{self.username} - {self.login_time.strftime('%Y-%m-%d %H:%M:%S')}"


# --------------------- GALLERY - SMILES MODEL ---------------------
def smiles_upload_path(instance, filename):
    return f"gallery/smiles/{filename}"

class Smile(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=smiles_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)


# --------------------- GALLERY - OUR CLIENTS MODEL ---------------------
def clients_upload_path(instance, filename):
    return f"gallery/clients/{filename}"

class OurClient(models.Model):
    MEDIA_TYPE_CHOICES = [
        ("image", "Image"),
        ("video", "Video"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    
    media_file = models.FileField(upload_to=clients_upload_path, blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.media_type})"

    def delete(self, *args, **kwargs):
        if self.media_file:
            if os.path.isfile(self.media_file.path):
                os.remove(self.media_file.path)
        super().delete(*args, **kwargs)


# --------------------- GALLERY - CEREMONIAL MODEL ---------------------
def ceremonial_upload_path(instance, filename):
    return f"gallery/ceremonial/{filename}"

class Ceremonial(models.Model):
    MEDIA_TYPE_CHOICES = [
        ("image", "Image"),
        ("video", "Video"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    
    media_file = models.FileField(upload_to=ceremonial_upload_path, blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.media_type})"

    def delete(self, *args, **kwargs):
        if self.media_file:
            if os.path.isfile(self.media_file.path):
                os.remove(self.media_file.path)
        super().delete(*args, **kwargs)


# --------------------- DEMONSTRATIONS MODEL ---------------------
def demonstration_upload_path(instance, filename):
    return f"demonstrations/{filename}"

class Demonstration(models.Model):
    MEDIA_TYPE_CHOICES = [
        ("image", "Image"),
        ("video", "Video"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    
    media_file = models.FileField(upload_to=demonstration_upload_path, blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.media_type})"

    def delete(self, *args, **kwargs):
        if self.media_file:
            if os.path.isfile(self.media_file.path):
                os.remove(self.media_file.path)
        super().delete(*args, **kwargs)