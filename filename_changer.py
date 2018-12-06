# this is to change the name of images from hashed names to their actual name
import csv
import os

# 1. Dictionary with key (hashed name of image) and value (desired name of image)
csv_file = 'cs50_2.csv'
# create dictionary
result = dict()
with open(csv_file, 'r') as fh:
    reader = csv.DictReader(fh, delimiter=',')
    # for row in csv, hashed name is the key and  row["Name"] is the value
    for row in reader:
        result[row["Photo-src"].split("/")[1]] = row["Name"]

# 2. Iterate through folder of images, if name matches key, change name to value
for image in os.listdir("/Users/marygao/Downloads/Harvard College Student Directory/"):
    full_path = os.path.join("/Users/marygao/Downloads/Harvard College Student Directory/", image)
    # if hashed image name matches key in result
    if image in result:
        # rename with actual name
        os.rename(full_path, os.path.join("/Users/marygao/Downloads/Harvard College Student Directory/", result[image]))
