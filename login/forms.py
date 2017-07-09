from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("This User Does Not Exist")

        if not user.check_password(password):
            raise forms.ValidationError("Incorrect Password")

        if not user.is_active:
            raise forms.ValidationError("User Is No Longer Active")

        return super(UserLoginForm, self).clean(*args, **kwargs)