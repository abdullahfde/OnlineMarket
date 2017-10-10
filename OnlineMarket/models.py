from django.db import models



class uploadImages(models.Model):

    Image1 = models.FileField(upload_to="static\Images")

    Image2 = models.FileField(upload_to="static\Images")
    Image3 = models.FileField(upload_to="static\Images")

class ItemInformation(models.Model):
    ItemTitle=models.CharField(max_length=50)
    Price=models.FloatField()
    Description=models.CharField(max_length=1000)
    Status=models.CharField(max_length=30)
    type=models.CharField(max_length=20)
    subType=models.CharField(max_length=20)
    username=models.CharField(max_length=50)
    Date=models.CharField(max_length=50)
    ImageID=models.IntegerField()
class  recommenationDatas(models.Model):
    username=models.CharField(max_length=100)
    productId=models.IntegerField()
    visitedTime=models.IntegerField()

class contacts(models.Model):
    senderName = models.CharField(max_length=50)
    receiverName = models.CharField(max_length=50)
    senderMail = models.CharField(max_length=50)
    receiverMail = models.CharField(max_length=50)
    productID= models.IntegerField()
    date = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    message =  models.CharField(max_length=1000)
    messageStatus=models.CharField(max_length=30)


class recommendationTraining(models.Model):
    number=models.IntegerField()
    frequency=models.FloatField()
    productId=models.IntegerField()

