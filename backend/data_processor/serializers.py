from rest_framework import serializers

class DataTypeSerializer(serializers.Serializer):
    column = serializers.CharField()
    data_type = serializers.CharField()

class DataPreviewSerializer(serializers.Serializer):
    data = serializers.ListField()
    columns = serializers.ListField()
    dtypes = serializers.DictField()