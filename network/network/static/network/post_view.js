import { getCookie, likeHandler, editHandler, createPostCard } from "./common.mjs";

const csrftoken = getCookie('csrftoken');

let page = 1;

function render_post(post_id) {
    fetch(`/post/${post_id}`)
    .then(response => response.json())
    .then(post => {
        const post_card = createPostCard(post);
        document.querySelector('#post-view').appendChild(post_card);
    })
}

function render_comments(post_id, page) {
    fetch(`/comments/${post_id}/${page}`)
    .then(response => response.json())
    .then(comments => {
        document.querySelector('#comment-feed').innerHTML = '';
        for (const comment of comments) {
            const comment_card = document.createElement('div');
            comment_card.className = "container border border-black m-2 p-2";
            comment_card.innerHTML = `
                <h5><a href='/user/${comment.user}'>${comment.user}</a></h5>
                <p>${comment.text}</p>
                <small><weak>${comment.timestamp}</weak></small>
            `;

            document.querySelector('#comment-feed').appendChild(comment_card);

            if (page <= 1) {
                document.querySelector('#previous').style.display = 'none';
            } else {
                document.querySelector('#previous').style.display = 'block';
            }

            fetch(`/max_page_comments/${post_id}`)
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

document.addEventListener('click', (event) => {
    likeHandler(event, csrftoken);
});

document.addEventListener('click', (event) => {
    editHandler(event, csrftoken);
})

document.addEventListener('DOMContentLoaded', () => {
    const post_id = document.querySelector('#post_id').dataset.id;
    render_post(post_id);
    render_comments(post_id, page);

    document.querySelector('#next').onclick = () => {
        fetch(`/max_page_comments/${post_id}`)
        .then(response => response.json())
        .then(response => parseInt(response['page_max']))
        .then(page_max => {
            if (page < page_max) {
                page++;
                window.scrollTo({
                    top: 100,
                    behavior: "smooth",
                });
                render_comments(post_id, page);
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
            render_comments(post_id, page);
        }
    }

    const comment_form = document.querySelector("#comment-form");

    if (comment_form) {
        comment_form.onsubmit = () => {
            fetch(`/new_comment/${post_id}`, {
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
                    document.querySelector('#form-body').value = '';
                    const comment = response.comment;
                    const comment_card = document.createElement('div');
                    comment_card.className = "container border border-black m-2 p-2 new-comment";
                    comment_card.innerHTML = `
                        <h5><a href='/user/${comment.user}'>${comment.user}</a></h5>
                        <p>${comment.text}</p>
                        <small><weak>${comment.timestamp}</weak></small>
                    `;

                    document.querySelector('#comment-feed').insertBefore(comment_card, document.querySelector('#comment-feed').firstChild);
                    comment_card.style.animationPlayState = 'running';
                } else {
                    document.querySelector('#form-message').innerHTML = response.error;
                }
            });

            // Don't reload page on form submit
            return false;
        }
    }
});