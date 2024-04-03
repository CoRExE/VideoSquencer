import random
from multiprocessing import Pool
import cv2


def extract_frames(video_path, output_path, start_frame, end_frame):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    i = start_frame
    while i < end_frame:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imwrite(f'{output_path}/frame{"%06d" % i}.jpg', frame)
        i += 1

    cap.release()


def extract_selected_frames(video_path, output_path, selected_frames):
    for frame_number in selected_frames:
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(f'{output_path}/frame{"%06d" % frame_number}.jpg', frame)
        cap.release()


def execute(input_path, output_path, num_frames, num_processes):
    cap = cv2.VideoCapture(input_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    if total_frames == 0:
        return
    elif num_frames == 'all':
        frames_to_process = total_frames
    else:
        frames_to_process = num_frames
        selected_frames = random.sample(range(total_frames), num_frames)

    frames_per_process = frames_to_process // num_processes

    # Adjust the last process to handle any remaining frames
    frames_for_last_process = frames_per_process + (frames_to_process % num_processes)

    pool = Pool(processes=num_processes)

    for i in range(num_processes):
        start_frame = i * frames_per_process
        end_frame = start_frame + frames_per_process if i < num_processes - 1 else start_frame + frames_for_last_process
        end_frame = min(end_frame, total_frames)  # Ensure the end frame is not beyond the total frame count

        if num_frames == 'all':
            pool.apply_async(extract_frames, args=(input_path, output_path, start_frame, end_frame))
        else:
            pool.apply_async(extract_selected_frames, args=(input_path, output_path, selected_frames))

    pool.close()
    pool.join()
