from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from torch import nn
from torchvision import transforms, models
from PIL import Image
from torchvision.models import ResNet50_Weights
import pandas as pd
import torch
import torch.nn.functional as F
from RimJobDetection.common.forms import UserUploadedPictureForm
from RimJobDetection.predictions.models import UserSearchHistory


def get_label(index):
    annotation_csv_file = pd.read_csv(
        '/Users/dimitarmladenov/RimJobDetection/RimJobDetection/predictions/CnnModel/labels/labels.csv'
    )
    label = annotation_csv_file.iloc[index, 1]

    return label


def get_num_labels():
    csv_file = pd.read_csv(
        '/Users/dimitarmladenov/RimJobDetection/RimJobDetection/predictions/CnnModel/labels/labels.csv'
    )
    return len(csv_file)


def make_prediction(image_path):
    model = models.resnet50(weights=ResNet50_Weights.DEFAULT)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 53)
    model.load_state_dict(torch.load(
        '/Users/dimitarmladenov/RimJobDetection/RimJobDetection/predictions/CnnModel/model_1.pth'
    ))
    model.eval()

    preprocess = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
    ])

    image_path = image_path
    image = Image.open(image_path)
    input_tensor = preprocess(image).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)

    probability = F.softmax(output, dim=1)

    confidence, predicted = torch.max(probability, 1)

    if confidence > 0.75:
        return get_label(int(predicted))
    else:
        return None


def prediction(request):
    if request.method == 'POST':

        uploaded_image_form = UserUploadedPictureForm(request.POST, request.FILES)
        if uploaded_image_form.is_valid():
            uploaded_image = uploaded_image_form.cleaned_data['image']

            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(uploaded_image.name, uploaded_image)
            file_path = fs.path(filename)

            image_prediction = make_prediction(file_path)

            image_hash = UserSearchHistory.calculate_image_hash(uploaded_image)
            image_exists = UserSearchHistory.objects.filter(user=request.user, image_hash=image_hash)

            if image_exists:
                get_saved_prediction = image_exists.get().model_prediction
                request.session['prediction'] = f'The rims in the picture you provided should be {get_saved_prediction}'
            elif not image_exists:
                if image_prediction is not None:
                    UserSearchHistory.objects.create(user=request.user,
                                                     image=uploaded_image,
                                                     model_prediction=image_prediction,
                                                     image_hash=image_hash
                                                     )
                    request.session['prediction'] = f'The rims in the picture you provided should be {image_prediction}'
                else:
                    request.session['prediction'] = "The model couldn't recognize the rims from the picture"

        return redirect('home page')
