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


def main(video_path, output_path, num_processes):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    frames_per_process = total_frames // num_processes
    pool = Pool(processes=num_processes)

    for i in range(num_processes):
        start_frame = i * frames_per_process
        if i == num_processes - 1:
            end_frame = total_frames
        else:
            end_frame = start_frame + frames_per_process

        pool.apply_async(extract_frames, args=(video_path, output_path, start_frame, end_frame))

    pool.close()
    pool.join()


if __name__ == "__main__":
    main('../SourceFiles/VideoEssai.mp4', 'Result', 4)
