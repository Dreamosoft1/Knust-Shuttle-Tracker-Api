from rest_framework import serializers
<<<<<<< HEAD:trip/serializers.py
from .models import Trip_Request

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip_Request
        fields = '__all__'
=======
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
>>>>>>> 381be816367d2a36a15ed0efb0d9021e109608ee:feedback/serializers.py
