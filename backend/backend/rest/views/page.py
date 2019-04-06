from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from backend.rest.serializers.page import PageBasicSerializer, PageCreateSerializer
from page.api.page import create


class PageAPI(ViewSet):
    serializer_class = PageBasicSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = PageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = create(**serializer.validated_data)
        serializer = self.serializer_class(page, many=True)
        return Response(serializer.data)
