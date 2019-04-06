from rest_framework import serializers as s


class PageBasicSerializer(s.Serializer):
    content = s.CharField()


class PageCreateSerializer(s.Serializer):
    image = s.CharField()
