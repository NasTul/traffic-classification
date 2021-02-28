from django.db import models

# Create your models here.
class uploadfile(models.Model):
    ID = models.AutoField(primary_key=True)
    uploadlocation = models.FileField(upload_to='./upload')
    class Meta:
        db_table = "uploadfile"



class graphfile(models.Model):
    ID = models.AutoField(primary_key=True)
    graphlocation = models.CharField(max_length=256)
    graphname = models.CharField(max_length=256)
    class Meta:
        db_table = "graphfile"	


class graphdata(models.Model):
    ID = models.AutoField(primary_key=True)
    graphdata = models.TextField()
    graphname = models.CharField(max_length=256)
    class Meta:
        db_table = "graphdata"	


class fileinfo(models.Model):
    ID = models.AutoField(primary_key=True)
    node_numbers =models.CharField(max_length=10)
    edges_numbers = models.CharField(max_length=10)
    anomalous_ndoes = models.CharField(max_length=10)
    anomalous_edges = models.CharField(max_length=10)
    
    class Meta:
        db_table = "fileinfo"  
