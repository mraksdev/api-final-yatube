from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Model representing a post group/category.

    Groups allow organizing posts by topic. Each group has a unique
    slug used in URLs and a human-readable title.
    """

    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('Идентификатор', max_length=50)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    """Model representing a user post.

    Each post belongs to an author and may optionally be assigned
    to a group. Posts can contain text and an image.
    """

    text = models.TextField('Текст поста')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
        verbose_name='Автор')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True, verbose_name='Изображение')
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True,
        verbose_name='Группа')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    """Model representing a comment on a post.

    Comments are nested under posts. Each comment has an author
    and belongs to exactly one post.
    """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Пост')
    text = models.TextField('Текст комментария')
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    """Model representing a subscription from one user to another.

    A follow creates a one-directional subscription where `user`
    follows `following`. A unique constraint prevents duplicate
    follows and the API layer prevents self-follows.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
        verbose_name='Подписчик')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
        verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_user_following'
            )
        ]
