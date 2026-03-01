import os
import sys
import yaml
import torch
from ultralytics import YOLO

# ==========================================

# ==========================================

# the path for the dataset 
DATASET_ROOT = r"./data/Fire and Smoke Dataset"

# project Name 
PROJECT_NAME = 'fire_smoke_detection'

# training parameters
EPOCHS = 30
BATCH_SIZE = 12
IMG_SIZE = 640


# ==========================================
# 2. YAML file
# ==========================================

def create_data_config():
    #Generates the data.yaml file required by YOLO with absolute paths

    # We construct full paths to ensure YOLO finds the image
    train_path = os.path.join(DATASET_ROOT, 'train', 'images')
    val_path = os.path.join(DATASET_ROOT, 'valid', 'images')
    test_path = os.path.join(DATASET_ROOT, 'test', 'images')

    # Verify folders exist before running to avoid cryptic errors
    if not os.path.exists(train_path):
        print("error:could not find training images")
        sys.exit()

    config = {
        'path': DATASET_ROOT,
        'train': train_path,
        'val': val_path,
        'test': test_path,
        'nc': 2,
        'names': {0: 'Fire', 1: 'Smoke'}  
    }

    # Save this config file 
    yaml_path = os.path.join(os.getcwd(), 'fire_dataset_local.yaml')

    with open(yaml_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

    print("Configuration file created")
    return yaml_path


# ==========================================
# 3. MAIN EXECUTION
# ==========================================

if __name__ == '__main__':

    #check for GPU
    device = 0 if torch.cuda.is_available() else 'cpu'
    if device == 'cpu':
        print("***WARNING***: No GPU detected")
    else:
        print(f"GPU detected: {torch.cuda.get_device_name(0)}")

    #create config
    yaml_file = create_data_config()

    #load model
    print("Loading YOLOv9-c model")
    model = YOLO('yolov9c.pt')

    #train
    print("Starting Training...")
    try:
        model.train(
            data=yaml_file,
            epochs=EPOCHS,
            imgsz=IMG_SIZE,
            batch=BATCH_SIZE,
            device=device,
            project='runs/detect',
            name=PROJECT_NAME,
            exist_ok=True,
            patience=10,
            save=True,
            verbose=True,
            workers=2 
        )
    except Exception as e:
        print(f"***AN ERROR OCCURRED DURING TRAINING***: {e}")

    # Validate
    print("Validating...")
    try:
        metrics = model.val()
        print(f"Validation Complete. mAP50-95: {metrics.box.map}")
    except:
        print("Validation skipped due to previous error.")

    # Export
    print("Exporting model to ONNX")
    try:
        export_path = model.export(format='onnx')
    except:
        pass

