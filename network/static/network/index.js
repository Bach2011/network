document.addEventListener('DOMContentLoaded', function() {
    //disabled button
if(document.querySelector("#post")){
    document.querySelector('#post').disabled = true;
    document.querySelector('textarea').onkeyup = () => {
        if(document.querySelector('textarea').value.trim().length > 0){
            document.querySelector('#post').disabled = false;
        }else {
            document.querySelector('#post').disabled = true;
        }
    } 
}
    document.querySelectorAll('.edit').forEach(button => {
        button.onclick = function() {
            alert(button.className)
        }
    })
})
function edit(post_id) {
    new_content = document.querySelector(`#edit_post${post_id}`)
}