from django import forms
from django.contrib.auth.models import User
from .models import GroupChat

class CreateGroupForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = GroupChat
        fields = ['name', 'members']
    
    def clean_members(self):
        members = self.cleaned_data.get('members')

        if len(members) < 2:
            raise forms.ValidationError("You must select atleast 2 members for a groupchat.")

        return members 
