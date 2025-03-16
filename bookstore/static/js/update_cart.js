
document.addEventListener('DOMContentLoaded', function(e){
    e.preventDefault()

    // getting the count element from the document
    const cartQuantityEl = document.getElementById('quantity')

    // if cartQuantity doesnt exist. stop the function 
    // not exist becouse of 'login logout check'
    if(!cartQuantityEl){
        console.log('User not logged in — skipping cart quantity update.');
        return;
    }

     window.updateCartQuantity = function(){
        fetch("/users/cart_quantity/", {
            method:'GET',
            headers:{
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken':csrfToken
            }
        })
        .then(response =>{

            if(response.status == 401){
                console.log('User not logged in. Skipping cart update.');
                if(cartQuantityEl){
                    cartQuantityEl.textContent = 0;
                }
                return null;
            }
            if (!response.ok) {
                throw new Error('Not logged in or error fetching cart data');
            }
            return response.json();
        })
        .then(data => {
            
            if(data && data.total_quantity !== undefined){
                cartQuantityEl.textContent = data.total_quantity ?? 0;
            }
        })
        .catch(error => {
            console.log('Error updating cart quantity:', error);
            if (cartQuantityEl) {
                cartQuantityEl.textContent = 0;  // Reset cart count on logout
            }
        })
     }
    updateCartQuantity();
});


