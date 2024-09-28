from rest_framework.response import Response
from rest_framework.decorators import api_view
from cluster.serializers import SchoolSerializer,DevelopmentSerializer,PhilosopherSerializer,SectionSerializer,RelationSerializer,AffiliationSerializer,TagSerializer
from cluster.models import School,Development,Philosopher,Section,Relation,Affiliation,Tag

@api_view(['GET'])
def getSchools(request):
    categories=School.objects.all()
    serializer=SchoolSerializer(categories,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getDevelopments(request):
    developments=Development.objects.all()
    serializer=DevelopmentSerializer(developments,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPhilosophersBySchool(request,school_pk):
    philosophers=Philosopher.objects.filter(school_id=school_pk)
    serializer=PhilosopherSerializer(philosophers,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAffiliations(request,philosopher_pk):
    affiliations=Affiliation.objects.filter(start_philosopher_id=philosopher_pk)
    serializer=AffiliationSerializer(affiliations,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSectionsByPhilosopher(request,philosopher_pk):
    sections=Section.objects.filter(philosopher_id=philosopher_pk)
    serializer=SectionSerializer(sections,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRelations(request,philosopher_pk):
    relations=Relation.objects.filter(start_philosopher_id=philosopher_pk)
    serializer=RelationSerializer(relations,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTags(request):
    tags=Tag.objects.order_by().values('name').distinct()
    serializer=TagSerializer(tags,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSectionsByTag(request,tag_pk):
    sections=Tag.objects.filter(id=tag_pk).section_id
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