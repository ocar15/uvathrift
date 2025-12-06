from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["title", "description", "price", "image", "condition"]

        labels = {
            "title": "",
            "description": "",
            "price": "",
            "image": "",
            "condition": "Condition"
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Title",
                "class": "form-input",
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Description",
                "class": "form-textarea",
                "rows": 4,
            }),
            "price": forms.NumberInput(attrs={
                "placeholder": "Price",
                "class": "form-input",
                "step": "0.01",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "file-upload",
            }),
            "condition": forms.Select(attrs={
                "class": "form-select",
            }),
        }
