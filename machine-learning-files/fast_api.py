from fastapi import FastAPI, HTTPException
from PIL import Image
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
import os
import time
import torch
import torchvision.models as models
import torchvision.transforms as transforms
import uvicorn

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

#All Classes
all_classes = [
  "battery",
  "biological",
  "cardboard",
  "glass",
  "metal",
  "paper",
  "plastic"
]

#Pytorch Model Loading
pytorch_model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# Freeze all layers
for param in pytorch_model.parameters():
  param.requiresGrad = False

# Replace the last fully connected layer with a new one
num_ftrs = pytorch_model.fc.in_features
pytorch_model.fc = torch.nn.Linear(num_ftrs, 7)

pytorch_model.load_state_dict(torch.load('resnet_18.pt', map_location=torch.device('cpu')), strict=False)
pytorch_model.eval()

#Image Transformations
image_transformations = transforms.Compose([
  transforms.Resize((256, 256)),
  transforms.ToTensor()
])

#Fast API App Instance
fast_api_app = FastAPI()

@fast_api_app.get("/classify_image")
async def classify_image(image_url: str | None = None) -> dict:
  start_time = time.time()
  if image_url is None:
    raise HTTPException(
      status_code=422, 
      detail="Missing query parameter 'image_url'"
    )

  # Load image from URL
  try:
    img_pil = Image.open(urlopen(image_url))
  except (HTTPError, URLError):
    raise HTTPException(
      status_code=422, 
      detail="Unprocessable Entity"
    )
  except:
    raise HTTPException(
      status_code=500,
      detail="Internal Server Error"
    )
  if img_pil.mode == 'RGBA':
    # Convert the image to RGB if it has an alpha channel
    img_pil = img_pil.convert('RGB')

  #Image Transformation for Prediction
  img_tensor : torch.Tensor = image_transformations(img_pil)
  img_tensor = img_tensor.unsqueeze(dim=0)
  tensor_prediction = pytorch_model(img_tensor)
  print(tensor_prediction)
  class_prediction = torch.argmax(tensor_prediction, 1).item()
  
  print(time.time() - start_time)
  #Returning Prediction Values
  return {
    "class_integer" : class_prediction,
    "class_string" : all_classes[class_prediction]
  }

if __name__=="__main__":
  uvicorn.run(fast_api_app,host="127.0.0.1",port=8080)