from django.db import models

# Create your models here.


from cis498.mongodb.menu import Menu



class MenuModel(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=150)
	price = models.CharField(max_length=10)
	type = models.CharField(max_length=10)

	class Meta:
		verbose_name = "Item"
		verbose_name_plural = "Items"

	def __str__(self):
		return self.name


