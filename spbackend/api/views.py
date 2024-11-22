from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from cluster.serializers import PageSerializer,SectionSerializer,RelationSerializer,TagSerializer
from cluster.models import Page,Section,Relation,Tag,PageTypeChoices,RelationTypeChoices

@api_view(['GET'])
def getSchools(request):
    # get all schools available on this website
    pages=Page.objects.filter(page_type=PageTypeChoices.SCHOOL)
    serializer=PageSerializer(pages,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSchoolBySlug(request,school_slug):
    # get a school page instance by slug
    school=Page.objects.get(Q(slug=school_slug) & Q(page_type=PageTypeChoices.SCHOOL))
    serializer=PageSerializer(school)
    return Response(serializer.data)

@api_view(['GET'])
def getDevelopments(request):
    # get all relations of development available on this website
    developments=Relation.objects.filter(relation_type=RelationTypeChoices.DEVELOPMENT)
    serializer=RelationSerializer(developments,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getDevelopmentsBySchool(request,school_slug):
    # get all relations of development available on this website starting from a school
    school=Page.objects.get(Q(slug=school_slug) & Q(page_type=PageTypeChoices.SCHOOL))
    developments=Relation.objects.filter((Q(start_page_id=school)|Q(end_page_id=school)) & Q(relation_type=RelationTypeChoices.DEVELOPMENT))
    serializer=RelationSerializer(developments,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPhilosophersBySchool(request,school_slug):
    school=Page.objects.get(slug=school_slug)
    affiliations=Relation.objects.filter(Q(start_page_id=school) & Q(relation_type=RelationTypeChoices.AFFILIATION))
    philosophers=[a.end_page_id for a in affiliations]
    serializer=PageSerializer(philosophers,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPhilosopher(request,philosopher_slug):
    philosopher=Page.objects.get(Q(slug=philosopher_slug) & Q(page_type=PageTypeChoices.PHILOSOPHER))
    serializer=PageSerializer(philosopher)
    return Response(serializer.data)

@api_view(['GET'])
def getAffiliations(request,philosopher_slug):
    philosopher=Page.objects.get(Q(slug=philosopher_slug) & Q(page_type=PageTypeChoices.PHILOSOPHER))
    affiliations=Relation.objects.filter(Q(start_page_id=philosopher) & Q(relation_type=RelationTypeChoices.AFFILIATION))
    serializer=RelationSerializer(affiliations,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSectionsByPhilosopher(request,philosopher_slug):
    philosopher=Page.objects.get(Q(slug=philosopher_slug) & Q(page_type=PageTypeChoices.PHILOSOPHER))
    sections=Section.objects.filter(Q(page_id=philosopher)).order_by("order")
    serializer=SectionSerializer(sections,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRelations(request,philosopher_slug):
    philosopher=Page.objects.get(Q(slug=philosopher_slug) & Q(page_type=PageTypeChoices.PHILOSOPHER))
    relations=Relation.objects.filter(Q(start_page_id=philosopher) | Q(end_page_id=philosopher))
    serializer=RelationSerializer(relations,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTags(request):
    tags=Tag.objects.distinct("name")
    serializer=TagSerializer(tags,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSectionsByTag(request,tag_slug):
    sections=[s.section_id for s in Tag.objects.filter(slug=tag_slug)]
    serializer=SectionSerializer(sections,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def samplePost(request):
    """
    This is a sample post function but will not be used.
    """
    serializer=SectionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)