let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
}


$(document).ready(function () {
    // add_to_cart
    $('.add_to_cart').on('click', function (e) {
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response)
                if (response.status == 'login_required') {
                    swal(response.message, '', 'warning').then(function () {
                        window.location = '/login'
                    })
                } else if (response.status == "Failed") { 
                    swal(response.message, '', 'error')
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)
                }
            }
        })
    })

    // decrease_from_cart
    $('.decrease_from_cart').on('click', function (e) {
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response)
                if (response.status == 'login_required') {
                    swal(response.message, '', 'warning').then(function () {
                        window.location = '/login'
                    })
                } else if (response.status == 'Failed') { 
                    swal(response.message, '', 'error')
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-' + food_id).html(response.qty)
                }
            }
        })
    })

    // delete cart item
    $('.delete_cart_item').on('click', function (e) {
        e.preventDefault();

        item_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response)
                if (response.status == 'Failed') {
                    swal(response.message, '', 'warning').then(function () {
                        window.location = '/login'
                    })
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    swal(response.message, '', 'success')

                    removeCartItem(0, item_id);
                    checkemptycart();
                }
            }
        })
    })

    // delete cart item element if the qty is zero.
    function removeCartItem(cartitemqty, item_id) {
        if (cartitemqty <= 0) {
            // delete cart element
            document.getElementById('cart-item-'+item_id).remove()
        }
    }


    // place the cart item quantity on load
    $('.item_qty').each(function () {
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })


    // check if cart is empty
    function checkemptycart() {
        var cart_counter = document.getElementById("cart_counter").innerHTML

        if (cart_counter == 0) {
            document.getElementById("empty-cart").style.display = "block";
        }
    }
});