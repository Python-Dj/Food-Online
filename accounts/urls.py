from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.myaccount),
    path("registerUser/", views.registerUser, name="register-user"),
    path("registerVendor/", views.registerVendor, name="register-vendor"),

    path("login/", views.login, name="log-in"),
    path("logout/", views.logout, name="log-out"),

    path("myaccount/", views.myaccount, name="my-account"),
    path("cusdashboard/", views.customer_dashboard, name="cus-dash-board"),
    path("vendashboard/", views.vendor_dashboard, name="ven-dash-board"),

    path("activate/<uidb64>/<token>/", views.activate, name="activate"),

    path("forgot-password/", views.forgot_password, name="forgot-password"),
    path("reset-password-validate/<uidb64>/<token>/", views.reset_password_validate, name="reset-password-validate"),
    path("reset-password/", views.reset_password, name="reset-password"),

    path("vendor/", include("vendor.urls")),
]