# Authors: Hyunwoo Lee <hyunwoo9301@naver.com>
# Released under the MIT license.

from django.db import models

class MessageModel(models.Model):
    text = models.CharField(max_length=1024)