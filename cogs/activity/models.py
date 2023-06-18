from django.db import models


class VoiceActivity(models.Model):
    user_id = models.BigIntegerField(null=False)
    guild_id = models.BigIntegerField(null=False)
    connect_time = models.DateTimeField(auto_now_add=True, null=False)
    disconnect_time = models.DateTimeField(null=True)
