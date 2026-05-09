import subprocess


def get_video_duration_from_path(path):
    ffprobe_path = r"C:\Users\User\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffprobe.exe"  # 🔥 SHU YERNI TO‘G‘RILA

    try:
        result = subprocess.run(
            [
                ffprobe_path, 
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print("OUTPUT:", result.stdout)
        print("ERROR:", result.stderr)

        if not result.stdout.strip():
            return None

        return float(result.stdout.strip())

    except Exception as e:
        print("Duration error:", e)
        return None