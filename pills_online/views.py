import os

from django.contrib.auth.models import User, Group
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Medication, Profile
from rest_framework import viewsets, status
from gensim.models import Word2Vec

from pills_online.permissions import RegistrationPermission, GetAuthPermission
from pills_online.serializers import UserSerializer, GroupSerializer, WarningsAnaloguesSerializer, MedicationSerializer, \
    UserProfileSerializer, MedicationIdSerializer
from pills_online.settings import PROJECT_ROOT


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
    """
    API endpoint for medication
    """
    # queryset = Medication.objects.all().filter(title__startswith='ГЕКСОРАЛ')
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer

    def get_queryset(self):
        """
        get all medications
        """
        return Medication.objects.all()
        # if self.request.query_params['q_type'] == 'all_drugs':
        #     return Medication.objects.all()
        # if self.request.query_params['q_type'] == 'my_drugs':
        #     user = User.objects.get(id=self.request.user.id)
        #     profile = user.profile
        #     return profile.medications.all()

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_user(self, request, pk=None):
        """
        add given medication to user list
        :param pk: id of medication
        :return: response
        """
        medication = Medication.objects.get(id=pk)
        user = User.objects.get(id=self.request.user.id)
        profile = user.profile
        profile.medications.add(medication)

        return Response(
            {"message": "Medication is added"},
            status=status.HTTP_200_OK
        )

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def delete_from_user(self, request, pk=None):
        """
        delete given medication from user list
        :param pk: id of medication
        :return: response
        """
        user = User.objects.get(id=self.request.user.id)
        profile = user.profile
        medication = profile.medications.get(id=pk)
        profile.medications.remove(medication)

        return Response(
            {"message": "Medication is deleted"},
            status=status.HTTP_200_OK
        )

    @detail_route(methods=['get'], permission_classes=[IsAuthenticated])
    def analogues(self, request, pk=None):
        """
        :param pk: id of medication
        :return: list of analogues
        """
        analogues = Medication.objects.get(id=pk).analogues
        serializer = self.get_serializer(analogues, many=True)

        return Response(serializer.data)

    @list_route(methods=['get'], permission_classes=[IsAuthenticated])
    def my(self, request):
        """
        :return: list of medications of current user
        """
        user = User.objects.get(id=request.user.id)
        profile = user.profile
        medications = profile.medications.all()
        serializer = self.get_serializer(medications, many=True)

        return Response(serializer.data)

    @detail_route(methods=['get'], permission_classes=[IsAuthenticated])
    def is_contra(self, request, pk=None):
        """
        :param pk: id of medication
        :return: is there is possible contraindication for user
        """
        medication = Medication.objects.get(id=pk)
        user = User.objects.get(id=request.user.id)
        profile = user.profile
        print(profile.id)
        return Response(medication.check_contradiction(profile.allergy))


class WarningsViewSet(viewsets.ModelViewSet):
    permission_classes = (GetAuthPermission,)
    serializer_class = WarningsAnaloguesSerializer

    def get_queryset(self):
        """
        return list of warnings for medication
        """
        queryset = Medication.objects.all().filter(id=self.request.query_params['id'])
        return queryset


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for retrieval and modification of user profile info
    """
    serializer_class = UserProfileSerializer

    @list_route(methods=['get'], permission_classes=[GetAuthPermission])
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        profile = user.profile
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @list_route(methods=['post'], permission_classes=[IsAuthenticated])
    def post(self, request):
        user = User.objects.get(id=request.user.id)
        profile = user.profile
        profile.allergy = request.data['allergy']
        profile.gender = request.data['gender']
        profile.weight = request.data['weight']
        profile.birthday = request.data['birthday']
        profile.save()
        return Response({"message": "Profile is edited"},
                        status=status.HTTP_200_OK)


class SearchEngine(viewsets.ModelViewSet):
    """
    API endpoint for search of medication
    """
    permission_classes = (GetAuthPermission,)
    serializer_class = MedicationIdSerializer

    file_ = os.path.join(PROJECT_ROOT, '../static/word2vec/w2vmodel.w2v')
    w2v_model = Word2Vec.load(file_)

    def get_queryset(self):

        query = self.request.query_params['query']

        tokens = query.split()
        query = ""
        for token in tokens:
            query += token + ' '
            if token not in self.w2v_model.wv.vocab:
                continue
            similar = self.w2v_model.most_similar(token)
            for sim_word in similar:
                if sim_word[1] > 0.85:
                    query += sim_word[0] + ' '
                break

        print("QUERY:", query)

        body_vector = SearchVector('title', 'indication', 'pharm_action', config='russian')
        term_query = SearchQuery(query, config='russian')  # & SearchQuery('орви')
        # res = Medication.objects.annotate(search=SearchVector('indication', 'contra')).filter(search='не')
        queryset = Medication.objects.annotate(rank=SearchRank(body_vector, term_query)).order_by('-rank')
        return queryset[:10]
