from datetime import datetime

from django.db import models


class VoiceActivity(models.Model):
    user_id = models.BigIntegerField(null=False)
    guild_id = models.BigIntegerField(null=False)
    connect_time = models.DateTimeField(default=datetime.utcnow, null=False)
    disconnect_time = models.DateTimeField(null=True)
