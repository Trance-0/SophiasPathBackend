from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from cluster.serializers import SchoolSerializer,DevelopmentSerializer,PhilosopherSerializer,SectionSerializer,RelationSerializer,AffiliationSerializer,TagSerializer
from cluster.models import School,Development,Philosopher,Section,Relation,Affiliation,Tag

@api_view(['GET'])
def getSchools(request):
    categories=School.objects.all()
    serializer=SchoolSerializer(categories,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSchoolBySlug(request,school_slug):
    school=School.objects.get(slug=school_slug)
    serializer=SchoolSerializer(school)
    return Response(serializer.data)

@api_view(['GET'])
def getDevelopments(request):
    developments=Development.objects.all()
    serializer=DevelopmentSerializer(developments,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getDevelopmentsBySchool(request,school_slug):
    developments=Development.objects.filter(Q(start_school_id__slug=school_slug)|Q(end_school_id__slug=school_slug))
    serializer=DevelopmentSerializer(developments,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPhilosophersBySchool(request,school_slug):
    philosophers=Philosopher.objects.filter(school_slug=school_slug)
    serializer=PhilosopherSerializer(philosophers,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPhilosopher(request,philosopher_slug):
    philosopher=Philosopher.objects.get(slug=philosopher_slug)
    serializer=PhilosopherSerializer(philosopher)
    return Response(serializer.data)

@api_view(['GET'])
def getAffiliations(request,philosopher_slug):
    affiliations=Affiliation.objects.filter(start_philosopher_id__slug=philosopher_slug)
    serializer=AffiliationSerializer(affiliations,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSectionsByPhilosopher(request,philosopher_slug):
    sections=Section.objects.filter(philosopher_id__slug=philosopher_slug).order_by("pk")
    serializer=SectionSerializer(sections,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRelations(request,philosopher_slug):
    relations=Relation.objects.filter(start_philosopher_id__slug=philosopher_slug)
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