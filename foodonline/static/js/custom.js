

// add to cart plus button 
$(document).ready(function(){
    // add to cart
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)
                if(response.status == 'login_required'){
                    
                    swal(response.message," ", "warning").then(function(){
                        window.location = '/login';
                    })
                }else if (response.status =='Failed'){
                    swal(response.message,'','error')
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);

                    // subtotal tags and grandtotal
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],
                    )

                }

            }
        })
    })

    // place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })

    // decrease_cart
    $('.decrease_cart').on('click',function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)

                if(response.status == 'login_required'){
                    swal(response.message,'','warning').then(function(){
                        window.location = '/login';
                    })
                }
                else if(response.status == 'Failed'){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty);

                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],
                    )

                    if(window.location.pathname == '/marketplace/cart/'){
                        removeCartItem(response.qty,cart_id);
                        checkEmptyCart();
                    }
                        
                }

            
            }
        })
    })

    // delete cart item
    $('.delete_cart').on('click',function(e){
        e.preventDefault();
        
        

        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)

                if(response.status == 'Failed'){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status,response.message,'success');


                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],
                    )

                    removeCartItem(0,cart_id);
                    checkEmptyCart();
                }

            
            }
        })
    })


    // delete the cart element if the qty is zero 0
    function removeCartItem(cartItemQty,cart_id){
        if(cartItemQty <=0){
            // then for the above condition remove the item element 
            document.getElementById("cart-item-"+cart_id).remove()

        }
    }

    // check if the cart if empty
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if(cart_counter==0){
            document.getElementById("empty-cart").style.display = "block";
        }
    }

    //to apply cart amounts
    function applyCartAmounts(subtotal,tax,grand_total){
        if(window.location.pathname == '/marketplace/cart/'){
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(grand_total)
        }

    }
});