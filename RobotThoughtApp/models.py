from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Log(models.Model):
	description = models.TextField()
	reported = models.BooleanField()
	creation_time = models.DateTimeField(auto_now=True)

	def __str__ (self):
		return "{}, {}, {}, {}".format(self.id, self.description, self.reported, self.creation_time)
