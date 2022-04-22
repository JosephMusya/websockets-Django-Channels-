import json

from channels.generic.websocket import AsyncWebsocketConsumer

#from asgiref.sync import async_to_sync

class MySocket(AsyncWebsocketConsumer):
    async def connect(self):
        print("PATH",self.scope['path'])
        print("USER",self.scope['user'])

        self.room_group_name = 'test'
        await (self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name #Auto generated
        )
        
        await self.accept()
        await self.send(text_data=json.dumps({
            'type':'connection-response',
            'message':'connection accepted from host',
        }))
        
        
    async def receive(self,text_data):
        json_data = json.loads(text_data)
        info = json_data['message']
        print("Message: ",info)
        
        await self.send(text_data = json.dumps({
            'type':'response',
            'message':info
        }))
        
        await (self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'Another_message',
                'message':info
            }
        )
    async def Another_message(self,event):
        message = event['message']
        
        await self.send(text_data = json.dumps({
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