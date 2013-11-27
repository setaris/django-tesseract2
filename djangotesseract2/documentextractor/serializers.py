from rest_framework import serializers


class DocumentSerializer(serializers.Serializer):
    fileid = serializers.CharField(max_length=50)
