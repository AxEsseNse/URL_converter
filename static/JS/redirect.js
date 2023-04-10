function redirect() {
    const response_log = document.getElementById('responselog').textContent
    console.log(response_log)
    const temp = document.getElementById('redirect').textContent;
    const obj = new Object({
        name: temp
    })
    document.location.href = temp
}