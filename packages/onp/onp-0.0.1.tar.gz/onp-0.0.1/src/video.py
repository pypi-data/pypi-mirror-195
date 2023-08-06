def extract_frames(video_path, output_dir, fps=5):
    os.makedirs(output_dir, exist_ok=True)
    cmd = ["ffmpeg", "-i", video_path, "-vf", "fps=%d" %
           fps, os.path.join(output_dir, "%d.jpg")]
    subprocess.call(cmd, stdout=open(os.devnull, 'wb'),
                    stderr=open(os.devnull, 'wb'))
