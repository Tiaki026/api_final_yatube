from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint

User = get_user_model()


class Group(models.Model):
    """Класс группы."""

    title = models. CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:

        verbose_name = 'Создать новую группу'
        verbose_name_plural = 'Создать новую группу'

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    """Класс поста."""

    text = models.TextField(
        verbose_name='Текст',
        help_text='О чём Вы сейчас думаете?'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Выберете группу, к которой относится Ваша заметка'
    )

    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        null=True,
        blank=True
    )

    class Meta:

        verbose_name = 'Создать новую заметку'
        verbose_name_plural = 'Создать новую заметку'

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    """Класс комметария."""

    text = models.TextField(
        verbose_name='Комментарий',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
        related_name='comments',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время',
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text


class Follow(models.Model):
    """Класс подписок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower',
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Вы подписаны',
        related_name='following',
    )

    class Meta:
        verbose_name = 'Подписаться'
        verbose_name_plural = 'Подписки',

        constraints = [
            UniqueConstraint(
                name='unique_follow',
                fields=['user', 'following'],
            )
        ]

    def __str__(self) -> str:
        return f'{self.user.username} -> {self.following.username}'

    def clean(self) -> None:
        super().clean()
        if self.user == self.author:
            raise ValidationError('Нельзя подписаться на самого себя')
