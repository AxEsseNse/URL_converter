function redirect() {
    const temp = document.getElementById('redirect').textContent;
    const obj = new Object({
        name: temp
    })
    document.location.href = temp
}