"""
This defines serializer for all objects in cluster
"""

from rest_framework import serializers
from .models import School,Development,Philosopher,Section,Relation,Affiliation,Tag

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

class DevelopmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Development
        fields = '__all__'

class PhilosopherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Philosopher
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = '__all__'

class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
    