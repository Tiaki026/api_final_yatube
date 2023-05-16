from rest_framework import serializers
from posts.models import Post, Group, Comment, Follow, User
from rest_framework.validators import UniqueTogetherValidator


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор поста."""

    author = serializers.StringRelatedField()

    class Meta:

        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор группы."""

    class Meta:

        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментария."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:

        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ['post']


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    user = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault()
    )

    following = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username')

    class Meta:

        model = Follow
        fields = ('id', 'user', 'following')
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны.'
            ),
        )

    def validate(self, data) -> any:
        if self.context.get('request').user == data.get('following'):
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return data
