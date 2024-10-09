function receber_msg(id){
    var conversa = document.getElementById(`${id}`)
    conversa.style.backgroundImage = "linear-gradient(to right, red, orange)"
    var msg = document.getElementById('mensagem')
    msg.innerHTML = 'Teste'
}
function abrir(id){
    var conversa = document.getElementById(`${id}`)
    conversa.style.backgroundColor = "rgba(211, 211, 211, 0.479)"
}