"""# blog/forms.py"""

from django import forms

class NameForm(forms.Form):
    """NameForm"""
    first_name = forms.CharField(label='First Name', max_length=50)
    last_name = forms.CharField(label='Last Name', max_length=50)

class ExampleSignupForm(forms.Form):
    """Example Signup Form"""
    first_name = forms.CharField(label='First name', max_length=50)
    last_name = forms.CharField(label='Last name', max_length=50)
    email = forms.EmailField()
    gender = forms.ChoiceField(
        label='Gender',
        required=False,
        choices=[
            (None, '-------'),
            ('m', 'Male'),
            ('f', 'Female'),
        ]
    )
    receive_newsletter = forms.BooleanField(
        required=False,
        label='Do you wish to receive our newsletter?'
    )
