# OCR Custom Training Guide (Google Colab)

## 1. Open Google Colab
Go to [colab.research.google.com](https://colab.research.google.com/) and create a new notebook.

## 2. Enable GPU
Click **Runtime** > **Change runtime type** > Select **T4 GPU**.

## 3. Copy & Run Each Cell Below

### Cell 1: Install Dependencies
```python
!pip install easyocr
!git clone https://github.com/JaidedAI/EasyOCR.git
%cd EasyOCR/trainer
!unzip -q /content/your_dataset.zip -d ./  # Upload your zip first!
```

### Cell 2: Prepare Dataset
*Ensure your dataset zip has two folders: `train` and `val`, each with images and `labels.csv`.*

```python
import os
import torch.backends.cudnn as cudnn
import yaml
from train import train
from utils import AttrDict
import pandas as pd

cudnn.benchmark = True
cudnn.deterministic = False

def get_config(training_folder, valid_folder):
    config = AttrDict()
    config.exp_name = 'custom_handwriting'
    config.train_data = training_folder
    config.valid_data = valid_folder
    config.manualSeed = 1111
    config.workers = 4
    config.batch_size = 32
    config.num_iter = 1000  # Increase for better results (e.g., 5000)
    config.valInterval = 200
    config.saved_model = ''
    config.FT = True
    config.adam = False
    config.lr = 1
    config.beta1 = 0.9
    config.rho = 0.95
    config.eps = 1e-8
    config.grad_clip = 5
    config.select_data = '/'
    config.batch_ratio = '1.0'
    config.total_data_usage_ratio = '1.0'
    config.is_alphanumeric = True # Set False if training on specific chars
    config.imgH = 64
    config.imgW = 600
    config.input_channel = 1
    config.output_channel = 512
    config.hidden_size = 256
    config.saved_model = '' # Path to pretrained model if fine-tuning
    return config
```

### Cell 3: Run Training
```python
config = get_config('./train', './val')
train(config)
```

## 4. Download Your Model
After training, your model will be in `saved_models/custom_handwriting/best_accuracy.pth`.

1. Download `best_accuracy.pth`.
2. Rename it to `custom.pth`.
3. Download the `custom_handwriting.yaml` config (or create one matching your params).

## 5. Install Locally
1. Copy `custom.pth` to `backend/detection/engine/models/`.
2. Restart your backend.
