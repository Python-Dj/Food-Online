from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]


    def clean(self):
        cleaned_data = super(UserForm, self).clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )
        

class UserProfileForm(forms.ModelForm):
    # note that validators only work with FiledField or u can try with other fields if it's working then it's fine.
    address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "start typing....", "required": "required"}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={"class": "btn btn-info"}), validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={"class": "btn btn-info"}), validators=[allow_only_images_validator])

    class Meta:
        model = UserProfile
        exclude = ["user", "created_at", "modified_at"]


    # latitude = forms.CharField(widget=forms.TextInput(attrs={"readonly": "readonly"}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={"readonly": "readonly"}))


    # this method is more handy if u want to work on multiple fields.
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for filed in self.fields:
            if filed == "longitude" or filed == "latitude":
                self.fields[filed].widget.attrs["readonly"] = "readonly"