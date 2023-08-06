import os
from PIL import Image
import cv2
import random
import shutil

def check_corrupted(img_path, dir_in):
    img = Image.open(os.path.join(dir_in, img_path))
    img.verify()
    img.close()
    img = Image.open(os.path.join(dir_in, img_path))
    img.transpose(Image.FLIP_LEFT_RIGHT)
    img.close()

def check_corrupted_images_in_directory(dir_in):
    count = 0
    for img_path in os.listdir(dir_in):
        if img_path.endswith('.JPG'):
            try:
                check_corrupted(img_path, dir_in)
            except(IOError, SyntaxError)as e:
                print(f'Bad file : {img_path}')
                count = count+1
    print(f"Number of corrupted images : {count}")


def extension_to_jpg(file_path, dir_in):
    file_name = file_path.split('.')[0]
    os.rename(os.path.join(dir_in, file_path),
              os.path.join(dir_in, file_name+".jpg"))

def to_lower(file_path, dir_in):
    file_name = file_path.split('.')[0]
    file_extension = file_path.split('.')[1]
    file_ext_low = file_extension.lower()
    os.rename(os.path.join(dir_in, file_path), os.path.join(
                  dir_in, file_name+'.'+file_ext_low))

def check_naming_conventions(dir_in):
    for img_path in os.listdir(dir_in):
        # Checking for jpeg extension
        if img_path.endswith('JPEG') or img_path.endswith('jpeg'):
            extension_to_jpg(img_path, dir_in)
            # checking for upper case extension
        elif img_path.endswith('JPG'):
            to_lower(img_path, dir_in)

def detect_and_fix(img_path, img_name):
    try:
        with open( img_path, 'rb') as im :
            im.seek(-2,2)
            if im.read() == b'\xff\xd9':
                print('Image OK :', img_name) 
            else: 
                img = cv2.imread(img_path)
                cv2.imwrite( img_path, img)
                print('FIXED corrupted image :', img_name)           
    except(IOError, SyntaxError) as e :
        print(e)
    print("Unable to load/write Image : {} . Image might be destroyed".format(img_path) )

def detect_and_fix_premature_ending(dir_path):
    for path in os.listdir(dir_path):
        if path.endswith('.jpg'):
            img_path = os.path.join(dir_path, path)
            detect_and_fix( img_path=img_path, img_name = path)
    print("Process Finished")


def separate_and_copy_files(folders, dest_main_folder):
    # Create the main folder to host the data eg. inside the YOLO folder. [Creates it only if it does not exist.]
    if not os.path.exists(dest_main_folder):
        os.makedirs(dest_main_folder)
        print("Directory '%s' created" % dest_main_folder)
    else:
        print("Directory '%s' already exists, continuing..." % dest_main_folder)

    # Create the train folder for images and labels
    im_train_path = dest_main_folder + os.path.sep + 'images' + os.path.sep + 'train'
    label_train_path = dest_main_folder + os.path.sep + 'labels' + os.path.sep + 'train'
    os.makedirs(im_train_path)
    print("Directory '%s' created" % im_train_path)
    os.makedirs(label_train_path)
    print("Directory '%s' created" % label_train_path)

    for folder in folders:
        for file in os.listdir(folder):
            # Move images to images/train directory
            if file.endswith('.jpg'):
                shutil.copy(folder + os.path.sep + file, im_train_path + os.path.sep + file)
                # Move labels to images/train directory
            elif file.endswith('.txt'):
                shutil.copy(folder + os.path.sep + file, label_train_path + os.path.sep + file)

# Define the folders that contain the original data you want to seperate
folder1 = '/path/to/1st/dataset/obj_train_data'
folder2 = '/path/to/2nd/dataset/obj_train_data'
# Put them in a list
folders = [folder1, folder2]

dest_main_folder = '/destination/path/for/main/folder'

separate_and_copy_files(folders, dest_main_folder)


def create_val_folders(img_val_path, label_val_path):
    val_paths = [img_val_path, label_val_path]
    for val_path in val_paths:
        if not os.path.exists(val_path):
            os.makedirs(val_path)
            print("Directory '%s' created" % val_path)
        else:
            print("Directory '%s' already exists, continuing..." % val_path)

def split_dataset(images_path, labels_path, img_val_path, label_val_path, split_fraction):
    create_val_folders(img_val_path, label_val_path)

    images = os.listdir(images_path)
    labels = os.listdir(labels_path)

    valid_images = random.sample(
        images, (int(round(len(images) * split_fraction))))

    valid_labels = []
    for name in valid_images:
        print("Val image:", name)
        valid_labels.append(name.split('.')[0] + '.txt')

    for val_image in valid_images:
        shutil.move(images_path + os.path.sep + val_image,
                    img_val_path + os.path.sep + val_image)
        print("Moved ", val_image, " to validation images")

    for val_label in valid_labels:
        shutil.move(labels_path + os.path.sep + val_label,
                    label_val_path + os.path.sep + val_label)
        print("Moved ", val_label, " to validation labels")
