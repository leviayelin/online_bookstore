document.addEventListener('DOMContentLoaded', function(e){

    e.preventDefault()

    let orderQuantityEl =  document.querySelectorAll('.order-quantity')

    orderQuantityEl.forEach( item =>{
        item.addEventListener('change', function(){
            let itemIdEl = this.getAttribute("id")
            let newQuantityEl = this.value
            
            console.log(itemIdEl, newQuantityEl);
            
            // condition if quantity is less then 1
            if(newQuantityEl < 1){
                alert("Quantity must be at least 1")
                this.value = 1;
                return;
            }

            // using AJAX to update data 
            fetch("/users/update_cart/",{
                method:"POST",
                headers:{
                    'Content-Type':"application/json",
                    'X-CSRFToken':csrfToken
                },
                body: JSON.stringify({
                    item_id:itemIdEl,
                    quantity:newQuantityEl
                })
            })
            .then(response => response.json())
            .then(data => {
                if(data.success){
                    document.querySelector('#showcase div #total').textContent = `total: ${data.total} $`;

                    // change the subtotal dinamcly
                    const subtotalEl = this.closest('tr').querySelector('#subtotal');
                    subtotalEl.textContent = `${data.subtotal} $`;

                    window.updateCartQuantity();  // Refresh the cart count
                }else{
                    console.error("Faild to update quantity")
                }
            })
        })
    })
})