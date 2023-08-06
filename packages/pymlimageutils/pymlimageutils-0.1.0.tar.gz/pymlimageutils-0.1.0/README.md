## mlutils
This package is useful for checking image data quality, separating image and label files, and splitting datasets.

#### Requirements
The package requires the following dependencies to be installed:
   - os
   - PIL (Python Imaging Library)
   - cv2 (OpenCV)
   - random
   - shutil

#### Installation
you can install mlutils via pip:
``
pip install mlutils
``
#### Usage
##### Check for corrupted images
Use the check_corrupted_images_in_directory(dir_in) function to check for corrupted images in a directory. It returns the number of corrupted images found.
```python
from mlutils import check_corrupted_images_in_directory
check_corrupted_images_in_directory("/path/to/images/folder")
```
#####Check image naming conventions
Use the check_naming_conventions(dir_in) function to check and fix image naming conventions in a directory. This function renames images with upper-case file extensions to lower-case and changes "jpeg" to "jpg" file extensions.
```python
from mlutils import check_naming_conventions
check_naming_conventions("/path/to/images/folder")
```
####Detect and fix images with a premature ending
Use the detect_and_fix_premature_ending(dir_path) function to detect and fix images with a premature ending in a directory. It returns the number of fixed images.
```python
from mlutils import detect_and_fix_premature_ending
detect_and_fix_premature_ending("/path/to/images/folder")
```
####Separate and copy files
Use the separate_and_copy_files(folders, dest_main_folder) function to separate image and label files from multiple folders and copy them to a new destination folder.
```python
from mlutils import separate_and_copy_files
folders = ["/path/to/1st/images/folder", "/path/to/2nd/images/folder"]
dest_main_folder = "/path/to/destination/folder"
separate_and_copy_files(folders, dest_main_folder)
```
####Split a dataset
Use the split_dataset(images_path, labels_path, img_val_path, label_val_path, split_fraction) function to split a dataset into training and validation sets. The function moves a fraction of images and their corresponding label files to validation folders.
```python
from mlutils import split_dataset
images_path = "/path/to/training/images"
labels_path = "/path/to/training/labels"
img_val_path = "/path/to/validation/images"
label_val_path = "/path/to/validation/labels"
split_fraction = 0.2 # 20% of the data will be moved to validation set
split_dataset(images_path, labels_path, img_val_path, label_val_path, split_fraction)
```






