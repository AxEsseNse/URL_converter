function mainEvent() {
    const data = document.getElementById('inputField').value;
    
    obj_for_request = new Object({
        url: data
    })

    fetch('http://127.0.0.1:5000/api/main', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
    },
        body: JSON.stringify(obj_for_request)                
    }).then(response => {
        return response.json();
    }).then(server_info => {
        console.log(server_info.comment);
        return server_info.data;
    }).then(server_data => {
        if (server_data == 'incorrect url') {
            document.getElementById('response_collapse').classList.remove("show");
            document.getElementById('flashmessage').innerHTML = 'Введенная ссылка некорректна';
            setTimeout(function() {
                document.getElementById('flashmessage').innerHTML = '';
            }, 5000)
            return
        }
        document.getElementById('flashmessage').innerHTML = '';
        const short_url = server_data
        const div_for_link = document.getElementById('short_url')
        const link = document.createElement('a')
        link.href = short_url
        link.title = 'Ваша ссылка'
        link.appendChild(document.createTextNode(short_url))
        div_for_link.replaceChildren(link)
        const collapse_element = document.getElementById('response_collapse')
        collapse_element.classList.add("show")
    })
}


function copyURL() {
    const short_url = document.getElementsByTagName('a')[0].href;
    hidden_field = document.createElement('input');
    hidden_field.value = short_url;
    const dop_div = document.getElementById('hidden_div');
    dop_div.appendChild(hidden_field);
    hidden_field.select();
    document.execCommand('copy');
    dop_div.removeChild(hidden_field);
}

function feedback() {
    const feedback = document.getElementById('feedbackmessage').value;

    if (feedback == '') {
        const flash_field = document.getElementById('flashmessagemodal');
        if (!flash_field.classList.contains('text-danger')) {
            flash_field.classList.add('text-danger');
        }
        if (flash_field.classList.contains('text-success')) {
            flash_field.classList.remove('text-success');
        }
        flash_field.innerHTML = 'Сообщение не должно быть пустым';
        document.getElementById('flashmessagemodaldate').innerHTML = '';
        setTimeout(function() {
            document.getElementById('flashmessagemodal').innerHTML = '';
        }, 1000);
        return
    } else {
        document.getElementById('flashmessagemodal').innerHTML = '';
    }

    obj_for_request = new Object({
        msg: feedback
    })

    fetch('http://127.0.0.1:5000/api/feedback', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
    },
        body: JSON.stringify(obj_for_request)                
    }).then(response => {
        return response.json()
    }).then(server_data => {
        const response = server_data.data;
        const way = server_data.code;
        const flash_field = document.getElementById('flashmessagemodal');
        const flash_field2 = document.getElementById('flashmessagemodaldate');
        if (way) {
            if (flash_field.classList.contains('text-danger')) {
                flash_field.classList.remove('text-danger');
            }
            if (!flash_field.classList.contains('text-success')) {
                flash_field.classList.add('text-success');
            }
            flash_field.innerHTML = response
            const feedback_date = server_data.date
            flash_field2.innerHTML = feedback_date
        } else {
            if (!flash_field.classList.contains('text-danger')) {
                flash_field.classList.add('text-danger');
            }
            if (flash_field.classList.contains('text-success')) {
                flash_field.classList.remove('text-success');
            }
            flash_field.innerHTML = response
            const feedback_date = server_data.date
            flash_field2.innerHTML = feedback_date
        }
    })
}

