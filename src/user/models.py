from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    email = models.EmailField(unique=True)#sobreescrito

    #web_site = models.CharField(max_length=255, blank=True)
    #twitter = models.CharField(max_length=255, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Follow(models.Model):
    """Representa la relación entre usuario y el seguimiento entre ellos. 

    Attributes:
        follower: Es el usuario que está siguiendo.
        following: Es el usuario que está siendo seguido.
        created_at: Fecha en la que el usuario follower empezó a seguir al usuario following.
    """
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} sigue a {self.following}'