from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    title = serializers.CharField()
    authors = serializers.ListField(child=serializers.CharField())
    publisher = serializers.CharField(allow_blank=True, required=False)
    publish_date = serializers.CharField(allow_blank=True, required=False)
    isbn = serializers.CharField()