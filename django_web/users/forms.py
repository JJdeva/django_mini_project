from django import forms
from .models import User, Review
from allauth.account.forms import LoginForm
from place.models import Store
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'title',
            'restaurant_name',
            'rating',
            'image1',
            'image2',
            'image3',
            'content',
            'store',
        ]
        widgets = {
            'rating': forms.RadioSelect,
        }

class ReviewStore(forms.ModelForm):
    class Meta:
        model = Store
        fields = [
            'store_name',
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'nickname',
            'profile_pic',
            'intro',
        ]
        widgets = {
            'intro': forms.Textarea,
        }

class MyCustomLoginForm(LoginForm):
    class Meta:
        model = User
        fields = ['']
    def login(self, *args, **kwargs):

        # Add your own processing here.

        # You must return the original result.
        return super(MyCustomLoginForm, self).login(*args, **kwargs)

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname']

    def signup(self, request, user):
        user.nickname = self.cleaned_data['nickname']
        user.save