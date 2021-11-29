document.addEventListener('DOMContentLoaded', function() {
    //disabled button
    document.querySelector('#post').disabled = true;
    document.querySelector('textarea').onkeyup = () => {
        if(document.querySelector('textarea').value.length > 0){
            document.querySelector('#post').disabled = false;
        }else {
            document.querySelector('#post').disabled = true;
        }
    }
    document.querySelector('form').onsubmit = post;
    document.querySelector('.like').addEventListener('click', function() {
        if(this.style.color == "red"){
            document.querySelector('.likes').innerText = 0;
            this.style.color = 'black'
            this.className = 'far fa-heart'
        }else {
            document.querySelector('.likes').innerText = 1;
            this.style.color = 'red';
            this.className = 'fas fa-heart'
        }
    })
})
function post() {
    let content = document.querySelector('textarea').value;
    fetch('/post', {
        method: "POST",
        body: JSON.stringify({
            content: content
        })
    })
    .then(response => response.json())
    .then(data => {
        if(!data.error){
            console.log("haha")
        }
    })
}