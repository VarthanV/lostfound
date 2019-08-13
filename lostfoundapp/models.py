from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=150)
    location =models.CharField(max_length =200)
    device_id=models.CharField(max_length=200,blank=True)
    User.profile=property(lambda u: Profile.objects.get_or_create(user=u)[0])
    def __str__(self):
        return self.user.username

class Loser(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    description=models.TextField()
    date_lost = models.DateTimeField(auto_now_add =True,null=True)
    def __str__(self):
        return f'{self.user.username}'

class Founder(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    description=models.TextField()
    date_found = models.CharField(max_length=100)
    def __str__(self):
        return self.user.username


class FounderImage(models.Model):
    founder=models.ForeignKey(Founder,on_delete=models.CASCADE,blank=True,null=True)
    img=models.ImageField()
    location=models.CharField(max_length=200)
    def __str__(self):
        return self.founder.user.username

class LoserImage(models.Model):
    loser=models.ForeignKey(Loser,on_delete=models.CASCADE,blank=True,null=True)
    img=models.ImageField()
    location=models.CharField(max_length=200)  
    def __str__(self):
        return self.loser.user.username  

class MatchedRecord(models.Model):
    loser = models.ForeignKey(LoserImage,on_delete=models.CASCADE)
    founder = models.ForeignKey(FounderImage,on_delete=models.CASCADE)
    match_confirm = models.BooleanField(default=False)
    

    


    

