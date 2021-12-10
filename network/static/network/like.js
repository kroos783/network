document.addEventListener('DOMContentLoaded', function() {

  });

function load_like(id) {
    
    fetch('/like/count/' + id)
    .then(response => response.json())
    .then(like => {
        let LikeButton = document.querySelector(`#buttonLike${id}`);
        let LikedScore = document.querySelector(`#liked${id}`);
        if (like.liked)
            LikeButton.innerHTML = '<img src="../static/network/liked.png"/> Unlike';
        else
            LikeButton.innerHTML = '<img src="../static/network/like.png"/> Like';
        let likeScore = JSON.parse(like.like_count)
        LikedScore.innerHTML = `Like : ${likeScore}`;
    })
}


function load_like_nologgin(id) {
    
    fetch('/like/countnotloggin/' + id)
    .then(response => response.json())
    .then(like => {
        let LikeButton = document.querySelector(`#buttonLike${id}`);
        let LikedScore = document.querySelector(`#liked${id}`);
        LikeButton.innerHTML = '<img src="../static/network/like.png"/> Like';
        let likeScore = JSON.parse(like.like_count)
        LikedScore.innerHTML = `Like : ${likeScore}`;
    })
}


function likeFunction(id) {

    let LikeButton = document.querySelector(`#buttonLike${id}`);


    fetch('/like/' + id)
    .then(response => response.json())
    .then(like => {
                
        if (like.liked)
            {LikeButton.innerHTML = '<img src="../static/network/liked.png"/> Unlike';}
        else
            {LikeButton.innerHTML = '<img src="../static/network/like.png"/> Like';}

        let likeScore = JSON.parse(like.like_count)
        let LikedScore = document.querySelector(`#liked${id}`);

        LikedScore.innerHTML = `Like : ${likeScore}`;

    })
}