import pandas as pd
import os
import numpy as np

recording_dir = '/srv/beegfs02/scratch/aegis_cvl/data/nikola/aegis_rides/2023-07-04_15-15-04-fdf08a6e'

world_t_path = os.path.join(recording_dir, 'world_timestamps.csv')
world_t = pd.read_csv(world_t_path)  
world_t = world_t['timestamp [ns]']

gaze_eye_path = os.path.join(recording_dir, 'gaze.csv')
gaze_eye = pd.read_csv(gaze_eye_path) 
gaze_eye = gaze_eye[['timestamp [ns]', 'gaze x [px]', 'gaze y [px]']] 

diff = np.abs(world_t.values[..., None] - gaze_eye['timestamp [ns]'].values[None, ...])
idx = np.argmin(diff, axis=1)

world_gaze_path = os.path.join(recording_dir, 'world_gaze.csv')
world_gaze = gaze_eye.iloc[idx].reset_index(drop=True)
world_gaze.to_csv(world_gaze_path)

a = 1