from django.db import models

# Create your models here.



class Vessels_in_Port(models.Model):
    run_date = models.DateField('Run Date')
    vessel_name = models.CharField('Vessel Name',max_length=120)
    terminal = models.CharField('Terminal Name',max_length=120)

    
    class Meta:
        unique_together  = [['vessel_name','run_date']]
   