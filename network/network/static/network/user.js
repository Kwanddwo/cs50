const NOT_LIKED_INNERHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-heart" viewBox="0 0 16 16">
        <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
    </svg>
`;
const LIKED_INNERHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-heart-fill" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
    </svg>
    `;

let page = 1;

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
  
const csrftoken = getCookie('csrftoken');

// Rendering a page of the feed
function user_feed(user_v, page) {
    fetch(`/user_posts/${user_v}/${page}`)
    .then(response => response.json())
    .then(posts => {
        document.querySelector('#post-feed').innerHTML = '';
        for (const post of posts) {
            const post_card = document.createElement('div');
            post_card.className = "container border border-black m-2 p-2";
            post_card.innerHTML = `
                <h5><a href='/user/${post.user}'>${post.user}</a></h5>
                <p>${post.text}</p>
                <small><weak>${post.timestamp}</weak></small>
            `;

            const like_div = document.createElement('div');
            like_div.className = "row";
            like_div.id = `like-row-${post.id}`;
            
            const like_button = document.createElement('div');
            like_button.className = "mx-3";
            like_button.id = `like-button-${post.id}`;
            if (post.liked) {
                like_button.classList.add("liked");
                like_button.innerHTML = LIKED_INNERHTML;
            } else {
                like_button.innerHTML = NOT_LIKED_INNERHTML;
            }

            like_div.appendChild(like_button);
            like_div.innerHTML += `
                <weak id="like-count-${post.id}">${post.like_count}</weak>
                <a href='#' class=" mr-4 ml-auto">Comment</a>
            `;
            post_card.appendChild(like_div);
            document.querySelector('#post-feed').appendChild(post_card);

            if (page <= 1) {
                document.querySelector('#previous').style.display = 'none';
            } else {
                document.querySelector('#previous').style.display = 'block';
            }

            fetch('/max_page')
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
    })
}

// Like clicking
document.addEventListener('click', (event) => {
    try {
        const svg = event.target.closest('svg');
        const like_div = svg.parentElement;
        if ((event.target.nodeName === 'path' || event.target.nodeName === 'svg') && like_div.id.match(/like-button-/)) {
            const post_id = like_div.id.replace("like-button-", "");

            if (like_div.classList.contains("liked")) {
                fetch(`/like/${post_id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken, // Include the CSRF token in the header
                      },
                    body: JSON.stringify({
                        like: false
                    })
                })
                .then(response => response.json())
                .then(response => {
                    if ("message" in response) {
                        like_div.innerHTML = NOT_LIKED_INNERHTML;
                        like_div.classList.remove("liked");
                        document.querySelector(`#like-count-${post_id}`).innerHTML = parseInt(document.querySelector(`#like-count-${post_id}`).innerHTML) - 1;
                    }
                })
                .catch(error => {
                    alert('You have to be logged in to like a post!')
                });
            }
            else {
                fetch(`/like/${post_id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken, // Include the CSRF token in the header
                      },
                    body: JSON.stringify({
                        like: true
                    })
                })
                .then(response => response.json())
                .then(response => {
                    if ("message" in response) {
                        like_div.innerHTML = LIKED_INNERHTML;
                        like_div.classList.add("liked");
                        document.querySelector(`#like-count-${post_id}`).innerHTML = parseInt(document.querySelector(`#like-count-${post_id}`).innerHTML) + 1;
                    }
                })
                .catch(error => {
                    alert('You have to be logged in to like a post!')
                });
            }
        }
    }
    catch (error) {
        if (!error instanceof TypeError)
        {
            throw (error)
        }
    }
});

function follow_click_handler(user_v) {
    fetch(`follow/${user_v}`)
    .then(response => response.json())
    .then(response => {console.log(response)});
}

document.addEventListener('DOMContentLoaded', () => {
    const user_v = document.querySelector('#user-v').dataset.username;
    const follow_button = document.querySelector('#follow-button')
    if (follow_button.data.follow) {
        follow_button.onclick = () => {follow_click_handler(user_v)};
    }
    user_feed(user_v, page);

    document.querySelector('#next').onclick = () => {
        fetch('/max_page')
        .then(response => response.json())
        .then(response => parseInt(response['page_max']))
        .then(page_max => {
            if (page < page_max) {
                page++;
                window.scrollTo({
                    top: 150,
                    behavior: "smooth",
                });
                user_feed(user_v, page);
            }
        })
    }
    document.querySelector('#previous').onclick = () => {
        if (page > 1) {
            page--;
            window.scrollTo({
                top: 150,
                behavior: "smooth",
            });
            user_feed(user_v, page);
        }
    }
})

