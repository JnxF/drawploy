from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from backend.rest.serializers.page import PageBasicSerializer, PageCreateSerializer, PageContentSerializer
from page.api.page import create, retrieve, update, _list, deploy


class PageAPI(ViewSet):
    serializer_class = PageBasicSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = PageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = create(**serializer.validated_data, token=request.GET.get('token'))
        return Response(page)

    def retrieve(self, request, pk):
        page = retrieve(request.GET.get('token'), pk=pk)
        return Response(page)

    def update(self, request, pk):
        serializer = PageContentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = update(**serializer.validated_data, token=request.GET.get('token'), pk=pk)
        return Response(page)

    def list(self, request):
        page = _list(request.GET.get('token'))
        return Response(page)

    @action(detail=True, methods=['post'])
    def deploy(self, request, pk):
        page = deploy(request.GET.get('token'), pk=pk)
        return Response(page)
