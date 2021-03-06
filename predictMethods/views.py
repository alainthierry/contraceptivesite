from django.shortcuts import render, get_object_or_404
from django.db import transaction, IntegrityError

from .forms import RegisterData, UserLogin, ParagraphErrorList
from .models import User, UserData

import numpy as np
import joblib

from django.utils.translation import gettext as _

from django.core.mail import send_mail
from django.conf import settings


def index(request):
    context = {
        'title': _('Predict Contraceptive Method Choice'),
        'page_title': _('Let\'s predict your Contraceptive Method Choice'),
    }
    return render(request, _('predictMethods/en/form.html'), context)

def user_login(request):
    context = {
        'title' : _('CMC login'),
        'page_title': _('Check Prediction')
    }
    if request.method == 'GET':
        form = UserLogin(request.GET or None)
        if form.is_valid():
            pseudonym = form.cleaned_data['pseudonym']
            user_age = form.cleaned_data['user_age']

            user_pseudo_exist = get_object_or_404(User, pseudonym=pseudonym)
            user_age_exist = UserData.objects.filter(user_age=user_age).filter(
                user=User.objects.get(pseudonym=user_pseudo_exist).id
            )
            if not (User.objects.filter(pseudonym=user_pseudo_exist).exists() and user_age_exist.exists()):
                context['message'] = _(" Sorry, you did not make any prediction before !")
                return render(request, _('predictMethods/en/login.html'), context)
            else:
                """ Everything is OK """

                context['found'] = True
                user = User.objects.filter(pseudonym=user_pseudo_exist).first()
                context['predict_result'] = user.predict_result
                context['predict_proba'] = user.predict_proba
                context['pseudonym'] = user.pseudonym
                context['title']  = pseudonym + _(" prediction")
                context['page_title'] = _("prediction of ")+pseudonym

                return render(request, _('predictMethods/en/login.html'), context)

    return render(request, _('predictMethods/en/login.html'), context)


def about_cmc(request):
    context = {
        'title': _('About CMC'),
        'page_title': _('About CMC'),
    }
    return render(request, _('predictMethods/en/about.html'), context)

def get_sent_data(request):
    context = {}
    if request.method == 'POST':
        form = RegisterData(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():

            """ Load the prediction model """
            rfcl_model = joblib.load('predictMethods/methodModels/finalized_model_rfcl.sav')

            user_age = int(form.cleaned_data['user_age'])
            pseudonym = form.cleaned_data['pseudonym']
            user_education = int("".join(form.cleaned_data['user_education']))
            husband_education = int("".join(form.cleaned_data['husband_education']))
            number_children_ever_born = int(form.cleaned_data['number_children_ever_born'])
            user_religion = int("".join(form.cleaned_data['user_religion']))
            user_working = int("".join(form.cleaned_data['user_working']))
            husband_occupation = int("".join(form.cleaned_data['husband_occupation']))

            new_user_data = np.array(
                [[user_age, user_education, husband_education,
                number_children_ever_born, user_religion, user_working, husband_occupation]]
            )
            """ Make prediction on data """
            context['predict_result'] = int(rfcl_model.predict(new_user_data))
            context['predict_proba'] = round( rfcl_model.predict_proba(new_user_data).max(), 3)
            context['page_title'] = _('Predicted method for ') + pseudonym
            context['pseudonym'] = pseudonym
            context['title'] = _("Predicted method for ") + pseudonym

            try:
                with transaction.atomic():
                    user = User.objects.filter(pseudonym=pseudonym)
                    if not user.exists():

                        user = User.objects.create(
                            pseudonym = pseudonym,
                            predict_result = context['predict_result'],
                            predict_proba = context['predict_proba'],
                        )
                        UserData.objects.create(
                            user_age = user_age,
                        	user_education = user_education,
                        	husband_education = husband_education,
                        	number_children_ever_born = number_children_ever_born,
                        	user_religion = user_religion,
                        	user_working = user_working,
                        	husband_occupation = husband_occupation,
                        	user = user,
                        )
                        """subject = 'A NEW PREDICTION HAS BEEN MADE !'
                        message = ""
                            This is to notify you that a new prediction has been made !
                            The project is continuing receiving new users !
                        ""
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = ['cobayeleamire@gmail.com',]
                        if send_mail( subject, message, email_from, recipient_list ):
                            return render(request, _('predictMethods/en/predict_result.html'), context)
                        else:"""
                        return render(request, _('predictMethods/en/predict_result.html'), context)
                    else:
                        """ The user exists in the database """
                        user = user.first()
                        user_data = UserData.objects.filter(user_age=user_age).only('user')

                        previous_predict = user.predict_result
                        previous_proba = user.predict_proba

                        if not user_data.exists():
                            """ New user_age value """

                            if (context['predict_result']==previous_predict) and (previous_proba > context['predict_proba']):
                                context['message'] = _("We're sorry, your data are still the same as the previous prediction you made on this website !")
                                context['predict_result'] = user.predict_result
                                context['predict_proba'] = user.predict_proba
                                context['page_title'] = _('Your new prediction is worse than your previous one !')
                                context['title'] = _('Prediction not allowed')
                                return render(request, _('predictMethods/en/predict_result.html'), context)

                            elif (context['predict_result']==previous_predict) and (previous_proba < context['predict_proba']):
                                """ Update proba and delete the previous data """

                                user.predict_proba  = context['predict_proba']
                                user_data = UserData.objects.get(user=user)
                                user_data.user_age = user_age
                                user_data.user_education = user_education
                                user_data.husband_education = husband_education
                                user_data.number_children_ever_born = number_children_ever_born
                                user_data.user_religion = user_religion
                                user_data.user_working = user_working
                                user_data.husband_occupation = husband_occupation

                                user.save()
                                user_data.save()
                                return render(request, _('predictMethods/en/predict_result.html'), context)
                            else:
                                if (context['predict_result'] !=previous_predict) and (previous_proba > context['predict_proba']):
                                    context['message'] = _("We're sorry, your data are still the same as the previous prediction you made on this website !")
                                    context['predict_result'] = user.predict_result
                                    context['predict_proba'] = user.predict_proba
                                    context['page_title'] = _('Your new prediction is worse than your previous one !')
                                    context['title'] = _('Prediction not allowed')
                                    return render(request, _('predictMethods/en/predict_result.html'), context)

                                elif (context['predict_result'] !=previous_predict) and (previous_proba < context['predict_proba']):
                                    """ Update proba and delete the previous data """

                                    user.predict_proba  = context['predict_proba']
                                    user.predict_result  = context['predict_result']
                                    user_data = UserData.objects.get(user=user)
                                    user_data.user_age = user_age
                                    user_data.user_education = user_education
                                    user_data.husband_education = husband_education
                                    user_data.number_children_ever_born = number_children_ever_born
                                    user_data.user_religion = user_religion
                                    user_data.user_working = user_working
                                    user_data.husband_occupation = husband_occupation

                                    user.save()
                                    user_data.save()
                                    return render(request, _('predictMethods/en/predict_result.html'), context)
                                else:
                                    context['message'] = _("We're sorry, your data are still the same as the previous prediction you made on this website.")
                                    context['predict_result'] = user.predict_result
                                    context['predict_proba'] = user.predict_proba
                                    context['title'] = _('Prediction not allowed')
                                    context['page_title'] = _('Your data did not change since your last prediction !')
                                    return render(request, _('predictMethods/en/predict_result.html'), context)
                        else:
                            """ No new prediction allowed, age did not change """

                            context['message'] = _(" We're sorry, your data are still the same as the previous prediction you made on this website.")
                            context['predict_result'] = user.predict_result
                            context['predict_proba'] = user.predict_proba
                            context['title'] = _('Prediction not allowed')
                            context['page_title'] = _('Your data did not change since your last prediction !')
                            return render(request, _('predictMethods/en/predict_result.html'), context)
            except IntegrityError:
                form.errors['internal'] = _(" An error occurred ! Thank you to try again later ! ")
        else:
            context = {}
            context['title'] = _('Predict Contraceptive Method')
            context['page_title'] = _('Let\'s predict your Contraceptive Method')
            return render(request, _('predictMethods/en/form.html'), context)
    else:
        pass
    return render(request, _('predictMethods/en/form.html'), context)
