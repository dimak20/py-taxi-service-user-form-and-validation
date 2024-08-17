import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(number) -> None:
    if len(number) != 8:
        raise ValidationError("License number must equal 8 symbols")
    if not re.match(r"^[A-Z]{3}", number):
        raise ValidationError(
            "License number must start with 3 uppercase letters"
        )
    if not re.match(r"^[A-Z]{3}[0-9]{5}$", number):
        raise ValidationError(
            "License number must include 5 digits after 3 uppercase letters"
        )


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        max_length=8,
        validators=[
            validate_license_number
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        max_length=8,
        validators=[
            validate_license_number
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
