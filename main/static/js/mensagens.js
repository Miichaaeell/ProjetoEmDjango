const janela_mensagens = document.getElementById('mensagens')
function scroll(){ 
    janela_mensagens.scroll(0, janela_mensagens.scrollHeight)
}

function receber_msg(){
    location.reload()
}
