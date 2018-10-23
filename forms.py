from django import forms


class LoginForm(forms.Form):
    uname = forms.CharField(label='User name', max_length=100)
    psw = forms.CharField(label='Password', max_length=100)
