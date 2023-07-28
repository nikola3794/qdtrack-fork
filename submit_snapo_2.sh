#!/bin/bash

#SBATCH --output="/srv/beegfs02/scratch/aegis_cvl/data/nikola/aegis_rides/%j.out"
#SBATCH --gpus-per-node=2
#SBATCH --job-name=qdtrack

#conda activate qdtrack

# Trick to prevent crashes due to matplotlib
DISPLAY=
export DISPLAY

cd /srv/beegfs02/scratch/aegis_cvl/data/nikola/code/qdtrack-fork

CONFIG_FILE=configs/aegis/qdtrack-frcnn_r50_fpn_12e_aegis.py
INPUT_FILE_OR_FOLDER=/srv/beegfs02/scratch/aegis_cvl/data/nikola/aegis_rides/2023-07-04_15-15-04-fdf08a6e/1bf99e7a_0.0-133.421.mp4
OUTPUT_FILE_OR_FOLDER=/srv/beegfs02/scratch/aegis_cvl/data/nikola/aegis_rides/2023-07-04_15-15-04-fdf08a6e/qd_tracker_output.mp4
CHECKPOINT_FILE=/srv/beegfs02/scratch/aegis_cvl/data/nikola/code/qdtrack-frcnn_r50_fpn_12e_bdd100k-13328aed.pth
FPS=30

/scratch_net/snapo_second/nipopovic/apps/miniconda3/envs/qdtrack/bin/python tools/inference.py --config ${CONFIG_FILE} --input ${INPUT_FILE_OR_FOLDER} --output ${OUTPUT_FILE_OR_FOLDER} --checkpoint ${CHECKPOINT_FILE} --fps ${FPS}