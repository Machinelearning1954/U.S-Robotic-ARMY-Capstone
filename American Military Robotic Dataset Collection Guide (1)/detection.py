"""
Vehicle Detection API Routes
Handles image upload and vehicle detection using YOLOv8 model
"""

import os
import io
import base64
from flask import Blueprint, request, jsonify
from PIL import Image
import numpy as np
from pathlib import Path

# Import YOLO model
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️  Warning: ultralytics not installed. Detection will not work.")

detection_bp = Blueprint('detection', __name__)

# Load model at module level (singleton pattern)
MODEL_PATH = Path(__file__).parent.parent.parent.parent / 'models' / 'best.pt'
model = None

if YOLO_AVAILABLE and MODEL_PATH.exists():
    try:
        model = YOLO(str(MODEL_PATH))
        print(f"✓ Loaded YOLOv8 model from {MODEL_PATH}")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
else:
    print(f"⚠️  Model not found at {MODEL_PATH}")

# Class names for military vehicles
CLASS_NAMES = [
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

@detection_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'model_path': str(MODEL_PATH),
        'yolo_available': YOLO_AVAILABLE
    })

@detection_bp.route('/detect', methods=['POST'])
def detect_vehicles():
    """
    Detect vehicles in uploaded image.
    
    Expected request:
        - multipart/form-data with 'image' file
        OR
        - JSON with 'image' as base64 string
    
    Returns:
        JSON with detection results including bounding boxes, classes, and confidence scores
    """
    
    if model is None:
        return jsonify({
            'success': False,
            'error': 'Model not loaded. Please check server logs.'
        }), 500
    
    try:
        # Get image from request
        image = None
        
        # Try multipart/form-data first
        if 'image' in request.files:
            file = request.files['image']
            if file.filename == '':
                return jsonify({'success': False, 'error': 'No file selected'}), 400
            
            image = Image.open(file.stream)
        
        # Try JSON with base64 image
        elif request.is_json:
            data = request.get_json()
            if 'image' in data:
                # Decode base64 image
                image_data = data['image']
                if ',' in image_data:
                    image_data = image_data.split(',')[1]
                
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
        
        if image is None:
            return jsonify({
                'success': False,
                'error': 'No image provided. Send as multipart/form-data or base64 JSON.'
            }), 400
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Run inference
        results = model(image, conf=0.25, iou=0.45)
        
        # Process results
        detections = []
        result = results[0]
        
        for box in result.boxes:
            # Get box coordinates
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            
            # Get confidence and class
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            
            # Get class name
            class_name = result.names[class_id] if class_id < len(result.names) else f'class_{class_id}'
            
            detections.append({
                'bbox': {
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2,
                    'width': x2 - x1,
                    'height': y2 - y1
                },
                'class': class_name,
                'confidence': confidence,
                'class_id': class_id
            })
        
        # Get annotated image
        annotated_image = result.plot()
        
        # Convert to base64 for sending back to client
        pil_image = Image.fromarray(annotated_image)
        buffered = io.BytesIO()
        pil_image.save(buffered, format="JPEG", quality=95)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'detections': detections,
            'count': len(detections),
            'annotated_image': f'data:image/jpeg;base64,{img_str}',
            'image_size': {
                'width': image.width,
                'height': image.height
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@detection_bp.route('/classes', methods=['GET'])
def get_classes():
    """Get list of supported vehicle classes."""
    return jsonify({
        'classes': CLASS_NAMES,
        'count': len(CLASS_NAMES)
    })

@detection_bp.route('/model-info', methods=['GET'])
def get_model_info():
    """Get information about the loaded model."""
    
    if model is None:
        return jsonify({
            'success': False,
            'error': 'Model not loaded'
        }), 500
    
    try:
        return jsonify({
            'success': True,
            'model_type': 'YOLOv8',
            'model_path': str(MODEL_PATH),
            'classes': CLASS_NAMES,
            'num_classes': len(CLASS_NAMES),
            'input_size': 640,
            'framework': 'Ultralytics YOLOv8'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

