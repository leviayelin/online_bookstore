document.addEventListener('DOMContentLoaded', function(e){

    e.preventDefault()

    const checkoutBtnEl = document.getElementById('checkout')
    if(checkoutBtnEl){
        checkoutBtnEl.addEventListener('click', function(){
            fetch('/users/checkout/',{
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                    'X-CSRFToken':csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if(data.success){
                    
                    // Clear the cart section
                    document.querySelector('#showcase').innerHTML = `<p>Your cart is empty</p>`;

                    // Update cart quantity in navbar
                    window.updateCartQuantity()

                    // Update order history dynamically
                    const orderHistoryEl = document.getElementById('order-history');
                    const newOrderHtml = `
                        <div class="order-box" id="order-${data.order_data.order_id}">
                            <p><strong>Order ID:</strong> ${data.order_data.order_id}</p>
                            <p><strong>Date:</strong> ${data.order_data.created_at}</p>
                            <p><strong>Total Price:</strong> ${data.order_data.total_price} $</p>
                            <ul>
                                ${data.order_data.items.map(item => 
                                    `<li>${item.title} (x${item.quantity}) — ${item.subtotal} $</li>`).join('')
                                }
                            </ul>
                        </div>`;
                    
                    // If there are no orders, replace the message
                    if (orderHistoryEl.innerHTML.includes('No orders found.')) {
                        orderHistoryEl.innerHTML = newOrderHtml;
                    } else {
                        orderHistoryEl.insertAdjacentHTML('afterbegin', newOrderHtml);
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        })
    }


    const clearHistoryBtnEl = document.getElementById('clear-history')

    if(clearHistoryBtnEl){
        clearHistoryBtnEl.addEventListener('click', function(){
            fetch('/users/clear_history/',{
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                    'X-CSRFToken':csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if(data.success){
                    document.getElementById('order-history').innerHTML = `<p>No orders found.</p>`;
                }else{
                    alert('Failed to clear history.');
                }
            })
        })
    }
})