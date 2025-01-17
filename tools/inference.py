import os
import os.path as osp
import tempfile
from argparse import ArgumentParser
import json

import mmcv

from qdtrack.apis import inference_model, init_model


def main():
    parser = ArgumentParser()
    parser.add_argument('--config', help='config file', 
                        default='configs/aegis/qdtrack-frcnn_r50_fpn_12e_aegis.py')
    parser.add_argument('--input', help='input video file or folder', 
                        default='/srv/beegfs02/scratch/aegis_cvl/data/nikola/aegis_rides/2023-07-04_15-15-04-fdf08a6e/1bf99e7a_0.0-133.421.mp4')
    parser.add_argument('--output', help='output video file (mp4 format) or folder', 
                        default='/srv/beegfs02/scratch/aegis_cvl/data/nikola/aegis_rides/2023-07-04_15-15-04-fdf08a6e/qd_tracker_output.mp4')
    parser.add_argument('--checkpoint', help='checkpoint file', 
                        default='/srv/beegfs02/scratch/aegis_cvl/data/nikola/code/qdtrack-frcnn_r50_fpn_12e_bdd100k-13328aed.pth')
    parser.add_argument(
        '--score-thr',
        type=float,
        default=0.0,
        help='The threshold of score to filter bboxes.')
    parser.add_argument(
        '--device', default='cuda:0', help='device used for inference')
    parser.add_argument(
        '--show',
        action='store_true',
        help='whether show the results on the fly')
    parser.add_argument(
        '--backend',
        choices=['cv2', 'plt'],
        default='cv2',
        help='the backend to visualize the results')
    parser.add_argument('--fps', help='FPS of the output video', default=20)
    args = parser.parse_args()
    assert args.output or args.show
    # load images
    if osp.isdir(args.input):
        imgs = sorted(
            filter(lambda x: x.endswith(('.jpg', '.png', '.jpeg')),
                   os.listdir(args.input)),
            key=lambda x: int(x.split('.')[0][-7:]))  # may cause bug
        IN_VIDEO = False
    else:
        imgs = mmcv.VideoReader(args.input)
        IN_VIDEO = True
    # define output
    if args.output is not None:
        if args.output.endswith('.mp4'):
            OUT_VIDEO = True
            out_dir = tempfile.TemporaryDirectory()
            out_path = out_dir.name
            _out = args.output.rsplit(os.sep, 1)
            if len(_out) > 1:
                os.makedirs(_out[0], exist_ok=True)
        else:
            OUT_VIDEO = False
            out_path = args.output
            os.makedirs(out_path, exist_ok=True)

    fps = args.fps
    if args.show or OUT_VIDEO:
        if fps is None and IN_VIDEO:
            fps = imgs.fps
        if not fps:
            raise ValueError('Please set the FPS for the output video.')
        fps = int(fps)

    # build the model from a config file and a checkpoint file
    model = init_model(args.config, args.checkpoint, device=args.device)

    prog_bar = mmcv.ProgressBar(len(imgs))
    # test and show/save the image
    tracking_res = []
    for i, img in enumerate(imgs):
        # if i == 100:
        #     break        
        if i == 60:
            a = 1
        if isinstance(img, str):
            img = osp.join(args.input, img)
        result = inference_model(model, img, frame_id=i)

        track_res_i = [result['track_results'][j].tolist() for j, _ in enumerate(result['track_results'])]
        tracking_res.append(track_res_i)

        if args.output is not None:
            if IN_VIDEO or OUT_VIDEO:
                out_file = osp.join(out_path, f'{i:06d}.jpg')
            else:
                out_file = osp.join(out_path, img.rsplit(os.sep, 1)[-1])
        else:
            out_file = None
        model.show_result(
            img,
            result,
            score_thr=args.score_thr,
            show=args.show,
            wait_time=int(1000. / fps) if fps else 0,
            out_file=out_file,
            backend=args.backend)
        prog_bar.update()

    output_dir = os.path.dirname(args.output)
    output_json = os.path.join(output_dir, 'track_results.json')
    with open(output_json, 'w') as fh:
        json.dump(tracking_res, fh)

    if args.output and OUT_VIDEO:
        print(f'making the output video at {args.output} with a FPS of {fps}')
        mmcv.frames2video(out_path, args.output, fps=fps, fourcc='mp4v')
        out_dir.cleanup()


if __name__ == '__main__':
    main()
