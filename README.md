
# 雲 (Yun)

## Overview
雲(Yun) is a machine learning project aimed at creating a novel symbolic language system inspired by traditional Chinese characters. The goal is to generate a unified system of symbolic characters akin to QR codes but designed to represent ideas and concepts through machine learning and artificial intelligence. The project uses CLIP for image-text alignment and Diffusion Models for generating new characters based on textual descriptions.

The project's long-term vision is to develop a fully automated method for creating characters that can represent different languages or even abstract ideas, using AI to bridge the gap between visual symbols and human understanding.
## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)


## Installation

### Prerequisites
To run this project, you'll need Python 3.12+ and the following packages:

- `numpy` - For numerical operations
- `pandas` - For data manipulation
- `scikit-learn` - For machine learning algorithms
- `matplotlib` - For visualizing data
- `torch` - For PyTorch framework (or TensorFlow if you prefer)
- `jupyter`  - For notebooks

You can install the dependencies using **pip** or **conda**.

#### Option 1: Using `pip`
```bash
pip install -r requirements.txt
```

#### Option 2: Using `conda`
```bash
conda env create -f environment.yml
conda activate yun_language_env
```

### Setting Up a Virtual Environment (Optional)

It is recommended to use a virtual environment to isolate the dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

## Usage

### Running the Notebook
The project includes Jupyter notebooks for exploratory data analysis (EDA) and model training. You can launch Jupyter with:
```bash
jupyter notebook
```

Then navigate to the desired notebook in the `notebooks/` directory.

### Running Scripts
You can also run scripts from the command line:
```bash
python src/model_training.py
```
For testing or generating new characters:
```bash
python src/data_mining.py
```

## Project Structure
Here’s a quick overview of the project structure:

```plaintext
Yun/
│
├── data/                          # Data directory
│   ├── chinese_dataset/           # Chinese characters dataset
│   │   ├── images/                # Folder for character images
│   │   └── chinese_characters.db  # SQLite database with character meanings
│   └── fonts/                     # Fonts used for rendering characters
│
├── experiments/                   # Experimentation directory
│   ├── logs/                      # Experiment logs and output
│   ├── configs/                   # Experiment configurations and hyperparameters
│   └── results/                   # Results from various experiments
│
├── notebooks/                     # Jupyter notebooks for analysis and model training
│   ├── 01_exploratory_analysis/   # Notebooks for exploratory data analysis (EDA)
│   └── 02_model_training/         # Notebooks for training models
│
├── src/                           # Source code
│   ├── data_mining.py             # Data mining functions and scripts
│   ├── models/                    # Model definitions and implementations
│   │   ├── clip_model.py          # CLIP-based model definitions
│   │   └── diffusion_model.py     # Diffusion-based model definitions
│   ├── evaluation/                # Model evaluation scripts
│   └── utils/                     # Utility functions (e.g., for image processing, data loading)
│
├── models/                        # Saved models
│   └── model_v1.pth               # Trained model files (e.g., CLIP and diffusion models)
│
├── requirements.txt               # Python dependencies
├── environment.yml                # Conda environment file
└── README.md                      # Project overview and instructions


```

