import os
import json
import argparse
import skimage.io
import matplotlib.pyplot as plt
import subprocess
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('-ulx', type=float, default=139.775)
parser.add_argument('-uly', type=float, default=35.683333)
parser.add_argument('-lrx', type=float, default=139.8375)
parser.add_argument('-lry', type=float, default=35.641667)
args = parser.parse_args()

convert = True
cresi_dir = '/opt/cresi'
src_dir = os.path.join(cresi_dir, 'cresi')
config_dir = os.path.join(cresi_dir, 'cresi/configs')
weight_dir = os.path.join(cresi_dir, 'results/aws_weights')
test_im_raw_dir = os.path.join(cresi_dir, 'test_imagery/dar/PS-MS')
test_im_clip_dir = os.path.join(cresi_dir, 'test_imagery/dar/PS-MS_clip')
test_final_dir = os.path.join(cresi_dir, 'test_imagery/dar/PS-RGB_8bit_clip')
results_root_dir = os.path.join(cresi_dir, 'results')
results_dir = os.path.join(results_root_dir, 'dar_tutorial_cpu')
mask_pred_dir = os.path.join(results_dir, 'folds')
mask_stitched_dir = os.path.join(results_dir, 'stitched/mask_norm')
# make dirs
for d in [weight_dir, test_im_raw_dir, test_im_clip_dir, test_final_dir]:
    os.makedirs(d, exist_ok=True)


# Clip the image extent
ulx, uly, lrx, lry = (args.ulx, args.uly, args.lrx, args.lry)

im_name = [z for z in os.listdir(test_im_raw_dir) if z.endswith('.tif')][0]
print("im_name:", im_name)
test_im_raw = os.path.join(test_im_raw_dir, im_name)
test_im_clip = os.path.join(test_im_clip_dir, im_name.split('.tif')[0] + '_clip.tif')
print("output_file:", test_im_clip)

# subprocess.call('gdalinfo {}'.format(test_im_raw).split())
subprocess.call('gdal_translate -projwin {} {} {} {} {} {}'.format(ulx, uly, lrx, lry, test_im_raw, test_im_clip).split())

# Convert 16-bit multispectral test data to 8-bit RGB
os.chdir('/opt/cresi/cresi/data_prep/')
create_8bit_images = __import__('create_8bit_images')

if convert:
    create_8bit_images.dir_to_8bit(test_im_clip_dir, test_final_dir,
                                  command_file_loc='',
                                  rescale_type="perc",
                                  percentiles=[2,98],
                                  band_order=[3,2,1])
else:
    shutil.rmtree(test_final_dir)
    shutil.copytree(test_im_clip_dir, test_final_dir)

# display our test image
fig_width, fig_height = 16, 16
im_test_name = [z for z in os.listdir(test_final_dir) if z.endswith('.tif')][0]
im_test_path = os.path.join(test_final_dir, im_test_name)
im_test = skimage.io.imread(im_test_path)

fig, ax = plt.subplots(figsize=(fig_width, fig_height))
_ = ax.imshow(im_test)
_ = ax.set_title(im_test_name)

