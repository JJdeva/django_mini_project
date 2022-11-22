from django import forms
from .models import Store, Menu
from users.models import User

class SearchForm(forms.Form):
    # 나중에 모델폼으로 바꾸자
    keyword = forms.CharField(label='keyword', max_length=100)