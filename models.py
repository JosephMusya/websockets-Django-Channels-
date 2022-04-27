from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Values(models.Model):
    status = (
        ('Checked','Checked'),
        ('Scanned','Scanned'),
        ('Screened','Screened'),
        ('Make-up','Make-up'),
        ('To Loading','To Loading'),
        ('Loaded','Loaded')
    )
    baggage_status = models.CharField(max_length=50,
                              choices=status,
                              default='Checked')
    #status = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.baggage_status +" > "+ self.user.username