from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CandidateRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


from .models import Application

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cv']
        widgets = {
            'cv': forms.ClearableFileInput(
                attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}
            )
        }

    def clean_cv(self):
        cv = self.cleaned_data['cv']

        allowed_extensions = ('.pdf', '.doc', '.docx')

        if not cv.name.lower().endswith(allowed_extensions):
            raise forms.ValidationError(
                'Please upload a PDF, DOC or DOCX file.'
            )

        if cv.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                'CV must be smaller than 5 MB.'
            )

        return cv