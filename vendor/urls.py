from django.urls import path
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path("", AccountViews.vendor_dashboard, name="vendor"),
    path("profile/", views.v_profile, name="v-profile"),
    path("menu-builder/", views.menu_builder, name="menu-builder"),
    path("menu-builder/category/<int:pk>/", views.fooditems_by_category, name="fooditems-by-category"),

    # category CRUD
    path("menu-builder/category/add/", views.add_category, name="add-category"),
    path("menu-builder/category/edit/<int:pk>/", views.edit_category, name="edit-category"),
    path("menu-builder/category/delete/<int:pk>/", views.delete_category, name="delete-category"),

    # FoodItem CRUD
    path("menu-bulider/food/add/", views.add_food, name="add-food"),
    path("menu-builder/food/edit/<int:pk>/", views.edit_food, name="edit-food"),
    path("menu-builder/food/delete/<int:pk>/", views.delete_food, name="delete-food"),
]
