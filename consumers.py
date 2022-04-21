import json

from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

class MySocket(WebsocketConsumer):
    def connect(self):
        
        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        self.send(text_data=json.dumps({
            'type':'connection-response',
            'message':'connection accepted from host',
        }))
        
        
    def receive(self,text_data):
        json_data = json.loads(text_data)
        info = json_data['message']
        print("Message: ",info)
        
        self.send(text_data = json.dumps({
            'type':'response',
            'message':info
        }))
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'Another_message',
                'message':info
            }
        )
    def Another_message(self,event):
        message = event['message']
        
        self.send(text_data = json.dumps({
            'type':'response',
            'message':message
        }))
        
    # def receive(self,data):
    #     json_data = json.loads(data)
    #     info = json_data['message']
    #     print("Message: ",info)
        
    #     self.send(data = json.dumps({
    #         'type':'response',
    #         'message':info
    #     }))