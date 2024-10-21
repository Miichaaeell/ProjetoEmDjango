const chatSocket = new WebSocket(`wss://${window.location.host}/ws/chat-socket/`)
Notification.requestPermission()
const img = '../image/whats_ico.ico'


chatSocket.onmessage = (event) => {
    let data = JSON.parse(event.data)
    console.log(data)
    if (data.type === 'new_message'){
        notify(title=`${data.message.name} new message`, body=data.message.body)
    }
}
function clicou(){
    alert('clicou')
    const sound = new Audio('../media/sound/notification.mp3')
    sound.play()
}
function notify(title, body){
    new Notification(title,{
        body: body,
        icon: img,
        requireInteraction: true
        })

}
