from django.contrib.auth.models import User, Group
from main.models import Medication
from rest_framework import viewsets

from pills_online.permissions import RegistrationPermission, GetAuthPermission
from pills_online.serializers import UserSerializer, GroupSerializer, MedicationSerializer, WarningsAnaloguesSerializer

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
    #queryset = Medication.objects.all().filter(title__startswith='ГЕКСОРАЛ')
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    """
    def get_queryset(self):
        if self.request.query_params['q_type'] == 'all_drugs':
            return Medication.objects.all()
            #return Medication.objects.all().filter(id=self.request.user.id+3800)
    """

class WarningsAnaloguesViewSet(viewsets.ModelViewSet):
    permission_classes = (GetAuthPermission,)
    serializer_class = WarningsAnaloguesSerializer
    def get_queryset(self):
        query_set = Medication.objects.all().filter(id=self.request.query_params['id'])
        return query_set