from django import forms
from django.forms.utils import ErrorList

from .models import UserData

USER_EDUCATION = (
	(1, "LOW"),
    (2, "MEDIUM"),
    (3, "HIGH"),
    (4, "VERY_HIGH"),
)
USER_OCCUPATION = (
	(1, "LOW"),
    (2, "MEDIUM"),
    (3, "HIGH"),
    (4, "VERY_HIGH"),
)
USER_RELIGION = (
	(0, "NONE_ISLAM"),
    (1, "ISLAM"),
)
USER_NOW_WORKING = (
	(0, "YES"),
    (1, "NO"),
)
class RegisterData(forms.Form):
	"""docstring for RegisterData"""

	pseudonym = forms.CharField(required=True, max_length=20)
	user_age = forms.IntegerField(required=True, min_value=16)
	user_education = forms.MultipleChoiceField(required=True,choices=USER_EDUCATION)
	husband_education = forms.MultipleChoiceField(required=True, choices = USER_EDUCATION)
	number_children_ever_born = forms.IntegerField(required=True, min_value=0, max_value=36)
	user_religion = forms.MultipleChoiceField(required=True, choices = USER_RELIGION)
	user_working = forms.MultipleChoiceField(required=True, choices = USER_NOW_WORKING)
	husband_occupation = forms.MultipleChoiceField(required=True, choices = USER_OCCUPATION)

class UserLogin(forms.Form):
	"""docstring for UserLogin."""

	pseudonym = forms.CharField(
		required=True,
		max_length=20,
	)
	user_age = forms.IntegerField(
		required=True,
		min_value=16,
		max_value=100,
	)

class ParagraphErrorList(ErrorList):
	"""docstring for ParagraphErrorList"""
	def __str__(self):
		return self.as_divs()

	def as_divs(self):
		if not self: return ''
		return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])
