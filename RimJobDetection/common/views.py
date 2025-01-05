from django.shortcuts import render
from RimJobDetection.common.forms import UserUploadedPictureForm


def home_page(request):
    picture_upload_form = UserUploadedPictureForm()
    prediction_result = None

    if 'prediction' in request.session:
        prediction_result = request.session['prediction']

    context = {
        'prediction_result': prediction_result,
        'picture_form': picture_upload_form,
        "user_is_auth": request.user.is_authenticated
    }

    return render(request, 'common_templates/main_page.html', context)
