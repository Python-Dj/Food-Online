from accounts.validators import allow_only_images_validator
from django import forms

from .models import Category, Fooditem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category

        fields = ("category_name", "description")


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = Fooditem

        fields = ["category", "food_title", "description", "price", "image", "is_available"]

    image = forms.ImageField(widget=forms.FileInput(attrs={"class": "mt-3 mr-3 btn btn-info"}), validators=[allow_only_images_validator])