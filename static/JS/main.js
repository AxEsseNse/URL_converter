function flashMessage() {
    const flash_field = document.getElementById('flashmessage');
    flash_field.innerHTML = 'Введенная ссылка некорректна';
    setTimeout(function() {
        const flash_field = document.getElementById('flashmessage');
        flash_field.innerHTML = '';
    }, 5000)
}

function isCorrectURL(url) {
    if (url.startsWith('https://www.')) {
        return true
    }
    if (url.startsWith('http://www.')) {
        return true
    }
    if (url.startsWith('www.')) {
        return true
    }
    return false
}

function mainEvent() {
    const data = document.getElementById('inputField').value
    if (!isCorrectURL(data)) {
        flashMessage()
        return
    }

    const flash_field = document.getElementById('flashmessage');
    flash_field.innerHTML = '';

    obj_for_request = new Object({
        url: data.startsWith('www.') ? 'http://' + data : data
    })

    fetch('http://127.0.0.1:5000/api/main', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
    },
        body: JSON.stringify(obj_for_request)                
    }).then(response => {
        return response.json()
    }).then(server_data => {
        const short_url = server_data.data
        const div_for_link = document.getElementById('short_url')
        const link = document.createElement('a')
        link.href = short_url
        link.title = 'Ваша ссылка'
        link.appendChild(document.createTextNode(short_url))
        div_for_link.replaceChildren(link)
        const collapse = document.getElementById('response_collapse')
        collapse.classList.add("show")
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
        flash_field.classList.remove('text-success');
        flash_field.classList.add('text-danger');
        flash_field.innerHTML = 'Сообщение не должно быть пустым';
        setTimeout(function() {
            const flash_field = document.getElementById('flashmessagemodal');
            flash_field.innerHTML = '';
        }, 5000);
        return
    } else {
        const flash_field = document.getElementById('flashmessagemodal');
        flash_field.innerHTML = '';
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
        const flash_field = document.getElementById('flashmessagemodal');
        if (response == 'success') {
            const flash_msg = 'Сообщение успешно отправлено';
            flash_field.classList.remove('text-danger');
            flash_field.classList.add('text-success');
            flash_field.innerHTML = flash_msg;
        } else {
            flash_field.classList.remove('text-success');
            flash_field.classList.add('text-danger');
            const flash_msg = 'Ошибка соединение с сервером';
            flash_field.innerHTML = flash_msg;
        }
    })
}

