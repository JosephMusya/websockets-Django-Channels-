from django.shortcuts import render

from .serializers import ValueSerializer
from .models import Values
from rest_framework import generics

# Create your views here.
def index(request):
    return render(request,'index.html')

class MySocket(generics.ListCreateAPIView,):
    queryset = Values.objects.all()
    serializer_class = ValueSerializer
    
    