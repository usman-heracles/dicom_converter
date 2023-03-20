
# To convert a DICOM file to an MP4 video, you'll need two libraries: pydicom to read and manipulate DICOM files, and imageio for writing the output video file. Let's start by installing the required libraries:

# Install the libraries using pip:
# bash
# Copy code
# pip install pydicom imageio imageio-ffmpeg
# imageio-ffmpeg is a plugin for imageio to handle video formats, and it is required to save videos in MP4 format.

# Create a Python script to convert the DICOM file to an MP4 video:
# python
# Copy code

import os
import sys
import pydicom
from pydicom.pixel_data_handlers import pylibjpeg_handler
import numpy as np
import cv2

def load_dcm_series(dcm_dir):
    dcm_files = []
    for root, _, files in os.walk(dcm_dir):
        for file in files:
            if file.endswith('.DCM'):
                dcm_files.append(os.path.join(root, file))
    dcm_files.sort()
    dcm_files_read = [pydicom.dcmread(file) for file in dcm_files]
    return dcm_files_read

def dcm_to_np_series(dcm_series):
    all_pixel_arrays = [pylibjpeg_handler.as_array(dcm) for dcm in dcm_series if 'PixelData' in dcm]
    return [np.reshape(series, series.shape + (1, )) for series in all_pixel_arrays if series.ndim == 3]

# def normalize_array(array, max_value=255):
#     array_min = array.min()
#     array_max = array.max()
#     normalized = (array - array_min) * max_value // (array_max - array_min)
#     return normalized.astype(np.uint8)

def mkfilename(idx, output_file):
    idx_output_file = output_file
    idx_output_file = f'{output_file[:-4]}_{idx}{output_file[-4:]}'
    return idx_output_file  

def save_as_mp4(np_series, output_file, fps=15):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30
    for idx, video in enumerate(np_series):
        idx_output_file = mkfilename(idx, output_file)
        size = (video.shape[1], video.shape[2])
        video_writer = cv2.VideoWriter(idx_output_file, fourcc, fps, size)
        # Write each frame to the video file
        for frame_idx in range(video.shape[0]):
            frame = video[frame_idx, :, :, :]
            video_writer.write(cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR))            
        video_writer.release()

        # for idx, np_image in enumerate(np_series):
        #     idx_output_file = mkfilename(idx, output_file)
        #     with imageio.get_writer(idx_output_file, mode='I', fps=fps) as writer:
        #     # writer.append_data(normalize_array(np_image))
        #         print(idx, np_image.ndim, np_image.shape)
        #         print(np_image.shape[0], np_image.shape[1], np_image.shape[2], np_image.shape[3])
        #         for frame in range(np_image.shape[0]):
        #             writer.append_data(np_image[frame, :, :, :])
        #         writer.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python dicom_to_mp4.py <input_dicom_folder> <output_mp4_file>')
        sys.exit(1)

    dcm_dir = sys.argv[1]
    output_file = sys.argv[2]

    dcm_series = load_dcm_series(dcm_dir)
    np_series = dcm_to_np_series(dcm_series)

    print([(series.ndim, series.shape) for series in np_series])
    save_as_mp4(np_series, output_file)
    print(f'Successfully converted DICOM series to {output_file}')

# Save the script as dicom_to_mp4.py and run it from the command line:
# bash
# Copy code
# python dicom_to_mp4.py <input_dicom_folder> <output_mp4_file>
# Replace <input_dicom_folder> with the path to your folder containing DICOM files and <output_mp4_file> with the desired output MP4 file name, including the .mp4 extension.

# This script assumes that the input is a folder containing a series of DICOM files forming a single 2D image series (e.g., an MRI or CT scan). It will load the DICOM files, convert them to a NumPy array, normalize the pixel values, and save the result as an MP4 video file