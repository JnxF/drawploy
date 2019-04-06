from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from backend.rest.serializers.page import PageBasicSerializer, PageCreateSerializer, PageContentSerializer
from page.api.page import create, retrieve, update, _list


class PageAPI(ViewSet):
    serializer_class = PageBasicSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = PageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = create(**serializer.validated_data)
        # serializer = self.serializer_class(page, many=True)
        # return Response(serializer.data)
        return Response(page)

    def retrieve(self, _, pk):
        page = retrieve(pk)
        return Response(page)

    def update(self, request, pk):
        serializer = PageContentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = update(**serializer.validated_data, pk=pk)
        return Response(page)

    def list(self, _):
        page = _list()
        return Response(page)
