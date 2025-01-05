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
        # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    image_path = image_path
    image = Image.open(image_path)
    input_tensor = preprocess(image).unsqueeze(0)  # Add batch dimension

    with torch.no_grad():
        output = model(input_tensor)

    probability = F.softmax(output, dim=1)

    confidence, predicted = torch.max(probability, 1)

    print(confidence)

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
            filename = fs.save(uploaded_image.name, uploaded_image)  # Save the file
            file_path = fs.path(filename)

            image_prediction = make_prediction(file_path)

            if image_prediction is not None:
                request.session['prediction'] = f'The rims in the picture you provided should be {image_prediction}'
            else:
                request.session['prediction'] = "The model couldn't recognize the rims from the picture"

        return redirect('home page')
