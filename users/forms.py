from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from PIL import Image
from django.core.files import File
from django.core.files.storage import default_storage as storage

# add email address to UserCreationForm (does not have email by default)
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# allow users to update their username and email in the User Model
class UserUpdateForm(forms.ModelForm):
    # User Model does not have email by default
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']


# allow users to update profile picture in the Profile Model
class ProfileUpdateForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ['image', 'x', 'y', 'width', 'height']

    # overwrite the save method to resize the image based on what we have cropped
    def save(self, *args, **kwargs):
        profile = super(ProfileUpdateForm, self).save(*args, **kwargs)

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(profile.image)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)

        # AWS S3 does not support absolute path with .save()
        # resized_image.save(profile.image.name)
        
        # Have to use this method with AWS S3
        fh = storage.open(profile.image.name, "w")
        picture_format = 'png'
        resized_image.save(fh, picture_format)
        fh.close()        

        return profile