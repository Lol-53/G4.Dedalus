import kagglehub
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Download latest version
path = kagglehub.dataset_download("uom190346a/disease-symptoms-and-patient-profile-dataset")

print("Path to dataset files:", path)


# Load the dataset
data = pd.read_csv(path + "/disease_symptom_dataset.csv")

data