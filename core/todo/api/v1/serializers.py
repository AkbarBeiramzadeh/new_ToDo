from rest_framework import serializers
from ...models import Task
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


class TaskSerializer(serializers.ModelSerializer):
    relative_url = serializers.URLField(source='get_relative_api_url', read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_abs_url")

    class Meta:
        model = Task
        fields = ('id', 'user', 'title', 'state', 'created_at', 'updated_at', 'relative_url', 'absolute_url')
        read_only_fields = ('user',)

    def get_abs_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('relative_url', None)
            rep.pop('absolute_url', None)
            
        rep["user"] = UserSerializer(instance.user, context={'request': request}).data
        return rep

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)
