import { getCookie, likeHandler, editHandler, createPostCard } from "./common.mjs";

let page = 1;
  
const csrftoken = getCookie('csrftoken');

// Rendering a page of the feed
function user_feed(user_v, page) {
    fetch(`/user_posts/${user_v}/${page}`)
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

            fetch(`/max_page/${user_v}`)
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
    likeHandler(event, csrftoken);
});

document.addEventListener('click', (event) => {
    editHandler(event, csrftoken);
});

document.addEventListener('DOMContentLoaded', () => {
    const user_v = document.querySelector('#user-v').dataset.username;
    const follow_button = document.querySelector('#follow-button');
    if (follow_button.dataset.follow === "true") {
        follow_button.onclick = (e) => {
            if (follow_button.dataset.following === "true") {
                fetch("/unfollow", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken, // Include the CSRF token in the header
                    },
                    body: JSON.stringify({
                        username: user_v
                    })
                })
                .then(response => response.json())
                .then(response => {
                    if ('message' in response)
                    {
                        follow_button.className = "btn btn-primary";
                        follow_button.dataset.following = "false";
                        follow_button.innerHTML = "Follow";
                        const count = document.querySelector('#follower-count');
                        count.innerHTML = parseInt(count.innerHTML) - 1;
                    }
                });
            } else {
                fetch("/follow", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken, // Include the CSRF token in the header
                    },
                    body: JSON.stringify({
                        username: user_v
                    })
                })
                .then(response => response.json())
                .then(response => {
                    if ('message' in response)
                    {
                        follow_button.className = "btn btn-secondary";
                        follow_button.dataset.following = "true";
                        follow_button.innerHTML = "Unfollow";
                        const count = document.querySelector('#follower-count');
                        count.innerHTML = parseInt(count.innerHTML) + 1;
                    }
                });
            }
        }
    }
    user_feed(user_v, page);

    document.querySelector('#next').onclick = () => {
        fetch(`/max_page/${user_v}`)
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

