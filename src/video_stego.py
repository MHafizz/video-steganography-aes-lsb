import os
import cv2
import math
import shutil
from stegano import lsb
from subprocess import call, STDOUT

class VideoSteganography:
    def __init__(self, temp_dir="./temp"):
        self.temp_dir = temp_dir

    def _split_message(self, message: str, parts: int = 10):
        per_c = math.ceil(len(message) / parts)
        return [message[i:i+per_c] for i in range(0, len(message), per_c)]

    def extract_frames(self, video_path: str):
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        cap = cv2.VideoCapture(video_path)
        count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imwrite(os.path.join(self.temp_dir, f"{count}.png"), frame)
            count += 1
        cap.release()
        return count

    def encode(self, video_path: str, message: str, output_video="Embedded_Video.avi"):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()

        total_frames = self.extract_frames(video_path)
        split_msg = self._split_message(message, total_frames)

        for i, chunk in enumerate(split_msg[:total_frames]):
            frame_path = os.path.join(self.temp_dir, f"{i}.png")
            secret = lsb.hide(frame_path, chunk)
            secret.save(frame_path)

        # Tambahkan penanda akhir
        last_frame_path = os.path.join(self.temp_dir, f"{min(len(split_msg), total_frames)-1}.png")
        secret = lsb.hide(last_frame_path, split_msg[-1] + "<ENDMSG>")
        secret.save(last_frame_path)

        # Audio & Rebuild
        call(["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", f"{self.temp_dir}/audio.mp3", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)
        call(["ffmpeg", "-framerate", str(fps), "-i", f"{self.temp_dir}/%d.png", "-c:v", "ffv1", f"{self.temp_dir}/temp_video.avi", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)
        call(["ffmpeg", "-i", f"{self.temp_dir}/temp_video.avi", "-i", f"{self.temp_dir}/audio.mp3", "-codec", "copy", output_video, "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)

        self.cleanup()

    def decode(self, video_path: str) -> str:
        total_frames = self.extract_frames(video_path)
        if total_frames == 0:
            self.cleanup()
            return ""

        # --- FIX: Early Exit jika frame pertama kosong ---
        first_frame = os.path.join(self.temp_dir, "0.png")
        try:
            first_check = lsb.reveal(first_frame)
            if not first_check:
                self.cleanup()
                return ""
        except:
            self.cleanup()
            return ""

        secret_msg = []
        for i in range(total_frames):
            frame_path = os.path.join(self.temp_dir, f"{i}.png")
            try:
                msg = lsb.reveal(frame_path)
                if msg:
                    secret_msg.append(msg)
                    if "<ENDMSG>" in msg: break
                else: break
            except: continue
        
        message = ''.join(secret_msg).replace("<ENDMSG>", "")
        self.cleanup()
        return message

    def cleanup(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)