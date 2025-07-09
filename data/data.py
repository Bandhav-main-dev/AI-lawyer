import kagglehub

# Download latest version
path = kagglehub.dataset_download("dev523/indian-penal-code-ipc-sections-information")

print("Path to dataset files:", path)