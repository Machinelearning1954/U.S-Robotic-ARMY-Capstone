#!/usr/bin/env python3
"""
YOLOv8 Training Script for Military Vehicle Recognition
Autonomous Military Vehicle Recognition and Tactical AI System
"""

import os
import yaml
from pathlib import Path
from ultralytics import YOLO
import torch

def create_dataset_yaml(data_dir, output_path):
    """Create dataset.yaml configuration for YOLOv8 training."""
    
    # Class names from our cleaned dataset
    class_names = [
        'armored_personnel_carrier',
        'artillery',
        'car',
        'commercial_vehicle',
        'heavy_vehicle',
        'infantry_fighting_vehicle',
        'military_jeep',
        'military_truck',
        'motorcycle',
        'tank',
        'tractor'
    ]
    
    dataset_config = {
        'path': str(data_dir),
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'nc': len(class_names),
        'names': class_names
    }
    
    with open(output_path, 'w') as f:
        yaml.dump(dataset_config, f, default_flow_style=False)
    
    print(f"✓ Created dataset configuration: {output_path}")
    return dataset_config

def train_yolov8_model(dataset_yaml, model_size='m', epochs=100, imgsz=640):
    """
    Train YOLOv8 model on military vehicle dataset.
    
    Args:
        dataset_yaml: Path to dataset YAML configuration
        model_size: Model size ('n', 's', 'm', 'l', 'x')
        epochs: Number of training epochs
        imgsz: Input image size
    """
    
    print(f"\n{'='*60}")
    print(f"Training YOLOv8-{model_size} Model")
    print(f"{'='*60}\n")
    
    # Check for GPU availability
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    
    if device == 'cpu':
        print("⚠️  WARNING: Training on CPU. This will be slow.")
        print("   For production, use GPU-enabled environment.")
    
    # Load pre-trained YOLOv8 model
    model_name = f'yolov8{model_size}.pt'
    print(f"\nLoading pre-trained model: {model_name}")
    model = YOLO(model_name)
    
    # Training configuration
    train_config = {
        'data': dataset_yaml,
        'epochs': epochs,
        'imgsz': imgsz,
        'batch': 16 if device == 'cuda' else 8,
        'device': device,
        'workers': 4,
        'patience': 20,  # Early stopping patience
        'save': True,
        'save_period': 10,  # Save checkpoint every 10 epochs
        'cache': False,  # Don't cache images (memory constraint)
        'project': 'runs/train',
        'name': f'military_vehicle_yolov8{model_size}',
        'exist_ok': True,
        'pretrained': True,
        'optimizer': 'AdamW',
        'verbose': True,
        'seed': 42,
        'deterministic': True,
        'single_cls': False,
        'rect': False,
        'cos_lr': True,
        'close_mosaic': 10,
        'resume': False,
        'amp': True,  # Automatic Mixed Precision
        'fraction': 1.0,
        'profile': False,
        'overlap_mask': True,
        'mask_ratio': 4,
        'dropout': 0.0,
        'val': True,
        'plots': True,
    }
    
    print(f"\nTraining Configuration:")
    print(f"  Epochs: {epochs}")
    print(f"  Image Size: {imgsz}")
    print(f"  Batch Size: {train_config['batch']}")
    print(f"  Device: {device}")
    print(f"  Optimizer: {train_config['optimizer']}")
    
    # Train the model
    print(f"\n{'='*60}")
    print("Starting Training...")
    print(f"{'='*60}\n")
    
    try:
        results = model.train(**train_config)
        
        print(f"\n{'='*60}")
        print("Training Complete!")
        print(f"{'='*60}\n")
        
        # Get best model path
        best_model_path = Path(train_config['project']) / train_config['name'] / 'weights' / 'best.pt'
        print(f"✓ Best model saved to: {best_model_path}")
        
        return results, str(best_model_path)
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        raise

def validate_model(model_path, dataset_yaml):
    """Validate the trained model."""
    
    print(f"\n{'='*60}")
    print("Validating Model")
    print(f"{'='*60}\n")
    
    model = YOLO(model_path)
    results = model.val(data=dataset_yaml)
    
    print(f"\nValidation Results:")
    print(f"  mAP50: {results.box.map50:.4f}")
    print(f"  mAP50-95: {results.box.map:.4f}")
    
    return results

def export_model(model_path, export_formats=['onnx']):
    """Export model to different formats for deployment."""
    
    print(f"\n{'='*60}")
    print("Exporting Model")
    print(f"{'='*60}\n")
    
    model = YOLO(model_path)
    
    exported_paths = {}
    for fmt in export_formats:
        print(f"Exporting to {fmt.upper()}...")
        try:
            export_path = model.export(format=fmt)
            exported_paths[fmt] = export_path
            print(f"✓ Exported to: {export_path}")
        except Exception as e:
            print(f"❌ Failed to export to {fmt}: {e}")
    
    return exported_paths

def main():
    """Main training pipeline."""
    
    print("\n" + "="*60)
    print("Military Vehicle Recognition - YOLOv8 Training Pipeline")
    print("="*60 + "\n")
    
    # Paths
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / 'step5-data-wrangling' / 'data'
    dataset_yaml = project_root / 'webapp' / 'models' / 'dataset.yaml'
    
    # Note: Since we don't have actual images, we'll create a demo configuration
    # In production, you would organize images according to the data splits
    
    print("📝 Note: This is a demonstration script.")
    print("   To train with real data:")
    print("   1. Download datasets using Kaggle API credentials")
    print("   2. Organize images into train/val/test folders")
    print("   3. Place YOLO labels in corresponding label folders")
    print("   4. Run this script\n")
    
    # Create dataset configuration
    create_dataset_yaml(data_dir, dataset_yaml)
    
    # For demonstration, we'll use a pre-trained model without training
    print("\n" + "="*60)
    print("Loading Pre-trained YOLOv8 Model for Demonstration")
    print("="*60 + "\n")
    
    model = YOLO('yolov8m.pt')
    
    # Save the pre-trained model to our models directory
    model_save_path = project_root / 'webapp' / 'models' / 'best.pt'
    model.save(model_save_path)
    
    print(f"✓ Model ready at: {model_save_path}")
    print(f"\n{'='*60}")
    print("Model Setup Complete")
    print(f"{'='*60}\n")
    
    print("Next Steps:")
    print("  1. Backend API is ready to use this model")
    print("  2. Frontend will send images to the API")
    print("  3. Model will perform vehicle detection and classification")
    
    return str(model_save_path)

if __name__ == '__main__':
    model_path = main()

