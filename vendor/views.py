from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify

from .forms import VendorForm
from accounts.forms import UserProfileForm

from .models import Vendor
from accounts.models import UserProfile

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from accounts.views import check_role_vendor
from menu.models import Category, Fooditem

from menu.forms import CategoryForm, FoodItemForm



def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required(login_url="log-in")
@user_passes_test(check_role_vendor)
def v_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Settings updated successfully!")
            return redirect("v-profile")
        else:
            messages.error(request, "Invalid data form!")
    else:
        vendor_form = VendorForm(instance=vendor)
        profile_form = UserProfileForm(instance=profile)
    return render(request, "vendor/vprofile.html",{
        "vendor_form": vendor_form,
        "profile_form": profile_form,
        "profile": profile,
        "vendor": vendor,
    })


@login_required(login_url="log-in")
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    return render(request, "vendor/menu-builder.html",{
        "categories": categories,
    })


@login_required(login_url="log-in")
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = Fooditem.objects.filter(vendor=vendor, category=category).order_by("created_at")
    print(fooditems)
    return render(request, "vendor/fooditems-by-category.html",{
        "fooditems": fooditems,
        "category": category,
    })


@login_required(login_url="log-in")
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category_name = form.cleaned_data["category_name"]
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect("menu-builder")
    else:
        form = CategoryForm()
    return render(request, "vendor/add-category.html", {
        "form": form,
    })


@login_required(login_url="log-in")
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category_name = form.cleaned_data["category_name"]
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect("menu-builder")
    else:
        form = CategoryForm(instance=category)

    return render(request, "vendor/edit-category.html", {
        "form": form,
        "category": category,
    })


@login_required(login_url="log-in")
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect("menu-builder")


@login_required(login_url="log-in")
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food_title = form.cleaned_data["food_title"]
            food.slug = slugify(food_title)
            form.save()
            messages.success(request, "FoodItem Added Successfully!")
            return redirect("fooditems-by-category", food.category.id)
    else:
        form = FoodItemForm()
        # Important point. lecture 91.
        form.fields["category"].queryset = Category.objects.filter(vendor=get_vendor(request))
    return render(request, "vendor/add-food.html", {
        "form": form,
    })
    

@login_required(login_url="log-in")
@user_passes_test(check_role_vendor)
def edit_food(request, pk=None):
    food = get_object_or_404(Fooditem, pk=pk)
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food_title = form.cleaned_data["food_title"]
            food.slug = slugify(food_title)
            form.save()
            messages.success(request, "Food updated Successfuly!")
            return redirect("fooditems-by-category", food.category.id)
    else:    
        form = FoodItemForm(instance=food)
        form.fields["category"].queryset = Category.objects.filter(vendor=get_vendor(request))
    return render(request, "vendor/edit-food.html", {
        "form": form,
        "food": food,
    })


@login_required(login_url="log-in")
@user_passes_test(check_role_vendor)
def delete_food(request, pk=None):
    food = get_object_or_404(Fooditem, pk=pk)
    food.delete()
    messages.success(request, "FoodItem deleted successfully!")
    return redirect("fooditems-by-category", food.category.id)