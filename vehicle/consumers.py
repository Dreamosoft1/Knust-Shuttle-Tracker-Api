import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from .models import Driver

class VehicleLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        driver_id = data['driver_id']
        lat = data['lat']
        long = data['long']

        # Update the driver's location and wait for the result
        driver = await self.update_driver_location(driver_id, lat, long)

        # Broadcast the updated location to all connected clients
        await self.send(text_data=json.dumps({'driver_id': driver.id, 'lat': driver.latitude, 'long': driver.longitude}))

    @sync_to_async
    def update_driver_location(self, driver_id, lat, long):
        try:
            driver = Driver.objects.get(id=driver_id)
            driver.latitude = lat
            driver.longitude = long
            driver.save()
            return driver
        except Driver.DoesNotExist:
            return Driver.objects.create(id=driver_id, latitude=lat, longitude=long)
