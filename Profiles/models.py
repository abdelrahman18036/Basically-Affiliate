from collections.abc import Iterable
import queue
from django.db import models
from .utils import generate_uuid
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, max_length=50)
    code = models.CharField(max_length=50, blank=True)
    reffeled_by = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='reffeled')
    payment_sucessful_ref= models.OneToOneField('user_payment.UserPayment', on_delete=models.CASCADE, blank=True, null=True, related_name='payment_ref')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.code}"
    
    def get_recommened_profiles(self):
        qs = Profile.objects.all()
        my_ref = []
        for profile in qs:
            if profile.reffeled_by == self:
                my_ref.append(profile)
        return my_ref
    

    def get_referred_users_with_payment(self):
        referred_users_with_payment = []
        for profile in Profile.objects.filter(reffeled_by=self):
            if profile.payment_sucessful_ref is not None:
                referred_users_with_payment.append(profile)
        return referred_users_with_payment
    
    def get_code(self):
        code = self.code
        return code
  
    def get_growth(self):
        try:
            qs = Profile.objects.all()
            my_ref = []
            for profile in qs:
                if profile.reffeled_by == self:
                    my_ref.append(profile)

            referred_users_with_payment = []
            for profile in Profile.objects.filter(reffeled_by=self):
                if profile.payment_sucessful_ref is not None:
                    referred_users_with_payment.append(profile)

            if len(my_ref) == 0:
                return 0

            growth = (len(referred_users_with_payment) / len(my_ref)) * 100
            return growth
        except ZeroDivisionError:
            return 0
    
    

    
  
    # def get_reffeled_by(self):
    #     my_profile = self
    #     qs = Profile.objects.all()
    #     for profile in qs:
    #         if profile.reffeled_by == my_profile:
    #             return profile
    #         else:
    #             return None

    # def get_payment_ref(self):
    #     my_profile = self
    #     qs = Profile.objects.all()
    #     for profile in qs:
    #         if profile.payment_sucessful_ref == my_profile:
    #             return profile
    #         else:
    #             return None        


    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_uuid()
            while Profile.objects.filter(code=code).exists():
                code = generate_uuid()
            self.code = code
        super().save(*args, **kwargs)

