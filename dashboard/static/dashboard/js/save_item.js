console.log('save_item.js loaded')

document.querySelectorAll('.save-btn').forEach(button => {

    button.addEventListener('click', async () => {
        const itemId = button.getAttribute('data-item-id')

        const res = await fetch(`toggle-save-item/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
        })

        if (!res.ok) {
            console.error('Failed to toggle save status')
            console.error(await res.text())
            return
        } else {
            console.log('Toggled save status successfully')
            const data = await res.json()
            console.log('Response data:', data)
            button.dataset.saved = data.saved
            if (data.saved) {
                button.classList.add('saved')
            } else {
                button.classList.remove('saved')
            }
        }


    })
})


// src: http://forum.djangoproject.com/t/send-views-py-request-post-with-javascript/23146/9
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}