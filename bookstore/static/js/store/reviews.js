document.addEventListener('DOMContentLoaded', function(){

    const reviewFormEl = document.querySelector('#reviews_form')

    if(!reviewFormEl){
        return;
    }
    
    reviewFormEl.addEventListener('submit',function(e){
        e.preventDefault()

        const bookId = document.getElementById('comment_id').value
        const commentTitle = document.getElementById('title').value
        const comment = document.getElementById('comment').value

        console.log(bookId);
        
        fetch("/store/reviews/add/",{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrfToken
            },
            body:JSON.stringify({
                'book_id': bookId,
                'review_title':commentTitle,
                'review_comment':comment
            })
        }).then(response =>{
             if(response.status === 401){
                return response.json().then(data =>{
                    window.location.href = data.redirect;
                })
             }
             if(!response.ok){
                throw new Error('Failed to submit review');
             }

             return response.json()
            })
        .then(data => {

            if(data.redirect){
                window.location.href = data.redirect;
                return;
            }

            if(data.success){

                const reviewList = document.getElementById('reviews-list');

                const newReview = `
                    <div class="user-review">
                        <p><b>${data.title}</b></p>
                        <hr>
                        <p>${data.comment}</p>
                        <div>
                            <span>${data.user}</span>
                            <span>${data.date}</span>
                        </div>
                    </div>
                `;

                document.getElementById('no-reviews').style.display = 'none';

                // If there are no reviews, replace the message
                if (reviewList.innerHTML.includes('no reviews yet!')) {
                    reviewList.innerHTML = newReview;
                    reviewFormEl.reset();
                } else {
                    // Add new review without reloading
                    reviewList.insertAdjacentHTML('afterbegin', newReview);
                    reviewFormEl.reset();
                }
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while submitting the review.");
        });
    })
})