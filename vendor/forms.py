from django import forms
from .models import Vendor
from accounts.validators import allow_only_images_validator


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor

        fields = ["vendor_name", "vendor_license"]

    # Adding css style
    # note that validators only work with FiledField or u can try with other fields if it's working then it's fine.
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={"class": "btn btn-info"}), validators=[allow_only_images_validator])