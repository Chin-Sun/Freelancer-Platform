from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    def get_freelancer(self):
        if(hasattr(self, 'freelancer')):
            return self.freelancer
        return None
        
    def get_business(self):
        if(hasattr(self, 'business')):
            return self.business
        return None
    
    def __str__(self) -> str:
        return f'{self.id} | {self.username}'


