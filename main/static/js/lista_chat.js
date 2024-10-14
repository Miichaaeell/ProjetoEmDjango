const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat-socket/`)
Notification.requestPermission()
const song = ''
song.src = `/sound/notification.mp3`
const ico = ''
ico.src = `/image/whats_ico.ico`
chatSocket.onmessage = (event) => {
    let data = JSON.parse(event.data)
    console.log(data)
    if (data.type === 'new_message'){
        let conversa = document.getElementById(`${data.id}`)
        conversa.style.backgroundImage = "linear-gradient(to right, red, orange)"
        let msg = document.getElementById(`mensagem_${data.id}`)
        msg.innerHTML = data.message
        console.log(data)
        notify(title="New Message", body=data.message)

    }
    else if (data.type === 'reply_message'){
        let msg = document.getElementById(`mensagem_${data.id}`)
        msg.innerHTML = data.message
        let conversa = document.getElementById(`${data.id}`)
        conversa.style.backgroundImage = 'none'
    }
    
}
function notify(title, body){
    new Notification(title,{
        body: body,
        icon: ico
})
    const audio = new Audio(song)
    audio.play()
}

function abrir(id){
    var conversa = document.getElementById(`${id}`)
    conversa.style.backgroundImage = 'none'
    
}