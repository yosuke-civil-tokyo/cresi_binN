import os
import json
import skimage.io
import matplotlib.pyplot as plt
import subprocess

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


os.chdir(src_dir)
subprocess.call('python 02_eval.py configs/dar_tutorial_cpu.json', shell=True)


# inspect
"""
mask_pred_file = 'fold0_0__19OCT06021423-S2AS-011595197010_01_P001_clip__0__0__1300__1300__2000__2000.tif'
mask_pred_path = os.path.join(mask_pred_dir, mask_pred_file)
mask_pred = skimage.io.imread(mask_pred_path)
print("mask_pred.shape:", mask_pred.shape)
print("mask_pred.dtype:", mask_pred.dtype)

# plot all layers
fig, axes = plt.subplots(2, 4, figsize=(16, 9))
for i, ax in enumerate(axes.flatten()):
    if i < (len(axes.flatten()) - 1):
        title = 'Mask Channel {}'.format(str(i))
    else:
        title = 'Aggregate'
    ax.imshow(mask_pred[i,:,:])
    ax.set_title(title)
"""

os.chdir(src_dir)
subprocess.call('python 03b_stitch.py  configs/dar_tutorial_cpu.json', shell=True)


"""
# Inspect the output
plot_all_layers = False
mask_pred_file = [z for z in os.listdir(mask_stitched_dir) if z.endswith('.tif')][0]
mask_pred_path = os.path.join(mask_stitched_dir, mask_pred_file)
mask_pred = skimage.io.imread(mask_pred_path)
print("mask_pred.shape:", mask_pred.shape)

# plot final layer
fig_width, fig_height = 12, 12
fig, ax = plt.subplots(figsize=(fig_width, fig_height))
_ = ax.imshow(mask_pred[-1,:,:])
_ = ax.set_title('Aggregate - ' + mask_pred_file)

# plot all layers (optional)
if plot_all_layers:
    fig, axes = plt.subplots(2, 4, figsize=(20, 11))
    for i, ax in enumerate(axes.flatten()):
        if i < (len(axes.flatten()) - 1):
            title = 'Mask Channel {}'.format(str(i))
        else:
            title = 'Aggregate'
        ax.imshow(mask_pred[i,:,:])
        ax.set_title(title)
"""
