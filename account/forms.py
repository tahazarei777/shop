from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label='نام')
    last_name = forms.CharField(required=True, label='نام خانوادگی')
    password = forms.CharField(required=False, widget=forms.PasswordInput, label='رمز عبور جدید')

    class Meta:
        model = Profile
        fields = ['phone_number']

    def save(self, user=None, commit=True):
        profile = super().save(commit=False)
        if user:
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            password = self.cleaned_data.get('password')
            if password:
                user.set_password(password)
            if commit:
                user.save()
                profile.user = user
                profile.save()
        return profile
