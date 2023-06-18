from django.db import models


class WelcomeConfig(models.Model):
    guild_id = models.BigIntegerField(null=False, unique=True)
    channel_id = models.BigIntegerField(null=False)
    recruit_channel_id = models.BigIntegerField(null=False)
    grant_role_id = models.BigIntegerField(null=False)
    recruiter_role_id = models.BigIntegerField(null=False)
    message = models.TextField(null=False)
