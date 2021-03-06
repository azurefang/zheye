from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': 'email exits',
        'password_mismatch': "The two password fields didn't match.",
    }

    first_name = forms.CharField(label='firstname')
    last_name = forms.CharField(label='lastname')
    username = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label=u'注册邮箱', max_length=100)
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput())


class QuestionForm(forms.Form):
    title = forms.CharField(label='title', max_length=40)
    content = forms.CharField(label='content', widget=forms.Textarea)

