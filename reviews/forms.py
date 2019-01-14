from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Review

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class CreateReview(forms.ModelForm):
    rating = forms.IntegerField(max_value=5, min_value=1)
    description = forms.Textarea()
    class Meta:
        model = Review
        fields = ('rating', 'description') 