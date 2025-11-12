from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import File, FileShare

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file', 'description']

class FileShareForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = FileShare
        fields = ['users', 'permission', 'can_download']

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.exclude(id=current_user.id)