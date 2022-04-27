import json

from channels.generic.websocket import AsyncWebsocketConsumer

from channels.db import database_sync_to_async

from .models import Values
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
from .serializers import ValueSerializer
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.mixins import ListModelMixin

from django.contrib.auth.models import User
#from asgiref.sync import async_to_sync

class MySocket(GenericAsyncAPIConsumer,
               ListModelMixin,):

    queryset = Values.objects.all()
    serializer_class = ValueSerializer
    
    @model_observer(Values)
    async def value_activity(self,
                             message: ValueSerializer,
                             observer: None,
                             subscribing_request_ids= [],
                             **kwargs):
        await self.send_json(message.data)

    @value_activity.serializer
    def value_activity(self,
                       instance: Values, action, **kwargs) -> ValueSerializer:
        return ValueSerializer(instance)
    

    #filtered observer response
    @value_activity.groups_for_signal
    def value_activity(self, instance: Values, **kwargs):
        yield instance.user_id
    
    @value_activity.groups_for_consumer
    def comment_activity(self, user, **kwargs):
        yield user
    
    #Action to be passed from json
    @action() 
    async def subscribe_to_value(self,
                                 user_pk,
                                 request_id, **kwargs):
        user = await database_sync_to_async(User.objects.get)(pk=user_pk)
        # status = await database_sync_to_async(Values.objects.get)(pk=user.id)
        print("{} subscribed to event changes".format(user))
        # print("{} is the current status".format(status))
        await self.value_activity.subscribe(
            user = user_pk,
            # status = status
        )
        status = await self.get_status(user)
        await self.send_json(
            {
                'baggage_status':status
            }
        )
        
    async def connect(self):
        # self.room_group_name = 'test'
        # await (self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name #Auto generated
        # )

        await self.accept()
        
        # await self.send(text_data=json.dumps({
        #     'type':'connection-response',
        #     'message':'connection accepted from host',
        # }))
        
        
    # async def receive(self,text_data):      
        
    #     await (self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type':'broadcast.message',
    #             'message':self.value
    #         }
    #     )
    
    # async def broadcast_message(self,event):
    #     message = event['message']
        
    #     await self.send(text_data = json.dumps({
    #         'type':'response',
    #         'message':message
    #     }))
    
    
    @database_sync_to_async
    def get_status(self,user):
        q_set = Values.objects.filter(user=user)
        status = (q_set.values('baggage_status').first()['baggage_status'])
        return status
        
        # status = await database_sync_to_async(value.baggage_status)

        
        
