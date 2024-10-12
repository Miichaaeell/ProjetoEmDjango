const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat-socket/`)
chatSocket.onmessage = (event) => {
    let data = JSON.parse(event.data)
    console.log(data)
    if (data.type === 'new_message'){
        let conversa = document.getElementById(`${data.id}`)
        conversa.style.backgroundImage = "linear-gradient(to right, red, orange)"
        let msg = document.getElementById('mensagem')
        msg.innerHTML = data.message 
    }
    
}


function receber_msg(id){
    var conversa = document.getElementById(`${id}`)
    conversa.style.backgroundImage = "linear-gradient(to right, red, orange)"
    var msg = document.getElementById('mensagem')
    msg.innerHTML = 'Teste'
}
function abrir(id){
    var conversa = document.getElementById(`${id}`)
    conversa.style.backgroundImage = 'none'
    
}