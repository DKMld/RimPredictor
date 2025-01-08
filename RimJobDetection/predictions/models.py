import hashlib
from django.db import models
import os
from django.template.context_processors import static
import RimJobDetection.settings as settings


# class OverwriteStorage(FileSystemStorage):
#     def get_available_name(self, name, max_length=None):
#         print(name)
#         if self.exists(name):
#             self.delete(name)
#         return name


class UserSearchHistory(models.Model):
    user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=os.path.join('static/', settings.MEDIA_URL))
    model_prediction = models.CharField(max_length=64, null=True)
    image_hash = models.CharField(max_length=128, unique=True, null=True)

    @staticmethod
    def calculate_image_hash(image):
        hasher = hashlib.md5()

        for chunk in image.chunks():
            hasher.update(chunk)
        return hasher.hexdigest()

    # def save(self, *args, **kwargs):
    #     if self.image:
    #         self.image_hash = self.calculate_image_hash()
    #         if UserSearchHistory.objects.filter(image_hash=self.image_hash).exists():
    #             print('exists')
    #             return
    #     super().save(*args, **kwargs)

