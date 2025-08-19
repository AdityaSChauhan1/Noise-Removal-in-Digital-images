# 🖼️ Image Noise Removal & Histogram Visualization

A Python project for **image restoration and analysis** that applies advanced spatial-domain filters to noisy images and visualizes histograms for better insight.  
This project was developed during my internship at **DRDO DEAL** as part of noise reduction in satellite imagery.


## 🚀 Features

- **Noise Removal Filters**:
  - Arithmetic, Geometric, Harmonic Mean Filters
  - Contraharmonic Filter
  - Median, Max, Min, Midpoint Filters
  - Alpha-Trimmed Mean Filter
  - Adaptive Median Filter (handles high-density impulse noise)

- **Histogram Visualization (PyQt5 GUI)**:
  - Compute intensity histograms from image matrices
  - Normalize frequency distribution
  - Display histograms with interactive GUI

- **Optimized Processing**:
  - Efficient matrix operations using **NumPy** and **SciPy**
  - Modular and extensible filter architecture


## 🛠️ Tech Stack

- **Programming Language**: Python
- **Libraries/Frameworks**:
  - NumPy, SciPy – numerical and scientific computing
  - PyQt5 – GUI for histogram visualization
- **Concepts**:
  - Spatial domain filtering
  - Noise models (Gaussian, Salt-and-Pepper, etc.)
  - Image preprocessing & restoration


## ⚙️ Installation & Usage

1. Clone this repository:
   ```
   git clone https://github.com/your-username/image-noise-removal.git
   cd image-noise-removal

2. Install dependencies:
   ```
   pip install numpy scipy PyQt5

4. Run the GUI:
   ```
   python main.py

👤 Author

Aditya S Chauhan

[LinkedIn](https://www.linkedin.com/in/aditya-s-chauhan-25162024a/)
[LeetCode](https://leetcode.com/u/adityachauhansingh000/)
