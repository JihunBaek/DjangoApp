from django.db import models

# Create your models here.
class Categories(models.Model):
    Title = models.CharField(max_length=40, null=False)
    
class TagModel(models.Model):
    Title = models.CharField(max_length=20, null=False)
       
class Entries(models.Model):
    id = 0
    Title = models.CharField(max_length=80, null=False)
    Content = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    Category = models.ForeignKey(Categories)
    Tags = models.ManyToManyField(TagModel)
    Comments = models.PositiveSmallIntegerField(default=0, null=True)
    Files = models.PositiveSmallIntegerField(default=0, null=True)
    
class Comments(models.Model):
    Name = models.CharField(max_length=20, null=False)
    Password = models.CharField(max_length=20, null=False)
    Content = models.TextField(max_length=2000, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    Entry = models.ForeignKey(Entries)
    
class Files(models.Model):
    Name = models.CharField(max_length=20, null=False)
    File = models.FileField(upload_to='files')
    Entry = models.ForeignKey(Entries)