const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat-socket/`)
Notification.requestPermission()
const ico = "https://via.placeholder.com/50x50"

chatSocket.onmessage = (event) => {
    let data = JSON.parse(event.data)
    if (data.type === 'new_message'){
        notify(title="New Message", body=data.message)
    }
}
function clicou(){
    alert('clicou')
    const sound = new Audio('/main/static/sound/notification.mp3')
    sound.play()
   
}
function notify(title, body){
    new Notification(title,{
        body: body,
        icon: ico,
        })

}
