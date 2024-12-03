# %%
from predict import get_boundaries
import librosa
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from tqdm import tqdm

# %%
# inference on single wav
ckpt = "C:\\Users\\sriha\\OneDrive - International Institute of Information Technology\\Sem7\\SAL\\Project Proposal\\UnsupSeg\\pretrained_models\\timit+_pretrained.ckpt"
# wav = "C:\\Users\\sriha\\OneDrive - International Institute of Information Technology\\Sem7\\SAL\\Project Proposal\\timit_directory\\test\\DR1_FAKS0_SA1.wav"

# %%
def parse_phone_data(file_path):
    phone_boundaries = []
    with open(file_path, 'r') as f:
        for line in f:
            # Skip any empty lines or lines that are comments
            if line.strip() == '' or line.startswith('#'):
                continue
            # Split the line into start, end, and phone label
            start, end, label = line.split()
            start = int(start)
            end = int(end)
            phone_boundaries.append((start, end, label))
    return phone_boundaries

# %%

def get_unmatched_gt(audio_file_path):
    phone_file_path = audio_file_path[:-3]+"phn"  # Replace with the path to your phone boundary text file

    # Load audio
    audio_data, sr = librosa.load(audio_file_path, sr=16000)

    temp = get_boundaries(audio_file_path,ckpt,prominence=0.05)

    boundary_indices = [int(t * sr) for t in temp]

    # Parse the phone boundaries from the text file
    phone_boundaries = parse_phone_data(phone_file_path)

    gt_boundaries=[]
    for (i,boundary) in enumerate(phone_boundaries[1:]):
        gt_boundaries.append((boundary[0],phone_boundaries[i-1][-1],boundary[2]))
    
    threshold = (20/1000)*sr # 20 ms
    unmatched_gt = []
    matched_gt =[]
    unmatched_pred = list(boundary_indices)
    for gt_b in gt_boundaries:
        closest_pred = min(unmatched_pred, key=lambda p: abs(p - gt_b[0]), default=None)
        if closest_pred is not None and abs(closest_pred - gt_b[0]) <= threshold:
            # matched.append((gt_b, closest_pred))
            unmatched_pred.remove(closest_pred)
            if(gt_b[1]=='h#' or gt_b[2]=='h#'):
                continue
            matched_gt.append(gt_b)
        else:
            if(gt_b[1]=='h#' or gt_b[2]=='h#'):
                continue
            unmatched_gt.append(gt_b)
    return unmatched_gt

# %%
audio_directory_path = 'C:\\Users\\sriha\\OneDrive - International Institute of Information Technology\\Sem7\\SAL\\Project Proposal\\timit_directory\\train'

# List to store the results
ans = []

# Iterate through all audio files in the given directory
for audio_file in tqdm(os.listdir(audio_directory_path)):
    audio_file_path = os.path.join(audio_directory_path, audio_file)
    
    # Ensure the file is a .wav or relevant audio format
    if audio_file.endswith('.wav'):  # or other formats, like '.mp3'
        unmatched_gt = get_unmatched_gt(audio_file_path)
        ans.append(unmatched_gt)

# Save the results as a JSON file
output_json_path = 'output_results_train.json'  # Path to save the JSON file
with open(output_json_path, 'w') as json_file:
    json.dump(ans, json_file, indent=0)

# %%
audio_directory_path = 'C:\\Users\\sriha\\OneDrive - International Institute of Information Technology\\Sem7\\SAL\\Project Proposal\\timit_directory\\test'

# List to store the results
ans = []

# Iterate through all audio files in the given directory
for audio_file in tqdm(os.listdir(audio_directory_path)):
    audio_file_path = os.path.join(audio_directory_path, audio_file)
    
    # Ensure the file is a .wav or relevant audio format
    if audio_file.endswith('.wav'):  # or other formats, like '.mp3'
        unmatched_gt = get_unmatched_gt(audio_file_path)
        ans.append(unmatched_gt)

# Save the results as a JSON file
output_json_path = 'output_results_test.json'  # Path to save the JSON file
with open(output_json_path, 'w') as json_file:
    json.dump(ans, json_file, indent=0)

# %%



