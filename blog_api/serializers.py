from rest_framework import serializers
from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'autor',
            'title',
            'body',
            'created',
            'status',
            'slug',
        )
        model = Post