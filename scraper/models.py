from django.db import models

# Create your models here.

class Contact(models.Model):

    name=models.CharField(max_length=50)
    email=models.EmailField()
    message=models.TextField()
    date=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name