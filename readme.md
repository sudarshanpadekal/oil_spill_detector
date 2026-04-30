# Oil Spill Classification System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-ee4c2c)
![License](https://img.shields.io/badge/License-MIT-green)

A deep learning project to detect and classify oil spills from images using a fine-tuned ResNet18 architecture.

## Overview

This repository contains an end-to-end PyTorch pipeline for classifying images into two categories: `oil` and `no_oil`. It leverages transfer learning on a pre-trained ResNet18 model, modifying the final fully connected layer for binary classification.

## Features

- **Transfer Learning**: Uses ResNet18 pre-trained weights for robust feature extraction.
- **Data Augmentation & Preprocessing**: Images are resized, converted to 3-channel grayscale (if needed), and normalized to match the expected ResNet input distribution.
- **Training Pipeline**: Complete training script (`train.py`) with an 80-20 train-validation split, cross-entropy loss, and Adam optimizer.
- **Evaluation**: A separate script (`evaluate.py`) to generate key metrics including Accuracy, Precision, Recall, and F1-Score using `scikit-learn`.

## Repository Structure

- `train.py`: Main script to train the ResNet18 model and save weights to `oil_model.pth`.
- `evaluate.py`: Loads the saved model and evaluates it against the test set, outputting detailed metrics.
- `model.py`, `dataset_loader.py`, `test_train_split.py`, `training_loop.py`: Prototype scripts and modular components for data loading and model architecture.
- `dataset/`: Directory expected to contain the image dataset organized into subfolders by class.

## Requirements

To run this project, you need the following libraries installed:

```bash
pip install torch torchvision scikit-learn
```

## Usage

### 1. Prepare the Dataset
Ensure your dataset is placed in the root directory under a folder named `dataset/` with the following structure:
```text
dataset/
├── oil/
│   ├── image1.jpg
│   └── ...
└── no_oil/
    ├── image1.jpg
    └── ...
```

### 2. Train the Model
Run the training script. This will train the model for 5 epochs (default) and save the best weights to `oil_model.pth`.

```bash
python train.py
```

### 3. Evaluate the Model
After training, you can evaluate the model's performance on the validation set by running:

```bash
python evaluate.py
```

## Model Performance

Based on recent test evaluations on the validation split, the model achieves the following metrics:

- **Accuracy**: 88.63%
- **Precision**: 93.79%
- **Recall**: 71.20%
- **F1 Score**: 80.95%

## License

This project is open-source and available under the [MIT License](LICENSE).
