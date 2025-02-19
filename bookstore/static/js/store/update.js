document.addEventListener('DOMContentLoaded', function(){

    let orderQuantityEl = document.querySelectorAll('.order-quantity')

    orderQuantityEl.forEach(item =>{
        item.addEventListener('change', function(){
            let orderIdEl = this.getAttribute('id')
            let newQuantityEl = this.value

            // console autput
            console.log(`order number: ${orderIdEl}, quantity: ${newQuantityEl}`);

            // in case minimum propery asign to html input 
            if(newQuantityEl < 1){
                alert("Quantity must be at least 1")
                this.value = 1
                return;
            }
            
            // using AJAX to upadte the quantity data
            fetch(updateURLEl, {
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "X-CSRFToken":csrfToken
                },
                body: JSON.stringify({
                    item_id:orderIdEl,
                    quantity:newQuantityEl
                })
            })
            .then(response => response.json())
            .then( data => {
                if(data.success){
                    location.reload();
                }else{
                    alert("Faild to update quantity")
                }
            })
        })
    })
})