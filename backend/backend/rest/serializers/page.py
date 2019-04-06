from rest_framework import serializers as s


class ContentBasic(s.Serializer):
    html = s.CharField(read_only=True)


class PageBasicSerializer(s.Serializer):
    content = s.ListField(child=ContentBasic(), read_only=True)


class PageCreateSerializer(s.Serializer):
    image = s.CharField()
