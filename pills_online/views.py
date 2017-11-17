from django.contrib.auth.models import User, Group
from main.models import Medication
from rest_framework import viewsets
from pills_online.serializers import UserSerializer, GroupSerializer, MedicationSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all().filter(title__startswith='ГЕКСОРАЛ')
    serializer_class = MedicationSerializer

    def get_queryset(self):
        if self.request.query_params['q_type'] == 'all_drugs':
            return Medication.objects.all()
