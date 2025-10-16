# Research Findings: Military Vehicle Recognition

## Academic Papers Found

### 1. Deep Learning Based Vehicle Detection with Images from UAVs
- **Authors:** M. Böyük et al.
- **Year:** 2020
- **Citations:** 35
- **URL:** https://ieeexplore.ieee.org/document/9259868/
- **Methods:** Faster R-CNN, YOLOv3-Tiny, SSD
- **Application:** UAV-based vehicle detection
- **Key Findings:** Automatic position detection of vehicles from aerial imagery

### 2. The Effect of Simulation Variety on Deep Learning-Based Military Vehicle Detector
- **Authors:** T.A. Eker et al.
- **Year:** 2023
- **Citations:** 13
- **URL:** https://www.spiedigitallibrary.org/conference-proceedings-of-spie/12742/127420O/
- **Methods:** Deep learning with synthetic data
- **Key Findings:** Military vehicle detector can be developed using only synthetic data

### 3. Military Vehicles Detection in Satellite & Aerial Imagery
- **Authors:** Nader Narcisse
- **Year:** 2023
- **URL:** https://wandb.ai/nadernarcisse/MVD-Satellite-Imagery/reports/
- **Methods:** Detectron2, Transfer Learning
- **Application:** Satellite and aerial imagery analysis

### 4. Object Detection for Military Surveillance using YOLO
- **Authors:** S. Borthakur et al.
- **Year:** 2023
- **Citations:** 2
- **URL:** https://ieeexplore.ieee.org/document/10440938/
- **Methods:** YOLO CNN architectures
- **Application:** Military surveillance

### 5. Edge Device Based Military Vehicle Detection from UAV
- **Authors:** Various
- **Year:** 2021
- **URL:** https://link.springer.com/article/10.1007/s11042-021-11242-y
- **Methods:** SSD MobileNet v2, Tiny YOLO v3
- **Application:** Real-time classification on edge devices

## Public Repositories Found

### 1. Automated Detection of Military Vehicles (ADOMVI)
- **URL:** https://github.com/jonasrenault/adomvi
- **Description:** State-of-the-art military vehicle tracker with YOLOv8
- **Status:** Active repository with notebooks and resources

### 2. Zero-Shot Multimodal Deep Learning
- **URL:** https://review.sto.nato.int/index.php/journal-issues/2023-fall/sas-ora-conference-2022/69-zero-shot-multimodal-deep-learning-models-for-military-vehicle-detection-an-analysis
- **Methods:** CLIP model for zero-shot detection
- **Application:** Text-prompt based vehicle identification

## Key Techniques Identified

1. **YOLO Family** (YOLOv3, YOLOv5, YOLOv8)
2. **Faster R-CNN**
3. **SSD (Single Shot Detector)**
4. **Detectron2**
5. **Transfer Learning**
6. **Synthetic Data Training**
7. **Zero-Shot Learning (CLIP)**

## Next Steps

1. Access and analyze the ADOMVI repository
2. Review Detectron2 implementation
3. Identify baseline metrics from papers
4. Reproduce selected approaches



## Detailed Analysis: Detectron2 Mask R-CNN Approach

### Paper: Military Vehicles Detection in Satellite & Aerial Imagery using Instance Segmentation

**Author:** Nader Narcisse
**Platform:** Weights & Biases
**URL:** https://wandb.ai/nadernarcisse/MVD-Satellite-Imagery/reports/

**Key Information:**

**Model:** Mask R-CNN (Region-based Convolutional Neural Network)
- Framework: Detectron2 (Meta AI Research)
- Introduced by Facebook AI Research (FAIR) in 2017
- Extends Faster R-CNN with mask branch for segmentation

**Dataset:**
- 200 satellite and aerial images in RGB format
- 10,624 annotated Russian military vehicles
- Source: Google Earth + Maxar Technologies
- Annotation tool: LabelMe (MIT CSAIL)
- High-resolution imagery with geospatial data

**Approach:**
- Transfer learning methodology
- Instance segmentation (not just bounding boxes)
- Predicts locations, classes, and shapes of objects
- Generates segmentation masks for precise boundaries

**Challenges Addressed:**
- High resolution images
- Large image sizes
- Clutter and occlusions in satellite imagery
- Complex environments

**Performance:**
- Achieved good performance in detecting military vehicles
- Effective even in complex and cluttered environments
- Evaluated on separate unseen test set

**Key Advantage:**
- Provides segmentation masks (pixel-level precision)
- Better than bounding boxes for military applications
- Enables precise vehicle identification and counting

