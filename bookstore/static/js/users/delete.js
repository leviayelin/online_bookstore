document.addEventListener('DOMContentLoaded', function(e){
    e.preventDefault()

    const deleteBtnEl = document.querySelectorAll('.delete')

    deleteBtnEl.forEach(deleteBtn => {
        deleteBtn.addEventListener('click', function(e){
            e.preventDefault()
            
            const itemId = this.value

            fetch("/users/delete/", {
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                    'X-CSRFToken':csrfToken
                },
                body:JSON.stringify({
                    'item_id':itemId
                })
            })
            .then(response => response.json())  
            .then(data => {
                if(data.success){
                    this.closest('tr').remove()
                    document.querySelector('#showcase div #total').textContent = `total: ${data.total} $`;

                    const tbRows = document.querySelectorAll('#showcase table tr').length;
                    
                    if(tbRows === 1){
                        document.querySelector('#showcase').innerHTML = `<p>empty cart</p>`;
                    }

                    console.log(tbRows)
                    window.updateCartQuantity();
                }
            })
        })
    })

    const deleteAllBtnEl = document.getElementById('delete-all')

    if(!deleteAllBtnEl){
        return;
    }

    deleteAllBtnEl.addEventListener('click', function(e){
        // e.preventDefault()
        
        console.log('delete all button clicked');

        fetch('/users/delete_all/', {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrfToken
            }
        })
        .then(resp => resp.json())
        .then(data => {
            if(data.success){

                document.querySelector('#showcase').innerHTML = `<p>empty cart</p>`;
                window.updateCartQuantity();
            }
        })
        
    })

})