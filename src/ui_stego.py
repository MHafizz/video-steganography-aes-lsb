import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from main import SecureVideoStego

class VideoStegoUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Steganografi - LSB + AES")
        self.root.geometry("600x600") # Ukuran sedikit diperbesar untuk menampung widget baru

        self.notebook = ttk.Notebook(root)
        self.tab_sisip = ttk.Frame(self.notebook)
        self.tab_ekstrak = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_sisip, text="Sisip Pesan")
        self.notebook.add(self.tab_ekstrak, text="Ekstrak Pesan")
        self.notebook.pack(expand=True, fill="both")

        self.build_tab_sisip()
        self.build_tab_ekstrak()

    def build_tab_sisip(self):
        frame = self.tab_sisip
        frame.columnconfigure(1, weight=1)

        # Bagian Input Video
        ttk.Label(frame, text="Input Video Asli:").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.file_video_asli = ttk.Entry(frame, width=50)
        self.file_video_asli.grid(row=0, column=1, sticky="w", padx=5)
        ttk.Button(frame, text="Cari", command=self.load_video_asli).grid(row=0, column=2, padx=5)

        # Pilihan Tipe Input Pesan
        ttk.Label(frame, text="Mode Pesan:").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        self.msg_input_type = tk.StringVar(value="manual")
        
        msg_type_frame = ttk.Frame(frame)
        msg_type_frame.grid(row=1, column=1, columnspan=2, sticky="w", padx=5)
        ttk.Radiobutton(msg_type_frame, text="Manual", variable=self.msg_input_type, value="manual", command=self.toggle_input_fields).pack(side="left")
        ttk.Radiobutton(msg_type_frame, text="File .txt", variable=self.msg_input_type, value="file", command=self.toggle_input_fields).pack(side="left", padx=10)

        # Input Manual (ScrolledText)
        ttk.Label(frame, text="Pesan Manual:").grid(row=2, column=0, sticky="nw", padx=10, pady=5)
        self.msg_manual = scrolledtext.ScrolledText(frame, width=50, height=5)
        self.msg_manual.grid(row=2, column=1, columnspan=2, sticky="w", padx=10, pady=5)

        # Input File Txt
        ttk.Label(frame, text="File Pesan (.txt):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.file_pesan_txt = ttk.Entry(frame, width=40)
        self.file_pesan_txt.grid(row=3, column=1, sticky="w", padx=5)
        self.btn_cari_txt = ttk.Button(frame, text="Cari File", command=self.load_txt_pesan)
        self.btn_cari_txt.grid(row=3, column=2, padx=5)

        # Password
        ttk.Label(frame, text="Password AES:").grid(row=4, column=0, sticky="w", padx=10, pady=10)
        self.password_sisip = ttk.Entry(frame, width=40, show="*")
        self.password_sisip.grid(row=4, column=1, sticky="w", padx=5)

        ttk.Button(frame, text="Mulai Sisipkan & Simpan", command=self.do_sisip).grid(row=5, column=1, sticky="w", pady=15, padx=5)
        
        # Inisialisasi status field
        self.toggle_input_fields()

    def build_tab_ekstrak(self):
        frame = self.tab_ekstrak
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Input Video Stego:").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.file_video_decode = ttk.Entry(frame, width=50)
        self.file_video_decode.grid(row=0, column=1, sticky="w", padx=5)
        ttk.Button(frame, text="Cari", command=self.load_video_decode).grid(row=0, column=2, padx=5)

        ttk.Label(frame, text="Password AES:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.password_ekstrak = ttk.Entry(frame, width=40, show="*")
        self.password_ekstrak.grid(row=1, column=1, sticky="w", padx=5)

        # Pilihan Output Ekstraksi
        ttk.Label(frame, text="Output Hasil:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.output_type = tk.StringVar(value="ui")
        out_frame = ttk.Frame(frame)
        out_frame.grid(row=2, column=1, sticky="w", padx=5)
        ttk.Radiobutton(out_frame, text="Tampilkan di UI", variable=self.output_type, value="ui").pack(side="left")
        ttk.Radiobutton(out_frame, text="Simpan ke .txt", variable=self.output_type, value="file").pack(side="left", padx=10)

        self.output_box = scrolledtext.ScrolledText(frame, width=50, height=8)
        self.output_box.grid(row=3, column=1, columnspan=2, sticky="w", padx=10, pady=10)

        ttk.Button(frame, text="Ekstrak Pesan", command=self.do_ekstrak).grid(row=4, column=1, sticky="w", pady=5)

    # --- LOGIKA HELPER ---

    def toggle_input_fields(self):
        """Mengatur field mana yang aktif berdasarkan pilihan RadioButton"""
        if self.msg_input_type.get() == "manual":
            self.msg_manual.config(state=tk.NORMAL, bg="white")
            self.file_pesan_txt.config(state=tk.DISABLED)
            self.btn_cari_txt.config(state=tk.DISABLED)
        else:
            self.msg_manual.delete("1.0", tk.END)
            self.msg_manual.config(state=tk.DISABLED, bg="#f0f0f0")
            self.file_pesan_txt.config(state=tk.NORMAL)
            self.btn_cari_txt.config(state=tk.NORMAL)

    def load_video_asli(self):
        path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi")])
        if path: 
            self.file_video_asli.delete(0, tk.END)
            self.file_video_asli.insert(0, path)

    def load_txt_pesan(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            self.file_pesan_txt.delete(0, tk.END)
            self.file_pesan_txt.insert(0, path)

    def load_video_decode(self):
        path = filedialog.askopenfilename(filetypes=[("Video Files", "*.avi *.mp4")])
        if path: 
            self.file_video_decode.delete(0, tk.END)
            self.file_video_decode.insert(0, path)

    def do_sisip(self):
        try:
            video_path = self.file_video_asli.get()
            password = self.password_sisip.get()
            
            if not video_path or not password:
                messagebox.showerror("Error", "Isi video dan password terlebih dahulu!")
                return

            # Ambil pesan berdasarkan mode
            if self.msg_input_type.get() == "manual":
                message = self.msg_manual.get("1.0", tk.END).strip()
            else:
                path_txt = self.file_pesan_txt.get()
                if not path_txt:
                    messagebox.showerror("Error", "Pilih file .txt terlebih dahulu!")
                    return
                with open(path_txt, "r", encoding="utf-8") as f:
                    message = f.read()

            if not message:
                messagebox.showerror("Error", "Pesan tidak boleh kosong!")
                return

            output_path = filedialog.asksaveasfilename(
                defaultextension=".avi",
                filetypes=[("AVI Video", "*.avi")],
                title="Simpan Video Hasil Steganografi"
            )
            
            if not output_path:
                return

            stego = SecureVideoStego(password)
            stego.hide_encrypted_message(video_path, message, output_path)
            
            messagebox.showinfo("Berhasil", f"Pesan berhasil disisipkan!\nFile disimpan di: {output_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def do_ekstrak(self):
        try:
            video_path = self.file_video_decode.get()
            password = self.password_ekstrak.get()
            
            if not video_path or not password:
                messagebox.showerror("Error", "Isi video dan password!")
                return

            stego = SecureVideoStego(password)
            message = stego.reveal_decrypted_message(video_path)

            if not message:
                messagebox.showwarning("Gagal", "Video tidak mengandung pesan rahasia atau password salah.")
                return

            # Kosongkan output box sesuai permintaan
            self.output_box.delete("1.0", tk.END)

            if self.output_type.get() == "ui":
                self.output_box.insert(tk.END, message)
            else:
                # Mode Simpan ke File .txt
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text Files", "*.txt")],
                    title="Simpan Pesan Rahasia"
                )
                if save_path:
                    with open(save_path, "w", encoding="utf-8") as f:
                        f.write(message)
                    messagebox.showinfo("Berhasil", f"Pesan berhasil disimpan ke: {save_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoStegoUI(root)
    root.mainloop()