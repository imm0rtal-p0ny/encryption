from django import forms


class EncryptionForms(forms.Form):
    file = forms.FileField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean_password2(self):
        passwd1 = self.cleaned_data['password1']
        passwd2 = self.cleaned_data['password2']
        if passwd1 != passwd2:
            raise forms.ValidationError('Passwords do not match')


class DecryptionForms(forms.Form):
    file = forms.FileField()
    password = forms.CharField(widget=forms.PasswordInput())
