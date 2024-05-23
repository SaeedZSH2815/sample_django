from django.db import models

# Create your models here.

class Todo(models.Model):
    title=models.CharField(default='', max_length=300,)
    content=models.TextField(default='')
    priority=models.IntegerField(default=1)
    isdone= models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return super().__str__()      
    
    class Meta:
        db_table = 'todos'
        managed = True
    
