from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["title", "description", "price", "condition", "listed", "image"]

        labels = {
            "title": "",
            "description": "",
            "price": "",
            "image": "",
            "condition": "Condition",
            "listed": "Public"
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Title",
                "class": "form-input",
                "maxlength": "100",
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Description",
                "class": "form-textarea",
                "rows": 4,
                "maxlength": "500",
            }),
            "price": forms.NumberInput(attrs={
                "placeholder": "Price",
                "class": "form-input",
                "step": "0.01",
                "min": "0",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "file-upload",
            }),
            "condition": forms.Select(attrs={
                "class": "form-select",
            }),
            "listed": forms.CheckboxInput()
        }
