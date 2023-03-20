import os
import pydicom
import cv2
import matplotlib.pyplot as plt

folder_path = '/Users/usman/Downloads/90142089_2-27-2023_FL-PHARYNX-SWALLOWING-EVAL-WITH-FLUORO'
file_name = '1.2.124.113532.80.22185.2318.20230227.131016.13869577'

# Create an empty dataset
dataset = pydicom.dataset.Dataset()

# Loop over all DICOM files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.DCM'):
        filepath = os.path.join(folder_path, filename)
        # Read the DICOM file and add it to the dataset
        dcm = pydicom.read_file(filepath)
        dataset.add(dcm)

# ds = pydicom.dcmread(folder_path)
# print(ds.patient_name)
print (dataset.patient_name)

# Read DICOM file
dicom_path = os.path.join(folder_path, f'{file_name}.DCM')
dcm = pydicom.dcmread(dicom_path)


# Extract pixel data and convert to uint8
plt.imshow(dcm.pixel_array, cmap='gray')
img = dcm.pixel_array
img = img.astype('uint8')


# Rescale pixel values to 0-255
img_min = img.min()
img_max = img.max()
img = 255.0 * (img - img_min) / (img_max - img_min)
img = img.astype('uint8')

# Create video writer object
mp4_path = os.path.join(folder_path, f'{file_name}.mp4')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 30
size = (img.shape[1], img.shape[0])
video_writer = cv2.VideoWriter(mp4_path, fourcc, fps, size)

# Write each frame to the video file
for i in range(img.shape[2]):
    frame = img[:, :, i]
    video_writer.write(cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR))

# Release video writer object
video_writer.release()
