from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Create your models here.

class Agency(models.Model):
    agencyname = models.CharField(max_length = 200)
    registration_no = models.IntegerField()
    primary_location = models.CharField(max_length=300)
    description = models.CharField(max_length=300, default ='The right agency for you')
    agency_logo = CloudinaryField(blank=True)
    
    
    def __str__(self):
        return self.agencyname

    class Meta:
        ordering = ['agencyname']
        verbose_name_plural = 'agencies'

    @classmethod
    def search_by_name(cls,search_term):
        agency = cls.objects.filter(agenncyname__icontains=search_term)
        return agency
    