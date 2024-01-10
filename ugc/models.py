from django.db import models
from django.contrib import admin



class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name = 'ID пользователя',
        unique = True,
    )
    name = models.TextField(
        verbose_name = 'Имя пользователя',
        unique = True,
    )

    def get_chat_id(update, context):
        chat_id = -1

        if update.message is not None:
    # from a text message
            chat_id = update.message.chat.id
        elif update.callback_query is not None:
    # from a callback message
            chat_id = update.callback_query.message.chat.id

        return chat_id
    
    def __str__(self):
        return f'#{self.external_id}{self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Message(models.Model):
    profile = models.ForeignKey(
        to = 'ugc.Profile',
        verbose_name = 'Профиль',
        on_delete = models.PROTECT,
    )
    text = models.TextField(
        verbose_name = 'Направление',
    )
    created_at = models.DateTimeField(
        verbose_name = 'Время получения',
        auto_now_add = True,
    )

    send = models.TextField(
        verbose_name = 'Рассылка',
    )

    def __str__(self):
        return f'Сообщение {self.pk}{self.profile}'
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

