from django.contrib.auth.models import User, Group
from main.models import Medication, Profile
from rest_framework import viewsets

from pills_online.permissions import RegistrationPermission, GetAuthPermission
from pills_online.serializers import UserSerializer, GroupSerializer, MedicationSerializer, WarningsAnaloguesSerializer
from rest_framework.response import Response


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
    # queryset = Medication.objects.all().filter(title__startswith='ГЕКСОРАЛ')
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer

    def get_queryset(self):
        if self.request.query_params['q_type'] == 'all_drugs':
            return Medication.objects.all()
        if self.request.query_params['q_type'] == 'my_drugs':
            user = User.objects.filter(id=self.request.user.id).first()
            profile = user.profile
            return profile.medications.all()


class WarningsAnaloguesViewSet(viewsets.ModelViewSet):
    permission_classes = (GetAuthPermission,)
    serializer_class = WarningsAnaloguesSerializer
    queryset = Medication.objects.all()

    def get_queryset(self):
        query_set = Medication.objects.all().filter(id=self.request.query_params['id'])
        return query_set
