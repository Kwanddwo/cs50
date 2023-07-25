import { getCookie, likeHandler, editHandler, createPostCard } from "./common.mjs";

let page = 1;
  
const csrftoken = getCookie('csrftoken');

// Rendering a page of the feed
function page_feed(page) {
    fetch(`/all_posts/${page}`)
    .then(response => response.json())
    .then(posts => {
        document.querySelector('#post-feed').innerHTML = '';
        for (const post of posts) {
            const post_card = createPostCard(post); 
            document.querySelector('#post-feed').appendChild(post_card);

            if (page <= 1) {
                document.querySelector('#previous').style.display = 'none';
            } else {
                document.querySelector('#previous').style.display = 'block';
            }

            fetch('/max_page/index')
            .then(response => response.json())
            .then(response => parseInt(response['page_max']))
            .then(page_max => {
                if (page >= page_max) {
                    document.querySelector('#next').style.display = 'none';
                } else {
                    document.querySelector('#next').style.display = 'block';
                }
            });
        }
    });
}

// Like clicking
document.addEventListener('click', (event) => {
    likeHandler(event, csrftoken);
});

document.addEventListener('click', (event) => {
    editHandler(event, csrftoken);
});

document.addEventListener('DOMContentLoaded', () => {
    page_feed(page);

    document.querySelector('#next').onclick = () => {
        fetch('/max_page/index')
        .then(response => response.json())
        .then(response => parseInt(response['page_max']))
        .then(page_max => {
            if (page < page_max) {
                page++;
                window.scrollTo({
                    top: 100,
                    behavior: "smooth",
                });
                page_feed(page);
            }
        })
    }
    document.querySelector('#previous').onclick = () => {
        if (page > 1) {
            page--;
            window.scrollTo({
                top: 100,
                behavior: "smooth",
            });
            page_feed(page);
        }
    }

    const post_form = document.querySelector('#form-post');
    
    if (post_form) {
        post_form.onsubmit = () => {
            fetch('/new_post', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken, // Include the CSRF token in the header
                },
                body: JSON.stringify({
                    text: document.querySelector('#form-body').value
                })
            })
            .then(response => response.json())
            .then(response => {
                if ("message" in response) {
                    console.log(response.message);
                    page = 1;
                    page_feed(page);
                    document.querySelector('#form-body').value = '';
                    const post = response.post;
                    const post_card = createPostCard(post, {
                        new: true
                    });
                    document.querySelector('#post-feed').insertBefore(post_card, document.querySelector('#post-feed').firstChild);
                    post_card.style.animationPlayState = 'running';
                } else {
                    document.querySelector('#form-message').innerHTML = response.error;
                }
            });

            // Don't reload page on form submit
            return false;
        }
    }
});