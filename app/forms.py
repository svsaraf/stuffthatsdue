from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):

    COLLEGES = (
        ('Pa', 'Patel'),
        ('St', 'Strople'),
        ('Le', 'Leung'),
        ('Sc', 'Schaefer'),
    )

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    college = forms.ChoiceField(choices = COLLEGES)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_match = forms.CharField(widget=forms.PasswordInput, label="Confirm")

    def clean_email(self):
        """
        Custom form validation that verifies the email
        address is unique
        """
        try:
            User.objects.get(email=self.cleaned_data['email'])
            raise forms.ValidationError("That email address has already been registered!")
        except User.DoesNotExist:
            pass

        try:
            x = self.cleaned_data['email']
            print x[-20:]
            if x[-20:] != 'fsm.northwestern.edu':
                raise forms.ValidationError("Use your fsm email, jerk!")
        except User.DoesNotExist:
            pass
        return self.cleaned_data['email']

    def clean_password_match(self):
        """
        Custom form validation that verifies the entered passwords
        match
        """
        match = self.cleaned_data['password_match']
        password = self.cleaned_data['password']

        if password != '' and match != password:
            raise forms.ValidationError("Passwords did not match!")
        return match


class ActivityForm(forms.Form):

    TYPE_OF_ACTIVITY = (
        ('R', 'Reading'),
        ('A', 'Assignment'),
    )

    DAY_IT_IS_DUE = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )

    title = forms.CharField()
    text = forms.CharField(widget=forms.TextInput(attrs={'class':'largeformfield'}))
    typeofact = forms.ChoiceField(choices = TYPE_OF_ACTIVITY)
    patelduedate = forms.ChoiceField(choices = DAY_IT_IS_DUE)
    stropleduedate = forms.ChoiceField(choices = DAY_IT_IS_DUE)
    leungduedate = forms.ChoiceField(choices = DAY_IT_IS_DUE)
    schaeferduedate = forms.ChoiceField(choices = DAY_IT_IS_DUE)



