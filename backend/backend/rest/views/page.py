from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from backend.rest.serializers.page import PageBasicSerializer, PageCreateSerializer, PageContentSerializer
from page.api.page import create, retrieve, update, _list, status, metrics


class PageAPI(ViewSet):
    serializer_class = PageBasicSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = PageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = create(**serializer.validated_data, token=request.GET.get('token'), email=request.GET.get('email'))
        return Response(page)

    def retrieve(self, request, pk):
        page = retrieve(request.GET.get('token'), email=request.GET.get('email'), pk=pk)
        return Response(page)

    def update(self, request, pk):
        page = update(request.GET.get('content'), request.GET.get('token'), request.GET.get('email'), pk)
        return Response(page)

    def list(self, request):
        page = _list(request.GET.get('token'), request.GET.get('email'))
        return Response(page)

    @action(detail=True, methods=['get'])
    def status(self, request, pk):
        page = status(request.GET.get('token'), operation_name=request.GET.get('operationName'), email=request.GET.get('email'), pk=pk)
        return Response(page)

    @action(detail=True, methods=['get'])
    def metrics(self, request, pk):
        page = metrics(request.GET.get('token'), email=request.GET.get('email'), pk=pk, zone=request.GET.get('region'))
        return Response(page)
