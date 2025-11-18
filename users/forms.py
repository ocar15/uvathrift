from django import forms
from django.core.exceptions import ValidationError

class StudentEmailForm(forms.Form):
    student_email = forms.EmailField(label='Student Email', max_length=254)
    
    def clean_student_email(self):
        email = self.cleaned_data.get('student_email')
        if not email.endswith("@virginia.edu"):
            raise ValidationError("Email must be a valid @virginia.edu address.")
        return email