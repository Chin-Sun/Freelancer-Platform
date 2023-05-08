from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Avg

User = get_user_model()

class Freelancer(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE) # delete the profile if the user deletes his/her account
    name = models.CharField(max_length=50) 
    profile_pic = models.ImageField(upload_to="profiles/", blank=True)
    joinedDate = models.DateTimeField(default=timezone.now)
    skills = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    def average_rating(self) -> float:
        return Rating.objects.filter(profile=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self) -> str:
        return f'{self.id} | {self.name} | {self.average_rating()}'
    

class Business(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE) # delete the profile if the user deletes his/her account
    name = models.CharField(max_length=50) 
    profile_pic = models.ImageField(upload_to='profiles/', blank=True)
    about = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.id} | {self.name}'

    
class Project(models.Model):
    CATEGORY = (
        ('full stack developer', 'full stack developer'),
        ('front-end developer', 'front-end developer'),
        ('back-end developer', 'back-end developer'),
        ('UI/UX designer', 'UI/UX designer'),
        ('database developer', 'database developer'),
        ('machine learning developer', 'machine learning developer')
    )

    PL = (
        ('python', 'python'),
        ('java', 'java'),
        ('matlab', 'matlab'),
        ('C++', 'C++'),
        ('django', 'django'),
        ('node js', 'node js'),
        ('HTML/CSS/JS', 'HTML/CSS/JS'),
        ('react', 'react'),
        ('angularJS', 'angularJS')
    )
    
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Business, on_delete=models.CASCADE)
    developer = models.ForeignKey(Freelancer, blank=True, null=True, on_delete=models.SET_NULL)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    programming_languages = models.CharField(max_length=200, null=True, choices=PL)
    is_complete = models.BooleanField(default=False)
    dateCreated = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    budjet = models.FloatField()

    def __str__(self) -> str:
        return f'{self.id} | {self.owner.name}'
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.profile.name}: {self.rating}"
