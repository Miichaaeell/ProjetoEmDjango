from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name="chat"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print('New Connection Success')
        
        await self.send(text_data=json.dumps({
            'type':'Connections',
            'message':'Connection Success!'
        }))

    async def receive(self, text_data):
        message_json = json.loads(text_data)
        if message_json['type'] == 'new_message':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type":"new_message",
                    "text":{
                        'message':message_json['message'],
                        'id':message_json['id']
                    }
                }
            )
        elif message_json['type'] == 'reply_message':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type':'reply_message',
                    "text":{
                        'message':message_json['message'],
                        'id':message_json['id']
                    }
                }
            )

    async def new_message(self, event):   
        print(event)
        await self.send(text_data=json.dumps({
            'type':'new_message',
            'message': event['text']['message'],
            'id': event['text']['id']
            }))
    
    async def reply_message(self, event):
        await self.send(text_data=json.dumps({
            'type':'reply_message',
            'message':event['text']['message'],
            'id':event['text']['id']
            })
        )


    

       