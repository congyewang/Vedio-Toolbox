import os
import subprocess


def get_duration(path: str) -> float:
    """
    Use ffprobe to get the duration of a video file in seconds.
    Raises RuntimeError if ffprobe fails or output cannot be parsed.

    Args:
        path (str): Path to the video file.

    Returns:
        float: Duration of the video in seconds.

    Raises:
        RuntimeError: If ffprobe fails or output cannot be parsed.
    """
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            path,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        raise RuntimeError(
            f"Could not parse duration from ffprobe output: {result.stdout}"
        )


def split_video(path: str, max_duration: int = 5400) -> None:
    """
    Split a video into segments of up to max_duration seconds using ffmpeg stream copy.
    If video is shorter than max_duration, it will still be renamed with _part000 suffix.

    Args:
        path (str): Path to the video file to split.
        max_duration (int): Maximum duration of each segment in seconds (default is 5400 seconds, i.e., 90 minutes).

    Raises:
        subprocess.CalledProcessError: If ffmpeg fails to execute.
    """
    dirname = os.path.dirname(path)
    basename = os.path.splitext(os.path.basename(path))[0]

    # 检查视频时长
    try:
        duration = get_duration(path)
    except RuntimeError as e:
        raise e

    if duration <= max_duration:
        # 视频时长小于等于max_duration，直接重命名为_part000
        output_path = os.path.join(dirname, f"{basename}_part000.mp4")
        os.rename(path, output_path)
    else:
        # 视频时长大于max_duration，按原逻辑分割
        output_pattern = os.path.join(dirname, f"{basename}_part%03d.mp4")
        cmd = [
            "ffmpeg",
            "-i",
            path,
            "-c",
            "copy",
            "-map",
            "0",
            "-f",
            "segment",
            "-segment_time",
            str(max_duration),
            "-reset_timestamps",
            "1",
            output_pattern,
        ]
        subprocess.run(cmd, check=True)


def cut_videos(root_dir: str) -> None:
    """
    Walk through root_dir, find all .mp4 files, and split those longer than 90 minutes.

    Args:
        root_dir (str): Root directory to search for mp4 files.

    Raises:
        RuntimeError: If ffprobe fails to get the duration of a video.
        subprocess.CalledProcessError: If ffmpeg fails to split a video.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            if file.lower().endswith(".mp4"):
                full_path = os.path.join(dirpath, file)
                try:
                    duration = get_duration(full_path)
                except Exception as e:
                    print(f"[ERROR] {full_path}: {e}")
                    continue

                minutes = duration / 60
                if duration > 90 * 60:
                    print(f"[INFO] Splitting '{full_path}' ({minutes:.2f} minutes)...")
                    try:
                        split_video(full_path)
                    except subprocess.CalledProcessError as e:
                        print(f"[ERROR] Failed to split '{full_path}': {e}")
                else:
                    print(f"[SKIP] '{full_path}' is only {minutes:.2f} minutes long.")
