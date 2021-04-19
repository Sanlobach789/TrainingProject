from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm, UsernameField
from django.contrib.auth.forms import UserCreationForm
from .models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):

    class Meta:

        model = ShopUser
        # username = forms.EmailField(max_length=64)
        fields = ('username', 'first_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Адрес почты'
        self.fields['first_name'].label = 'Ваше имя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтвердите пароль'

        for field_name, field in self.fields.items():

            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return data


class ShopUserChangePasswordForm(PasswordChangeForm):
    class Meta:
        fields = ('old_password', 'new_password1', 'new_password2')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.help_text = ''


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('email', 'first_name', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return data
