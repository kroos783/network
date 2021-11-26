document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    //document.querySelector('#allposts').addEventListener('click', () => load_posts('allposts'));
    //document.querySelector('#allposts').addEventListener('click', () => load_posts('show_posts'));
    document.querySelector('#compose-form').addEventListener('submit', submit_post);
  
    // By default, load the inbox
    load_posts('show_posts');
  });

function load_posts(posts) {

    fetch('/posts/' + posts)
        .then(response => response.json())
        .then(posts => {
            let posts_view = document.querySelector("#posts_view");

            posts.forEach(post => {
                let div = document.createElement('div');

                div.innerHTML = `
                <div class="owner col-3"> From : <strong>${post.user}</strong></div>
                <div class="body col-5"> Message : <strong>${post.body}</strong></div>
                <div class="timestamp col-3">${post.timestamp}</div>
                `

                posts_view.appendChild(div);
            });
        })
}

function submit_post(event) {
    // Change behavor if needed
    event.preventDefault();
  
    // Create variables and save data form for send to db
    const user = document.querySelector('#compose-user').value;
    const body  = document.querySelector('#compose-body').value;
    var csrftoken = getCookie('csrftoken');

    // Send data to db server
    fetch('/posts', {
      credentials: 'include',
      method: "POST",
      mode: 'same-origin',
      headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({
        user: user,
        body: body,
        
      })
    })
    .then(response => response.json())
    .then(result => { 
      console.log(result);
      load_posts('show_posts');
    })
  }

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}