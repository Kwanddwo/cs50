document.addEventListener('DOMContentLoaded', () => {
    const post_form = document.querySelector('#post-form');
    if (post_form) {
        post_form.onsubmit = () => {
            fetch('/new_post', {
                'method': 'post'
            })
        } 
    }
})