from django.db import models

class User(models.Model):
	"""docstring for User"""

	class UserContraceptiveMethod(models.IntegerChoices):
		"""docstring for UserContraceptiveMethod"""
		NO_USE = 1
		LONG_TERM = 2
		SHORT_TERM = 3

	""" unique pseudonym """
	pseudonym = models.CharField(max_length = 20, unique=True)
	predict_result = models.PositiveSmallIntegerField(choices = UserContraceptiveMethod.choices)
	predict_date = models.DateField(auto_now_add = True)
	predict_proba = models.FloatField(default=0)

	def __str__(self):
		return self.pseudonym

class UserData(models.Model):
	"""docstring for UserData
	"""
	class UserEducation(models.IntegerChoices):
		"""docstring for UserEducation"""
		LOW = 1
		MEDIUM = 2
		HIGH = 3
		VERY_HIGH = 4

	class UserReligion(models.IntegerChoices):
		"""docstring for UserReligion"""
		NONE_ISLAM = 0
		ISLAM = 1

	class UserNowWorking(models.IntegerChoices):
		"""docstring for UserNowWorking"""
		YES = 0
		NO = 1

	user_age = models.PositiveSmallIntegerField()
	user_education = models.PositiveSmallIntegerField(choices = UserEducation.choices)
	husband_education = models.PositiveSmallIntegerField(choices = UserEducation.choices)
	number_children_ever_born = models.PositiveSmallIntegerField()
	user_religion = models.PositiveSmallIntegerField(choices = UserReligion.choices)
	user_working = models.PositiveSmallIntegerField(choices = UserNowWorking.choices)
	husband_occupation = models.PositiveSmallIntegerField(choices = UserEducation.choices)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
