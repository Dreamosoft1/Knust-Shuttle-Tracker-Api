from rest_framework.views import APIView
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class TripRequestView(APIView):
    def post(self, request):
        # Process the trip request
        # ...

        # Send a WebSocket notification to update the trip status
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'trip_updates',  # Group name for trip updates
            {
                'type': 'trip_update',
                'message': 'New trip request received',
                'data': {
                    # Additional data to send with the notification
                    # ...
                }
            }
        )

        return Response({'message': 'Trip request submitted'})
