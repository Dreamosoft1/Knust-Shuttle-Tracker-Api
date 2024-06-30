from rest_framework import generics
from .models import Feedback
from .serializers import FeedbackSerializer

# Create your views here.
class FeedbackListCreate(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class FeedbackList(generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer