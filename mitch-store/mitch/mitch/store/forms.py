from django import forms
from django.contrib.auth.forms import UserCreationForm, UserModel
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(label = "Email", required=True)
    first_name = forms.CharField(label = "First name", required = True )
    last_name = forms.CharField(label = "Last name", required = True)
   
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2" )

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None