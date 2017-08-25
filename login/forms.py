from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout

User = get_user_model()

# Use django built in form code for user authentication

class UserLoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):
        user = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(user=user, password=password)
        if not user:
            raise forms.ValidationError("Either User Does Not Exist or Password Invalid")
        if not user.is_active:
            raise forms.ValidationError("User Is No Longer Active")
            
        # If the user authenciates, log them in. 
        return super(UserLoginForm, self).clean(*args, **kwargs)