import os, tempfile
def save_uploaded_file(uploaded_file, target_dir='uploads'):
    os.makedirs(target_dir, exist_ok=True)
    path = os.path.join(target_dir, uploaded_file.name)
    with open(path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return path
