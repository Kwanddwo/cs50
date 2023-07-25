import { getCookie, likeHandler, editHandler, createPostCard } from "./common.mjs";
  
let page = 1;
  
const csrftoken = getCookie('csrftoken');

// Rendering a page of the feed
function following_feed(page) {
    fetch(`/following_posts/${page}`)
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

            fetch('/max_page_following')
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
    likeHandler(event);
});

document.addEventListener('click', (event) => {
    editHandler(event);
})

document.addEventListener('DOMContentLoaded', () => {
    following_feed(page);

    document.querySelector('#next').onclick = () => {
        fetch('/max_page_following')
        .then(response => response.json())
        .then(response => parseInt(response['page_max']))
        .then(page_max => {
            if (page < page_max) {
                page++;
                window.scrollTo({
                    top: 100,
                    behavior: "smooth",
                });
                following_feed(page);
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
            following_feed(page);
        }
    }
});