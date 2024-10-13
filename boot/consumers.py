from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'Atendimento'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        print('New Connection Success')
        self.send(text_data=json.dumps({
            'type':'Connections',
            'message':'Connection Success!'
        }))

    def receive(self, text_data):
        message_json = json.loads(text_data)
        if message_json['type'] == 'new_message':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'new_message',
                    'message': message_json['message'],
                    'id': message_json['id']

                }
            )
        elif message_json['type'] == 'reply_message':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'reply_message',
                    'message': message_json['message'],
                    'id': message_json['id']

                }
            )

    def new_message(self, event):        
        self.send(text_data=json.dumps({
            'type':'new_message',
            'message': event['message'],
            'id': event['id']
            })
        )
    
    def reply_message(self, event):
        self.send(text_data=json.dumps({
            'type':'reply_message',
            'message':event['message'],
            'id': event['id']
            })
        )

    

       