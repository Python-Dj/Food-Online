from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from vendor.models import Vendor

from marketplace.models import Fooditem
from .models import Cart
from menu.models import Category

from .context_processors import get_cart_counter
from django.contrib.auth.decorators import login_required




def market_place(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    return render(request, "marketplace/vendors-list.html", {
        "vendors": vendors,
        "vendor_count": vendor_count,
    })


def vendor_details(request, slug):
    vendor = Vendor.objects.get(slug=slug)

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    
    return render(request, "marketplace/vendor-details.html", {
        "vendor": vendor,
        "cart_item": cart_items,
    })


def add_to_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            #check if the food item exist.
            try:
                fooditem = Fooditem.objects.get(id=food_id)
                #check if user has already addedthat food to the cart.
                try:
                    chkcart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    #Increase the Cart quantity.
                    chkcart.quantity += 1
                    chkcart.save()
                    return JsonResponse({"status": "Success", "message": "Increase the cart quantity!", "cart_counter": get_cart_counter(request), "qty":chkcart.quantity})
                except:
                    chkcart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({"status": "Success", "message": "added food to the Cart!", "cart_counter": get_cart_counter(request), "qty":chkcart.quantity})

            except:
                return JsonResponse({"status": "Failed", "message": "This food does not exist!"})
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid request!"})
    else:
        return JsonResponse({"status": "login_required", "message": "Please log in to Continue"})
    

def decrease_from_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            try:
                fooditem = Fooditem.objects.get(id=food_id)
                try:
                    chkcart = Cart.objects.get(fooditem=fooditem, user=request.user)
                    if chkcart.quantity > 0:
                        chkcart.quantity -= 1
                        chkcart.save()
                        return JsonResponse({"status": "Success", "message": "decreases the Cart quantity!", "cart_counter": get_cart_counter(request), "qty":chkcart.quantity})
                    else:
                        return JsonResponse({"status": "Failed", "message": "you can not decreases the quantity now!"})
                except:
                    return JsonResponse({"status": "Failed", "message": "you can't decrease the quantity now!"})
            except:
                return JsonResponse({"status": "Failed", "message": "This food does not exist!"})
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid request!"})
    else:
        return JsonResponse({"status": "login_required", "message": "please log in to continue!"})
    

@login_required(login_url="log-in")
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by("created_at")

    return render(request, "marketplace/cart.html", {
        "cart_items": cart_items,
    })


def delete_cart_item(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({"status": "Success", "message": "Cart item has been deleted!", "cart_counter": get_cart_counter(request)})
            except:
                    return JsonResponse({"status": "Failed", "message": "This cart item does not exist!"})
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid request!"})