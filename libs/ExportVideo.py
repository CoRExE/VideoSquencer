from multiprocessing import Pool
from tqdm import tqdm
import cv2


def extract_frames(video_path, output_path, start_frame, end_frame):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    for i in tqdm(range(start_frame, end_frame), desc="Processing frames"):
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imwrite(f'{output_path}/frame{i}.jpg', frame)

    cap.release()


def execute(input_path, output_path, num_frames, num_processes):
    cap = cv2.VideoCapture(input_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    frames_to_process = total_frames if num_frames == 'all' else min(num_frames, total_frames)

    frames_per_process = frames_to_process // num_processes

    # Adjust the last process to handle any remaining frames
    frames_for_last_process = frames_per_process + (frames_to_process % num_processes)

    pool = Pool(processes=num_processes)

    for i in range(num_processes):
        start_frame = i * frames_per_process
        end_frame = start_frame + frames_per_process if i < num_processes - 1 else start_frame + frames_for_last_process
        end_frame = min(end_frame, total_frames)  # Ensure the end frame is not beyond the total frame count

        pool.apply_async(extract_frames, args=(input_path, output_path, start_frame, end_frame))

    pool.close()
    pool.join()
