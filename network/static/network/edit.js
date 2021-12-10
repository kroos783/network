function editFunction(id) {

    let ButtonEdit = document.querySelector(`#buttonEdit${id}`);
    let PostEdit = document.querySelector(`#postBody${id}`);

    ButtonEdit.innerHTML = ``


    fetch('/edit/' + id)
    .then(response => response.json())
    .then(post => {
        PostEdit.innerHTML = `
        <form id="compose-form">
        <textarea
          class="form-control"
          id="compose-body${id}"
          placeholder="Body"
        >${post.post}</textarea>
        <button class="btn btn-sm btn-primary m-3 ml-4" onclick="editSubmit('${id}')">Submit</button>
        <button class="btn btn-sm btn-primary m-3 ml-4" onclick="cancelFunction('${id}')">Cancel</button>
        </form>`

    })
}

function cancelFunction(id) {
    let ButtonEdit = document.querySelector(`#buttonEdit${id}`);
    let PostEdit = document.querySelector(`#postBody${id}`);
    ButtonEdit.innerHTML = `<button class="btn btn-sm btn-primary m-3 ml-4" onclick="editFunction('${id}')">Edit</button>`;
    
    fetch('/edit/' + id)
    .then(response => response.json())
    .then(post => {
        PostEdit.innerHTML = ` Message : <strong>${post.post}</strong>`;
    })
}

function editSubmit(id) {
    
    let ButtonEdit = document.querySelector(`#buttonEdit${id}`);
    let PostEdit = document.querySelector(`#postBody${id}`);

    const body = document.querySelector(`#compose-body${id}`).value;
    console.log(body)

    fetch('/edit/submit', {
        credentials: 'include',
        method: "POST",
        mode : 'same-origin',
        headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            body: body,
            postid: id
        })
    })
    .then(response => response.json())
    .then(result => {
        ButtonEdit.innerHTML = `<button class="btn btn-sm btn-primary m-3 ml-4" onclick="editFunction('${id}')">Edit</button>`;
        PostEdit.innerHTML = ` Message : <strong>${result.post}</strong>`;
    })
}