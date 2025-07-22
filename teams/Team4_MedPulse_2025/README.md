# 🫀 Cardiovascular Disease Detection System

A multi-modal AI-based system for detecting cardiovascular diseases by combining structured clinical data and chest X-ray images using deep learning models.

---

## 🚀 Project Overview

This project leverages deep learning techniques to detect the presence of **10 major cardiovascular diseases** by utilizing:
- **Structured EHR data** (vitals, labs, demographics)
- **Chest X-ray images** from the MIMIC-CXR dataset

The aim is to provide accurate disease predictions by integrating image and tabular data using a hybrid model architecture (ResNet-50 + MLP).

---

## 📁 Dataset

We use a balanced, preprocessed subset of the **MIMIC-IV** and **MIMIC-CXR** datasets:
- **Structured Inputs (12 features)**:
  - Heart Rate
  - Arterial BP (Systolic & Diastolic)
  - SpO₂
  - Temperature
  - Sodium, Potassium
  - Glucose (serum)
  - Cholesterol
  - Respiratory Rate
  - Gender
  - Anchor Age
- **Images**:
  - PNG-formatted chest X-rays derived from DICOM files
  - Linked using subject ID and DICOM ID

> 💡 The dataset is pre-split into `train`, `val`, and `test` sets (80:10:10).

---

## 🧠 Model Architecture

- **Image Branch**: Pretrained ResNet-50 CNN (with modified FC layer)
- **Structured Data Branch**: Fully-connected neural network (MLP)
- **Fusion Layer**: Concatenates image and structured features before final prediction
- **Output**: Multi-label sigmoid classification layer for 10 cardiovascular diseases

---

## 🔧 Technologies Used

- **PyTorch** for model building and training
- **Pandas / NumPy** for data preprocessing
- **OpenCV & PIL** for image handling
- **Matplotlib / Seaborn** for visualization
- **GPU acceleration** (NVIDIA CUDA supported)

---

## 🧪 Evaluation Metrics

- **Accuracy**
- **Precision, Recall, F1-Score (per disease)**
- **ROC-AUC**
- **Confusion Matrix**

---

## ⚙️ Installation

```bash
git clone https://github.com/your_username/cardio-disease-detection.git
cd cardio-disease-detection

# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
