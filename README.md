# Road info from Satellite Imagery
## Note
This repository is based on [SpaceNet repository](https://github.com/avanetten/cresi), and for getting visual information of road network from satellite imagery.  
We assume that data created on this repository is utilized in other projects such as aggregating vehicle speed or disaster information on road. In addition, it's better to modify the road network by incorporating the information from other network source (OpenStreetMap is most common). This repository offers only visible information, so occluded road is ignored.  

## How to
Mainly the required process is similar to the original repository (see 'README_cresi.md), but docker environment, main code and function include some changes, so follow the procedure below.  
1. Make environment  
    After ```git clone``` this repository, put your RGB satellite image (.tif file) on 'test_imagery/dar/PS-MS'. Now you can run  
    ```
    docker build -t cresi ./

    nvidia-docker run -it cresi
    ```
    . (cpu is enough for a certain size of satellite image (~15min), but if you process multiple images, I recommend you use gpu)  
2. Run code  
    Now you are in the docker env, so press 'P, Q' with 'control' to dettach from the env. Run the following.  
    ```
    sudo docker exec -u 1000 cresi python /opt/cresi/main/cresi_cpu_testdata.py -ulx [top left longutude] -uly [top left latitude] -lrx [bottom right longitude] -lry [bottom right longitude]  

    sudo docker exec -u 1000 cresi python /opt/cresi/main/cresi_cpu_detect.py  

    sudo docker exec -u 1000 cresi python /opt/cresi/main/cresi_cpu_graph.py
    ```
3. Get output  
    Output files are below. You can copy from docker env by 
    ```
    docker cp cresi:[data_path] [folder_path]
    ```
    Grayscale road mask images. '_qua' is 4^2 times smaller image. 
    ```
    cresi:/opt/cresi/results/dar_tutorial_cpu/mask_for_lane/mask_f.tif
    cresi:/opt/cresi/results/dar_tutorial_cpu/mask_for_lane/mask_qua_f.tif
    ```
    Road network data. edge and node data are for simulation. pix_to_edge.csv is for aggregating other information to road edge.  
    ```
    cresi:/opt/cresi/results/pix_to_edge.csv
    cresi:/opt/cresi/results/edge_for_sim.csv
    cresi:/opt/cresi/results/node_for_sim.csv
    ```

## What is new?  
These processes are the extensions from the original repository.  

- smoothing and lower the effect of shadows/flopped buildings in the detected road area by post-process
- output road mask image in the format of geo-referrenced '.tif'
- link each road mask pixel to 'edge' of road network
- calculate road width from road mask and set it as an edge feature
- output road network as 'edge & node' style
- conda environment's libraries are checked again and some are changed (2022.11.20)