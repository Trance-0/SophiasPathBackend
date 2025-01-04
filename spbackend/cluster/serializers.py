"""
This defines serializer for all objects in cluster
"""

from rest_framework import serializers
from .models import Page,Section,Relation,Tag

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = '__all__'

    def get_url(self, obj):
        return f"{obj.page_id.slug}#{obj.slug}"

class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
    