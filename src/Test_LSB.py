import os
import cv2
import shutil
from stegano import lsb


class VideoLSBExtractor:
    def __init__(self, temp_dir="./temp_extract"):
        self.temp_dir = temp_dir

    def extract_frames(self, video_path: str) -> int:
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

    def decode_to_txt(self, video_path: str, output_txt="extracted_message.txt") -> str:
        """
        Mengekstraksi pesan LSB dari video dan menyimpannya ke file TXT
        """
        total_frames = self.extract_frames(video_path)

        if total_frames == 0:
            self.cleanup()
            return ""

        # Validasi awal
        first_frame = os.path.join(self.temp_dir, "0.png")
        try:
            first_msg = lsb.reveal(first_frame)
            if not first_msg:
                self.cleanup()
                return ""
        except Exception:
            self.cleanup()
            return ""

        secret_parts = []

        for i in range(total_frames):
            frame_path = os.path.join(self.temp_dir, f"{i}.png")
            try:
                msg = lsb.reveal(frame_path)
                if msg:
                    secret_parts.append(msg)
                    if "<ENDMSG>" in msg:
                        break
                else:
                    break
            except Exception:
                continue

        message = "".join(secret_parts).replace("<ENDMSG>", "")

        # Simpan ke file TXT
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(message)

        self.cleanup()
        return message

    def cleanup(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


extractor = VideoLSBExtractor()
extractor.decode_to_txt(
    video_path="TestEkstraksiLSB.avi",
    output_txt="hasil_ekstraksi.txt"
)
