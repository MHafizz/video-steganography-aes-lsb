import base64
from crypto_aes import AESCipher
from video_stego import VideoSteganography

class SecureVideoStego:
    def __init__(self, password: str):
        self.aes = AESCipher(password)
        self.stego = VideoSteganography()

    def hide_encrypted_message(self, video_path: str, message: str, output_video: str):
        # AES Encrypt
        encrypted = self.aes.encrypt(message.encode())
        encrypted_b64 = base64.b64encode(encrypted).decode()
        # Penanda sistem agar tidak salah baca video biasa
        payload = f"<<<START>>>{encrypted_b64}<<<END>>>"
        self.stego.encode(video_path, payload, output_video)

    def reveal_decrypted_message(self, video_path: str) -> str:
        hidden_data = self.stego.decode(video_path)

        # Validasi header pesan sistem
        if not hidden_data or not hidden_data.startswith("<<<START>>>"):
            return ""

        try:
            # Mengambil data di antara marker
            hidden_b64 = hidden_data.split("<<<START>>>")[1].split("<<<END>>>")[0]
            encrypted_data = base64.b64decode(hidden_b64.encode())
            decrypted = self.aes.decrypt(encrypted_data)
            return decrypted.decode('utf-8', errors="ignore")
        except:
            return ""