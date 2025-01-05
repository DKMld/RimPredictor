from django.db import models


class UserSearchHistory(models.Model):
    user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/wheel_pictures')
    model_prediction = models.CharField(max_length=64, null=True)
