from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для публикаций пользователей."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'image', 'pub_date', 'group')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев к публикациям."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created')
        read_only_fields = ('post', 'author', 'created')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для сообществ публикаций."""

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок на пользователей."""
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    def validate_following(self, value):
        request = self.context.get('request')
        if not request:
            return value
            
        current_user = request.user
        if value == current_user:
            raise serializers.ValidationError(
                'Подписка на собственный аккаунт невозможна'
            )
            
        existing_follow = Follow.objects.filter(
            user=current_user, 
            following=value
        ).exists()
        
        if existing_follow:
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя'
            )
            
        return value

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]
