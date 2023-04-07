function mainEvent() {
    const data = document.getElementById('inputField').value

    obj_for_request = new Object({
        url: data
    })
    fetch('http://127.0.0.1:5000/api', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
    },
        body: JSON.stringify(obj_for_request)                
    }).then(response => {
        return response.json()
    }).then(server_data => {
        const short_url = server_data.data
        const change_field = document.getElementById('server_response')
        change_field.innerHTML = short_url
    })
}