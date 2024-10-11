from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User, UserProfile
from vendor.models import Vendor

from vendor.forms import VendorForm

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from .utils import detectuser, send_varification_email

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.text import slugify


# Restrict the vendor from accessing customer page.
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
# Restrict the customer from accessing vendor page.
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "User is already logged in!")
        return redirect("cus-dash-board")

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # create user using form.
            user = form.save(commit=False)
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()

            # Send Varification Email.
            mail_subject = "Please activate your account"
            email_template = "accounts/emails/account_varification_email.html"
            send_varification_email(request, user, mail_subject, email_template)
            
            messages.success(request, "Your account has been registered successfully!")
            return redirect("register-user")
    else:      
        form = UserForm()
    return render(request, "accounts/register-user.html", {
        "form": form,
    })


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect("ven-dash-board")
    
    if request.method == "POST":
        u_form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if u_form.is_valid() and v_form.is_valid:
            user = u_form.save(commit=False)
            password = u_form.cleaned_data["password"]
            user.set_password(password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data["vendor_name"]
            vendor.slug = slugify(vendor_name)+"-"+str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # Send Varification Email.
            mail_subject = "Please activate your account"
            email_template = "accounts/emails/account_varification_email.html"
            send_varification_email(request, user, mail_subject, email_template)

            messages.success(request, "Your account has been registered successfully!")
            return redirect("register-vendor")

    else:
        u_form = UserForm()
        v_form = VendorForm()
    return render(request, "accounts/register-vendor.html", {
        "u_form": u_form,
        "v_form": v_form,
    })


def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True.
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (KeyError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulation your account is activated!")
        return redirect("my-account")
    else:
        messages.error(request, "Invalid activation link!")
        return redirect("my-account")
    

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect("my-account")
    
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
    
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect("my-account")
        else:
            messages.error(request, "Invalid login Credentials!")
            return redirect("log-in")

    return render(request, "accounts/login.html")


def logout(request):
    auth.logout(request)
    messages.info(request,"You are logged out!")
    return redirect("log-in")


@login_required(login_url="log-in")
def myaccount(request):
    user = request.user
    redirect_url = detectuser(user)
    return redirect(redirect_url)


@login_required(login_url="log-in")
@user_passes_test(check_role_customer)
def customer_dashboard(request):
    return render(request, "accounts/cus-dashboard.html")


@login_required(login_url="log-in")
@user_passes_test(check_role_vendor)
def vendor_dashboard(request):
    vendor = Vendor.objects.get(user=request.user)
    return render(request, "accounts/ven-dashboard.html", {
        "vendor": vendor,
    })


def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            #send reset password email.
            mail_subject = "Reset your password"
            email_template = "accounts/emails/reset_password_email.html"
            send_varification_email(request, user, mail_subject, email_template)
            messages.success(request, "Password reset link has been sent to your email!")
            return redirect("log-in")
        else:
            messages.error(request, "Account does not exist!")
            return redirect("forgot-password")
    return render(request, "accounts/forgot-password.html")


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(ValueError, KeyError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.info(request, "Please reset your password!")
        return redirect("reset-password")
    else:
        messages.error(request, "This link has been expired!")
        return redirect("my-account")


def reset_password(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            pk = request.session.get("uid")
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Your password has been reset successfully!")
            return redirect("log-in")
        else:
            messages.error(request, "Password do not match!")
            return redirect("reset-password")
    return render(request, "accounts/reset-password.html")
