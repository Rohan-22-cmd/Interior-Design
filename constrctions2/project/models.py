from django.db import models
from django.core.exceptions import ValidationError

class ConstructionProject(models.Model):
    project_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='project/', blank=True, null=True, verbose_name="Project Image")
    
    def __str__(self):
        return self.project_name

    def project_duration(self):
        return (self.end_date - self.start_date).days

    def clean(self):        
       
        if self.budget <= 0:
            raise ValidationError({'budget': 'Budget must be greater than 0.'})



class Consultation(models.Model):
    PLATFORM_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('google_meet', 'Google Meet'),
        ('zoom', 'Zoom'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    profession = models.CharField(max_length=100)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Consultation with {self.name} on {self.date} at {self.time}"
