from django.contrib.auth.models import User, Group
from main.models import Medication, Profile
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])

        profile = Profile.objects.create(
            user=user
        )

        user.save()
        profile.save()

        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class MedicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Medication
        fields = ('id',
                  'title',
                  'pharm_action',
                  'pharm_kinetic',
                  'indication',
                  'contra',
                  'dosage',
                  'side_effect',
                  'med_interact',
                  'spec_instruct',
                  'pregnancy',
                  'kidney',
                  'liver',
                  'clinic_pharm_group',
                  'form_composition',
                  'overdosage',
                  'child_policy',
                  'old_policy',
                  'distr_policy',
                  'expiration_date',
                  'img_path'
                  )


class WarningsAnaloguesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Medication
        fields = ('id', 'warn_pregnancy', 'warn_kidney', 'warn_liver')


class UsersMedicationProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', '')
