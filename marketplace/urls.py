from django.urls import path
from . import views


urlpatterns = [
    path("", views.market_place, name="market-place"),
    path("<slug:slug>", views.vendor_details, name="vendor-details"),

    #add to Cart
    path("addToCart/<int:food_id>/", views.add_to_cart, name="add-to-cart"),
    # Decrease
    path("decreaseFromCart/<int:food_id>/", views.decrease_from_cart, name="decrease-from-cart"),

    path("cart/", views.cart, name="cart"),
    # Delete the cart
    path("deleteCartItem/<int:cart_id>", views.delete_cart_item, name="delete-cart-item"),
]
