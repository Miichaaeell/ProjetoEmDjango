const chatSocket = new WebSocket(`wss://${window.location.host}`)
const form = document.getElementById('form')
const form_end_atendimento = document.getElementById('form_end_atendimento')
const id_client = document.getElementById('id_client').textContent
chatSocket.onmessage = (event) => {
    let data = JSON.parse(event.data)
    console.log(data)
    if (data.type === 'new_message' && data.id == id_client){
        window.location.reload()
    }
}

form.addEventListener('submit', (event)=>{
    let message = event.target.mensagem.value
    chatSocket.send(JSON.stringify({
        'type':'reply_message',
        'message':message,
        'id': id_client
    }))
})

form_end_atendimento.addEventListener('submit', (event) => {
    chatSocket.send(JSON.stringify({
        'type':'reply_message',
        'message':'end',
        'id': id_client
    }))
})