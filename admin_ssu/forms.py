# forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User, Group, Permission
from collections import OrderedDict
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class EmailAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True, 'placeholder': 'Email'}))
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'placeholder': 'Contraseña'}),
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']
        self.fields = OrderedDict(
            (k, self.fields[k]) for k in ['email', 'password']
        )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email/password combination.")

            if not user.check_password(password):
                raise forms.ValidationError("Invalid email/password combination.")

            self.user_cache = user

        return self.cleaned_data
    
    
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Requerido.', label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, help_text='Requerido.',label="Apellidos")
    is_superuser = forms.BooleanField(required=False,label="Hacer Admin")
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False, label="Grupos")
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email', 'password1', 'password2','groups','is_superuser' )
        

class CustomUserEditForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserEditForm, self).__init__(*args, **kwargs)
        del self.fields['password']
        self.fields['is_superuser'].label = "Es admin"
        self.fields['email'].label = "Email"
        
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'groups', 'is_superuser','is_active')
        
        
class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Permisos"
    )
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        content_types = ContentType.objects.all().order_by('model')
        choices = []
        for content_type in content_types:
            permissions_of_model = Permission.objects.filter(content_type=content_type)
            if permissions_of_model:
                choices.append([f'{content_type.app_label} | {content_type.model}', permissions_of_model])
        self.fields['permissions'].choices = choices