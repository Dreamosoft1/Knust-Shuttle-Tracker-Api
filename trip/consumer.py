from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from authentication.models import User
from .models import Trip_Request, Driver

class TripConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Check if the user is logged in
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            await self.accept()
            # Add the user to the drivers group
            if isinstance(self.scope["user"], Driver):
                async_to_sync(self.channel_layer.group_add)("drivers", self.channel_name)

    async def disconnect(self, close_code):
        # Remove the user from the drivers group
        if isinstance(self.scope["user"], Driver):
            async_to_sync(self.channel_layer.group_discard)("drivers", self.channel_name)
        self.close()

    async def receive(self, text_data):
        trip_request_id = int(text_data)
        await self.join_trip_request(trip_request_id)

    @database_sync_to_async
    def join_trip_request(self, trip_request_id):
        trip_request = Trip_Request.objects.get(id=trip_request_id)
        user = self.scope["user"]
        trip_request.joined_users.add(user)
        #Count Users in trip and reset trip
        requests = trip_request.joined_users.all().count()
        if requests == 4:
            trip_request.joined_users.clear()
            trip_request.status = 2
            trip_request.save()
            self.send_notification_to_drivers(trip_request_id)
            return trip_request
        
        return trip_request

    @database_sync_to_async
    def send_notification_to_drivers(self, trip_request_id):
        trip_request = Trip_Request.objects.get(id=trip_request_id)
        drivers = Driver.objects.filter(vehicle__stop__name=trip_request.start_point, vehicle__stop__name=trip_request.end_point)
        # Send a message to all drivers
        async_to_sync(get_channel_layer().group_send)(
            "drivers",
            {
                "type": "trip.request",
                "trip_request_id": trip_request_id,
            },
        )