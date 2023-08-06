import numpy as np
import os

import numpy as np
import pandas as pd
# exec(open("/Users/amitosi/PycharmProjects/chester/diamond/manual_run.py").read())
from PIL import Image

from diamond.run import run
from diamond.user_classes import ImagesAugmentationInfo, ImageModel, ImageModels

# # define directory path
data_dir = '/Users/amitosi/PycharmProjects/chester/chester/data/pizza_not_pizza'
# subdir: not pizza, .jpg
# subdir: pizza, .jpg

# # define image size
img_size = (64, 64)

# define empty arrays to store images and labels
images = []
labels = []

# loop over the directories containing the images

# loop over the subdirectories
for subdir in os.listdir(data_dir):
    # get the full path of the subdirectory
    subdir_path = os.path.join(data_dir, subdir)

    # loop over the files in the subdirectory
    for filename in os.listdir(subdir_path):
        # get the full path of the file
        file_path = os.path.join(subdir_path, filename)

        # load the image using PIL
        img = Image.open(file_path)

        # resize the image to img_size
        img = img.resize(img_size)

        # convert the image to a numpy array
        img = np.array(img)

        # append the image to the images array
        images.append(img)

        # append the label to the labels array
        if subdir == 'pizza':
            labels.append(1)
        else:
            labels.append(0)

# convert the images and labels arrays to numpy arrays
sample_indices = np.random.choice(len(images), size=50, replace=False)
images = np.array(images)[sample_indices]
labels = np.array(labels)[sample_indices]


image_shape = (3, 64, 64)


image_model_list = [
    ImageModel(network_name="EfficientNetB0",
               batch_size=64 * 64 * 16,
               num_epochs=1,
               optimizer_params={'lr': 0.005},
               dropout=0.7)]
image_models = ImageModels(image_model_list=image_model_list)

diamond_collector = run(images=images,
                        image_shape=image_shape,
                        labels=labels,
                        get_image_description=True,
                        is_augment_data=False,
                        image_augmentation_info=ImagesAugmentationInfo(aug_prop=0.1),
                        is_train_model=False, image_models=image_models,
                        is_post_model_analysis=False,
                        plot=True)
