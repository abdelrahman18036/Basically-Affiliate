from collections.abc import Iterable
from django.db import models
from .utils import generate_uuid
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    code = models.CharField(max_length=50, blank=True)
    reffeled_by = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='reffeled')
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

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_uuid()
            while Profile.objects.filter(code=code).exists():
                code = generate_uuid()
            self.code = code
        super().save(*args, **kwargs)

