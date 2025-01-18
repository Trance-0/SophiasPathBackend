from collections import Counter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
# from django.db.models.functions import Lower
# from django.db.models import CharField,TextField
from cluster.serializers import PageSerializer,SectionSerializer,RelationSerializer,TagSerializer
from cluster.models import DefinitionLink, Page,Section,Relation, SectionTypeChoices,Tag,PageTypeChoices,RelationTypeChoices
import logging

logger=logging.getLogger(__name__)

# register lower lookup for CharField: https://stackoverflow.com/questions/61482696/unsupported-lookup-lower-for-charfield-or-join-on-the-field-not-permitted
# CharField.register_lookup(Lower)
# TextField.register_lookup(Lower)

@api_view(['GET'])
def getSchools(request):
    # get all schools available on this website
    pages=Page.objects.filter(page_type=PageTypeChoices.SCHOOL)
    serializer=PageSerializer(pages,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSchoolBySlug(request,school_slug):
    # get a school page instance by slug
    try:
        school=Page.objects.get(Q(slug=school_slug) & Q(page_type=PageTypeChoices.SCHOOL))
        serializer=PageSerializer(school)
        return Response(serializer.data)
    except Page.DoesNotExist:
        return Response({"error":"School not found"},status=404)
    

@api_view(['GET'])
def getDevelopments(request):
    # get all relations of development available on this website
    developments=Relation.objects.filter(relation_type=RelationTypeChoices.DEVELOPMENT)
    serializer=RelationSerializer(developments,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getDevelopmentsBySchool(request,school_slug):
    # get all relations of development available on this website starting from a school
    try:
        school=Page.objects.get(Q(slug=school_slug) & Q(page_type=PageTypeChoices.SCHOOL))
        developments=Relation.objects.filter((Q(start_page_id=school)|Q(end_page_id=school)) & Q(relation_type=RelationTypeChoices.DEVELOPMENT))
        serializer=RelationSerializer(developments,many=True)
        return Response(serializer.data)
    except Page.DoesNotExist:
        return Response({"error":"School not found"},status=404)

@api_view(['GET'])
def getPhilosophersBySchool(request,school_slug):
    try:
        school=Page.objects.get(Q(slug=school_slug) & Q(page_type=PageTypeChoices.SCHOOL))
        logger.info(f"Getting philosophers by school {school.name}")
        affiliations=Relation.objects.filter(Q(end_page_id=school) & Q(relation_type=RelationTypeChoices.AFFILIATION))
        philosophers=[a.start_page_id for a in affiliations]
        serializer=PageSerializer(philosophers,many=True)
        return Response(serializer.data)
    except Page.DoesNotExist:
        return Response({"error":"School not found"},status=404)

@api_view(['GET'])
def getPage(request,page_slug):
    try:
        page=Page.objects.get(Q(slug=page_slug))
        serializer=PageSerializer(page)
        return Response(serializer.data)
    except Page.DoesNotExist:
        return Response({"error":"Page not found"},status=404)

@api_view(['GET'])
def getAffiliations(request,philosopher_slug):
    try:
        philosopher=Page.objects.get(Q(slug=philosopher_slug) & Q(page_type=PageTypeChoices.PHILOSOPHER))
        affiliations=Relation.objects.filter(Q(start_page_id=philosopher) & Q(relation_type=RelationTypeChoices.AFFILIATION))
        serializer=RelationSerializer(affiliations,many=True)
        return Response(serializer.data)
    except Page.DoesNotExist:
        return Response({"error":"Philosopher not found"},status=404)

@api_view(['GET'])
def getSections(request,page_slug):
    try:
        page=Page.objects.get(Q(slug=page_slug))
        sections=Section.objects.filter(Q(page_id=page)).order_by("order")
        serializer=SectionSerializer(sections,many=True)
        # assume the definition link size is small, we can iterate over all the links.
        # DO NOT DO THIS when definition link size is large, use add on create instead.
        definitions=DefinitionLink.objects.all()
        # render the definition links as dict of {term:url}
        definition_links={d.term:d.url() for d in definitions}
        # add definition links used in the page
        for section in serializer.data:
            # skip non-text sections
            if section["section_type"]!=SectionTypeChoices.TEXT: continue
            definition_links_in_section={}
            for word in section["text"].split():
                if word in definition_links:
                    definition_links_in_section[word]=definition_links[word]
            section["definition_links"]=definition_links_in_section
        return Response(serializer.data)
    except Page.DoesNotExist:
        return Response({"error":"Page not found"},status=404)

@api_view(['GET'])
def getRelations(request,philosopher_slug): 
    try:
        philosopher=Page.objects.get(Q(slug=philosopher_slug) & Q(page_type=PageTypeChoices.PHILOSOPHER))
        relations=Relation.objects.filter(Q(start_page_id=philosopher) | Q(end_page_id=philosopher))
        serializer=RelationSerializer(relations,many=True)
        return Response(serializer.data)
    except Page.DoesNotExist:
        return Response({"error":"Philosopher not found"},status=404)

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

@api_view(['GET'])
def search(request):    
    try:
        q=request.query_params.get("q")
        sort=request.query_params.get("sort","relevance")
        # set default page to 1
        page=request.query_params.get("page",1)
        page_number=int(page)
        # show 10 items per page
        page_size=10
        sections=[]
        if sort=="relevance":
            # TODO: use trigram similarity to search for relevance
            sections=Section.objects.filter(Q(subtitle__icontains=q) | Q(text__icontains=q))
            # sections=Section.objects.all()
        elif sort=="latest":
            sections=Section.objects.filter(Q(subtitle__icontains=q) | Q(text__icontains=q)).order_by("-last_edit")
        elif sort=="oldest":
            sections=Section.objects.filter(Q(subtitle__icontains=q) | Q(text__icontains=q)).order_by("last_edit")
        logger.info(f"Searching for keyword {q} with sort {sort}, result: {sections}")
        max_page_number=(len(sections)+page_size-1)//page_size
        if page_number>max_page_number or page_number<1:
            return Response({"error":f"Page number is out of range, should be between 1 and {max_page_number} total entries count is {len(sections)}"},status=400)
        serializer=SectionSerializer(sections[(page_number-1)*page_size:min(page_number*page_size,len(sections)+1)],many=True)
        # compose result
        final_result={}
        # page number starts from 1
        final_result["sections"]=serializer.data
        final_result["total_pages"]=max_page_number
        return Response(final_result)
    except Exception as e:
        return Response({"error":str(e)},status=404)

# @api_view(['POST'])
# def samplePost(request):
#     """
#     This is a sample post function but will not be used.
#     """
#     serializer=SectionSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)