from django.db import models
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from Profiles.models import Profile



# Create your models here.
class UserPayment(models.Model):
    app_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_session_id = models.CharField(max_length=50, blank=True)
    updated = models.DateTimeField(auto_now=True)



@receiver(post_save, sender=Profile)
def create_user_payment(sender, instance, created, **kwargs):
    if created:
        UserPayment.objects.create(app_user=instance)

