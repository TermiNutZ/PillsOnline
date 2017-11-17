from django.contrib.auth.models import User, Group

from main.models import Medication
from rest_framework import viewsets

from pills_online.permissions import RegistrationPermission
from pills_online.serializers import UserSerializer, GroupSerializer, MedicationSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (RegistrationPermission,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
