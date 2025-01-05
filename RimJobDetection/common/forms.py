from django.forms import ModelForm
from RimJobDetection.predictions.models import UserSearchHistory


class UserUploadedPictureForm(ModelForm):

    class Meta:
        model = UserSearchHistory

        fields = ['image']
