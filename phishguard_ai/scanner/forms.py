from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class URLScanForm(forms.Form):
    url = forms.CharField(
        label="Enter URL to scan",
        widget=forms.TextInput(
            attrs={
                "placeholder": "https://example.com/login",
                "class": "form-control form-control-lg neon-input",
                "autocomplete": "off",
            }
        ),
        max_length=500,
    )

    def clean_url(self):
        value = self.cleaned_data["url"].strip()
        if not value.startswith(("http://", "https://")):
            value = "http://" + value
        validator = URLValidator()
        try:
            validator(value)
        except ValidationError as e:
            raise ValidationError("Please enter a valid URL.")
        return value

