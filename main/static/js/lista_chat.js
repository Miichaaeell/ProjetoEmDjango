const chatSocket = new WebSocket(`wss://${window.location.host}/ws/chat-socket/`)
Notification.requestPermission()
chatSocket.onmessage = (event) => {
    let data = JSON.parse(event.data)
    if (data.type === 'new_message'){
        let conversa = document.getElementById(`${data.id}`)
        conversa.style.backgroundImage = "linear-gradient(to right, red, orange)"
        let msg = document.getElementById(`mensagem_${data.id}`)
        msg.innerHTML = data.message['body']
        console.log(data)


    }
    else if (data.type === 'reply_message'){
        var msg = document.getElementById(`mensagem_${data.id}`)
        var conversa = document.getElementById(`${data.id}`)
        if (data.message !='end'){
            msg.innerHTML = data.message
            conversa.style.backgroundImage = 'none'
        }
        else {
            conversa.remove()
        }
    }

    
}
function abrir(id){
    var conversa = document.getElementById(`${id}`)
    conversa.style.backgroundImage = 'none'
    
}