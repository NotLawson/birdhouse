import subprocess
import sys
import time
import threading
import io

def record():
    ffmpeg_proc = subprocess.Popen(
        [
            "ffmpeg",
            "-y",
            "-t","15",
            # --- Video Input Parameters ---
            "-fflags", "+genpts",
            "-f", "h264",
            "-r", "30",
            "-i", "pipe:0",
            "-c:v", "copy",
            "-movflags", "+frag_keyframe+empty_moov",
            "-f", "mp4",
            "pipe:1"
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr
    )
    time.sleep(0.5)

    if ffmpeg_proc.poll() is not None:
        raise Exception("!!FFmpeg failed to initialize. Check the errors above.!!")

    camera_proc = subprocess.Popen(
        [
            "rpicam-vid", 
            "-t", "0", 
            "--width", "1920", 
            "--height", "1080", 
            "--framerate", "30", 
            "--codec", "h264",
            "-o", "-",
        ], 
        stdout=ffmpeg_proc.stdin, 
        stderr=sys.stderr
    )

    mp4_buffer = io.BytesIO()
    def stream_reader(proc, buffer):
        try:
            while True:
                chunk = proc.stdout.read(4096)
                if not chunk:
                    break
                buffer.write(chunk)
        except Exception:
            pass
        finally:
            try:
                proc.stdout.close()
            except:
                pass
    reader_thread = threading.Thread(target=stream_reader, args=(ffmpeg_proc, mp4_buffer), daemon=True)
    reader_thread.start()

    try:
        while True:
            if ffmpeg_proc.poll() is not None:
                break
            if camera_proc.poll() is not None:
                break
            time.sleep(0.2)

    except KeyboardInterrupt:
        pass
    finally:
        camera_proc.terminate()
        camera_proc.wait()

        try:
            ffmpeg_proc.communicate(timeout=3)
        except subprocess.TimeoutExpired:
            ffmpeg_proc.kill()

    return mp4_buffer

if __name__ == "__main__":
    out = open("ouput.mp4", "wb")
    buf = record()
    buf.seek(0)
    out.write(buf.read())
    out.close()
    
