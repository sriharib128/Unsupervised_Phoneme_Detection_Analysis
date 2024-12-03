# Phoneme Boundary Detection and Analysis: Codebase Documentation

This repository contains the codebase for a project focused on unsupervised phoneme boundary detection and analysis. The primary goal of the project is to predict phoneme boundaries using an unsupervised model, evaluate its performance, and analyze errors based on linguistic properties such as the manner of articulation.

---

## **Repository Structure**

```plaintext
.
├── original_readme.md           # Original documentation from the model's author
├── spec-file.yml                # Conda environment file for replicating experiments

├── other files from the original git repository https://github.com/felixkreuk/UnsupSeg.git.

├── get_all_matched.py           # Script to extract matched boundaries
├── get_all_unmatched.py         # Script to extract unmatched boundaries
├── vis.ipynb                    # Notebook for generating plots and visualizations
└── analysis/
    ├── json files  # Matched and Unmatched boundaries from the proposed model
    ├── phoneme_data.csv             # Mapping of phonemes to their manner of articulation
    └── Linguistic Analysis.ipynb    # Step-by-step process for analysis and results generation
```

---

## **Installation and Setup**

1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/sriharib128/Unsupervised_Phoneme_Detection_Analysis.git
   cd Unsupervised_Phoneme_Detection_Analysis
   ```

2. **Setup Environment**:  
   Use the `spec-file.yml` to create the conda environment:  
   ```bash
   conda env create -f spec-file.yml
   conda activate phoneme-analysis
   ```

3. **Prepare Dataset**:  
   Ensure the TIMIT dataset is placed in the following directory structure:  
   ```plaintext
    ├── timit_directory/           # TIMIT dataset in the required directory structure
    │   ├── test/                  # Test set
    │   │   ├── DR1_FAKS0_SA1.phn
    │   │   ├── DR1_FAKS0_SA1.wav
    │   ├── train/                 # Training set
    │       ├── DR1_FCJF0_SA1.phn
    │       ├── DR1_FCJF0_SA1.wav
    ```

4. **Model Setup**  
   Follow the instructions in `original_readme.md` for setting up the model.

---

## **Workflow**

### **Step 1: Boundary Prediction**
Use the unsupervised model to predict phoneme boundaries for the TIMIT dataset. After running the model, the predictions are compared against the ground truth phoneme boundaries with a tolerance of 20 ms.
```bash
# inference on single wav
python predict.py --ckpt "./pretrained_models/timit+_pretrained.ckpt" --wav "your_audio"
```
### **Step 2: Extract Matched and Unmatched Boundaries**
Run the following scripts to extract matched and unmatched phoneme boundaries:  
- **Extract Matched Boundaries**:  
  ```bash
  python get_all_matched.py
  ```
  This generates the `matched_results_test.json` and `matched_results_train.json` files in the `analysis/` directory.

- **Extract Unmatched Boundaries**:  
  ```bash
  python get_all_unmatched.py
  ```
  This generates the `output_results_test.json` and `output_results_train.json` files in the `analysis/` directory.

### **Step 3: Analysis and Visualization**
1. Use the `phoneme_data.csv` file to map phonemes to their manner of articulation.  
2. Perform linguistic analysis on the extracted boundaries using the `Linguistic Analysis.ipynb`.  
3. Generate various visualizations using the `vis.ipynb` notebook.

---

## **Results**

### **Precision**
- Achieved a precision of **0.85** on the TIMIT dataset with a tolerance of 20 ms.

### **Key Findings**  
- **Error Trends**: High failure rates were observed for specific phoneme categories, particularly approximants, where slow and gradual transitions are difficult to capture.  
- **Strengths**: The model performed well on stops and fricatives due to their sharp and abrupt transitions.  
- **Linguistic Insights**: Errors were more frequent between phonemes with similar manners of articulation.

---

## **File Details**

##### **`vis.ipynb`**
Generates various plots for boundary analysis and visualizations of the audio waveform.

##### **`phoneme_data.csv`**
A CSV file mapping each phoneme to its linguistic properties:  
- **Manner of Articulation**  
- **Place of Articulation**  
- **Voicing**

##### **`Linguistic Analysis.ipynb`**
Provides a step-by-step process for:  
1. Grouping phonemes by linguistic properties.  
2. Computing co-occurrence matrices.  
3. Analyzing matched and unmatched phoneme boundaries.

---

## **Future Work**
- Improve the unsupervised model to better predict boundaries by training on more data.
- Align the predicted boundaries with the phonemes.
- Add stress detection to the phoneme boundary detection process.

---
