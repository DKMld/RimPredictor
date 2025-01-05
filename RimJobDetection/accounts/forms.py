from RimJobDetection.accounts.models import Users
from django import forms


class UserRegistrationForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = ['username', 'password', 'email']
        exclude = ['last_login']


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user
