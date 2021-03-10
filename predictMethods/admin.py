from django.contrib import admin
from .models import (User, UserData)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("pseudonym", "predict_result", "predict_proba", "predict_date")
    list_filter = ("predict_date", )


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
	"""docstring for UserDataAdmin"""

	list_display = (
		"user_age", "user_education", "husband_education", "number_children_ever_born",
		"user_religion", "user_working", "husband_occupation", "user",
	)
	list_filter = ("user_age", "user_religion", )

