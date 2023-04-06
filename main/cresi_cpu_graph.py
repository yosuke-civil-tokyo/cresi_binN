import os
import json
import skimage.io
import numpy as np
import pandas as pd
import scipy.spatial
import networkx as nx
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
subprocess.call('python 04_skeletonize.py configs/dar_tutorial_cpu.json', shell=True)
subprocess.call('python 05_wkt_to_G.py configs/dar_tutorial_cpu.json', shell=True)

# inspect the output
gpickle_file = [z for z in os.listdir(os.path.join(results_dir, 'graphs')) if z.endswith('.gpickle')][0]
gpickle_path = os.path.join(results_dir, 'graphs', gpickle_file)
G0 = nx.read_gpickle(gpickle_path)
# _, _ = ox.plot_graph(G0, fig_height=12, fig_width=12)

subprocess.call('python 06_infer_speed.py configs/dar_tutorial_cpu.json', shell=True)

plot_graph_plus_im = __import__('08_plot_graph_plus_im')

# data
im_test = [z for z in os.listdir(test_final_dir) if z.endswith('.tif')][0]
im_test_path = os.path.join(test_final_dir, im_test)
im_test = skimage.io.imread(im_test_path).astype(np.uint8)

gpickle_file = [z for z in os.listdir(os.path.join(results_dir, 'graphs_speed')) if z.endswith('.gpickle')]
gpickle_path = os.path.join(results_dir, 'graphs_speed', gpickle_file[0])
G = nx.read_gpickle(gpickle_path)

# plot settings
fig_height=16
fig_width=16
node_color='green'
edge_color='#bfefff'   # lightblue
node_size=8
node_alpha=1
edge_color_key = 'inferred_lane_width'
edge_linewidth=1.3
edge_alpha=1
route_color='blue'
orig_dest_node_color=('green', 'red')
orig_dest_node_alpha=0.8
route_linewidth=5*edge_linewidth
orig_dest_node_size=400
invert_yaxis = True
dpi=150
plt.close()

# # print an edge
# edge_tmp = list(G.edges())[-1]
# print (edge_tmp, "random edge props:", G.edges([edge_tmp[0], edge_tmp[1]])) #G.edge[edge_tmp[0]][edge_tmp[1]])

# plot
color_dict, color_list = plot_graph_plus_im.make_color_dict_list(max_speed=41)
# _ = plot_graph_plus_im.plot_graph_pix(G, im=None, fig_height=fig_height, fig_width=fig_width,
#                            node_size=node_size, node_alpha=node_alpha, node_color=node_color,
#                            edge_linewidth=edge_linewidth, edge_alpha=edge_alpha,
#                            edge_color_key=edge_color_key, color_dict=color_dict,
#                            invert_yaxis=invert_yaxis,
#                            default_dpi=dpi,
#                            show=False, save=True)

_ = plot_graph_plus_im.plot_graph_pix(G, im=im_test, fig_height=fig_height, fig_width=fig_width, 
                           node_size=node_size, node_alpha=node_alpha, node_color=node_color, 
                           edge_linewidth=edge_linewidth, edge_alpha=edge_alpha,
                           edge_color_key=edge_color_key, color_dict=color_dict,
                           invert_yaxis=invert_yaxis, 
                           default_dpi=dpi,
                           show=True, save=True, filename='/opt/cresi/results/lane_width.png')
