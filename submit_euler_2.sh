#!/bin/bash

#SBATCH --output="/cluster/work/cvl/specta/experiment_logs/_tmp/%j.out"
#SBATCH --time=23:59:00
#SBATCH -n 1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=4096
#SBATCH --gpus=1 
#SBATCH --gpus=rtx_2080_ti:1
#SBATCH --gres=gpumem:10000m
#SBATCH --job-name=qdtrack

source /cluster/home/nipopovic/python_envs/qdtrack/bin/activate

# Trick to prevent crashes due to matplotlib
DISPLAY=
export DISPLAY

cd /cluster/project/cvl/specta/code/qdtrack

CONFIG_FILE=configs/bdd100k/qdtrack-frcnn_r50_fpn_12e_bdd100k.py
INPUT_FILE_OR_FOLDER=/cluster/work/cvl/specta/data/aegis_rides/2023-07-04_15-15-04-fdf08a6e/1bf99e7a_0.0-133.421.mp4
OUTPUT_FILE_OR_FOLDER=/cluster/work/cvl/specta/data/aegis_rides/2023-07-04_15-15-04-fdf08a6e/qd_tracker_output.mp4
CHECKPOINT_FILE=bdd100k.pth
FPS=30

python tools/inference.py --config ${CONFIG_FILE} --input ${INPUT_FILE_OR_FOLDER} --output ${OUTPUT_FILE_OR_FOLDER} --checkpoint ${CHECKPOINT_FILE} --fps ${FPS}