const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat-socket/`)
const form = document.getElementById('form')
var id_client = document.getElementById('id_client').textContent
chatSocket.onmessage = (event) => {
    let data = JSON.parse(event.data)
    console.log(data)
    if (data.type === 'new_message' && data.id == id_client){
        window.location.reload()
    }
}

form.addEventListener('submit', (event)=>{
    let message = event.target.mensagem.value
    console.log(message)
    chatSocket.send(JSON.stringify({
        'type':'reply_message',
        'message':message,
        'id': id_client
    }))
})
