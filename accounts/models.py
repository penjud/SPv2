from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cryptography.fernet import Fernet
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    betfair_username = models.CharField(max_length=100)
    betfair_password = models.BinaryField()
    betfair_api_key = models.BinaryField()

    def save(self, *args, **kwargs):
        f = Fernet(settings.ENCRYPTION_KEY)
        self.betfair_password = f.encrypt(self.betfair_password.encode())
        self.betfair_api_key = f.encrypt(self.betfair_api_key.encode())
        super().save(*args, **kwargs)

    def decrypt_password(self):
        f = Fernet(settings.ENCRYPTION_KEY)
        return f.decrypt(self.betfair_password).decode()

    def decrypt_api_key(self):
        f = Fernet(settings.ENCRYPTION_KEY)
        return f.decrypt(self.betfair_api_key).decode()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()