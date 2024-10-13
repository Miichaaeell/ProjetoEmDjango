const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat-socket/`)
chatSocket.onmessage = (event) => {
    let data = JSON.parse(event.data)
    console.log(data)
    if (data.type === 'new_message'){
        let conversa = document.getElementById(`${data.id}`)
        conversa.style.backgroundImage = "linear-gradient(to right, red, orange)"
        let msg = document.getElementById(`mensagem_${data.id}`)
        msg.innerHTML = data.message 
    }
    else if (data.type === 'reply_message'){
        let msg = document.getElementById(`mensagem_${data.id}`)
        msg.innerHTML = data.message
        let conversa = document.getElementById(`${data.id}`)
        conversa.style.backgroundImage = 'none'
    }
    
}

function abrir(id){
    var conversa = document.getElementById(`${id}`)
    conversa.style.backgroundImage = 'none'
    
}