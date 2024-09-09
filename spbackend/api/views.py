from rest_framework.response import Response
from rest_framework.decorators import api_view
from cluster.serializers import SectionSerializer,TagSerializer,PageSerializer,CategorySerializer,RelationSerializer,DevelopmentSerializer
from cluster.models import Category,Development,Page,Section,Relation,Tag

@api_view(['GET'])
def getCategories(request):
    categories=Category.objects.all()
    serializer=CategorySerializer(categories,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getDevelopments(request):
    developments=Development.objects.all()
    serializer=CategorySerializer(developments,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPageByCategory(request,cate_pk):
    pages=Page.objects.filter(category_id=cate_pk)
    serializer=PageSerializer(pages,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSectionByPage(request,page_pk):
    sections=Section.objects.filter(page_id=page_pk)
    serializer=SectionSerializer(sections,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRelations(request):
    relations=Relation.objects.all()
    serializer=RelationSerializer(relations,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTags(request):
    tags=Tag.objects.all()
    serializer=TagSerializer(tags,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSectionByTag(request,tag_pk):
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