document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    //document.querySelector('#allposts').addEventListener('click', () => load_posts('allposts'));
    //document.querySelector('#allposts').addEventListener('click', () => load_posts('show_posts'));
    //document.querySelector('#compose-form').addEventListener('submit', submit_post);
  
    // By default, load the inbox
    //load_posts('userPage');
  });


function followFunction(id) {

    let FollowButton = document.querySelector("#buttonFollow");


    fetch('/follow/' + id)
    .then(response => response.json())
    .then(follow => {
                
        if (FollowButton.innerHTML === 'Follow')
            FollowButton.innerHTML = 'Unfollow';
        else
            FollowButton.innerHTML = 'Follow';

        let followScore = JSON.parse(follow.follower_count)
        let followedScore = document.querySelector("#followed");

        followedScore.innerHTML = `Followed : ${followScore}`;

    })
}


function load_posts(posts) {

    document.querySelector("#posts_view").innerHTML = "";

    fetch('/posts/' + posts)
        .then(response => response.json())
        .then(posts => {
            let posts_view = document.querySelector("#posts_view");

            posts.forEach(post => {
                let div = document.createElement('div');
                
                
                div.innerHTML = `
                <div class="owner col-3"> From : <a href="{% url 'userPage' post.user %}"><strong>{{post.user}}</strong></a></div>
                <div class="body col-5"> Message : <strong>{{post.body}}</strong></div>
                <div class="timestamp col-3">{{post.timestamp}}</div>
                `
                
                

                
                posts_view.appendChild(div);
            });
        })
}