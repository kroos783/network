
function likeFunction(id) {

    let LikeButton = document.querySelector(`#buttonLike${id}`);


    fetch('/like/' + id)
    .then(response => response.json())
    .then(like => {
                
        if (LikeButton.innerHTML === 'Like')
            LikeButton.innerHTML = 'Unlike';
        else
            LikeButton.innerHTML = 'Like';

        let likeScore = JSON.parse(like.like_count)
        let LikedScore = document.querySelector(`#liked${id}`);

        LikedScore.innerHTML = `Like : ${likeScore}`;

    })
}