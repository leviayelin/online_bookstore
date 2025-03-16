document.addEventListener('DOMContentLoaded', function(e){
    e.preventDefault()
    
    let addToCartBtnEl = document.querySelectorAll('.add-book-btn')
    addToCartBtnEl.forEach( bottun => {

        bottun.addEventListener('click', function(){

            let itemValue = this.value
            console.log('button clicked');
            
            
            fetch("/store/add_to_cart/", {
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                    'X-CSRFToken':csrfToken
                },
                body:JSON.stringify({
                    bookId:itemValue,
                })
            })

            .then(response => response.json())
            .then(data => {
                if(data.redirect){
                    window.location.href = data.redirect;
                    return; 
                }
                if(data.success){
                    console.log('success')
                    window.updateCartQuantity();
                }
            }).catch(error =>{
                console.error('error', error)
            })
        })
    })
})