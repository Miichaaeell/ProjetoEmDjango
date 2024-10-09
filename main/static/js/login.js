const olho = document.querySelector('#olho')
const senha = document.querySelector('#password')
olho.addEventListener('click', () => {
    senha.type = senha.type == 'text' ? 'password' : 'text'
    olho.innerHTML = senha.type == 'text' ? 'visibility_off' : 'visibility'
})
