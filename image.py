import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import cv2
import numpy as np
import json
import os
import hashlib
from rembg import remove
import io
import threading

class ImageEditorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FEDXI - PhotoPro Image Editor")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0a0e27")
        
        self.current_user = None
        self.users_file = "user.txt"
        self.current_image = None
        self.original_image = None
        self.display_image = None
        
        # Load users database
        self.load_users()
        
        # Show login screen
        self.show_login_screen()
        
    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
    
    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def show_loading(self, message="Processing..."):
        self.loading_label = tk.Label(self.canvas_frame, text=message,
                                     font=("Helvetica", 14, "bold"), 
                                     fg="#00f0ff", bg="#1a1f3a",
                                     padx=30, pady=20)
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")
        self.root.update()
    
    def hide_loading(self):
        if hasattr(self, 'loading_label'):
            self.loading_label.destroy()
    
    def show_login_screen(self):
        self.clear_window()
        
        # Container frame
        container = tk.Frame(self.root, bg="#0a0e27")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title = tk.Label(container, text="FEDXI", font=("Helvetica", 42, "bold"), 
                        fg="#00f0ff", bg="#0a0e27")
        title.pack(pady=20)
        
        subtitle = tk.Label(container, text="Advanced Image Editor", 
                           font=("Helvetica", 14), fg="#7a8bff", bg="#0a0e27")
        subtitle.pack(pady=(0, 40))

        subtitle = tk.Label(container, text="by farildev", 
                           font=("Helvetica", 14), fg="#7a8bff", bg="#0a0e27")
        subtitle.pack(pady=(0, 40))
        
        # Login frame
        login_frame = tk.Frame(container, bg="#1a1f3a", bd=0)
        login_frame.pack(padx=60, pady=20)
        
        # Username
        tk.Label(login_frame, text="Username", font=("Helvetica", 12), 
                fg="#ffffff", bg="#1a1f3a").grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))
        
        self.username_entry = tk.Entry(login_frame, font=("Helvetica", 12), 
                                      bg="#0a0e27", fg="#ffffff", 
                                      insertbackground="#00f0ff", bd=0, 
                                      highlightthickness=2, highlightbackground="#00f0ff",
                                      highlightcolor="#7a8bff", width=30)
        self.username_entry.grid(row=1, column=0, padx=20, pady=(0, 15))
        
        # Password
        tk.Label(login_frame, text="Password", font=("Helvetica", 12), 
                fg="#ffffff", bg="#1a1f3a").grid(row=2, column=0, sticky="w", padx=20, pady=(10, 5))
        
        self.password_entry = tk.Entry(login_frame, font=("Helvetica", 12), 
                                      bg="#0a0e27", fg="#ffffff", show="●",
                                      insertbackground="#00f0ff", bd=0,
                                      highlightthickness=2, highlightbackground="#00f0ff",
                                      highlightcolor="#7a8bff", width=30)
        self.password_entry.grid(row=3, column=0, padx=20, pady=(0, 25))
        
        # Buttons frame
        btn_frame = tk.Frame(login_frame, bg="#1a1f3a")
        btn_frame.grid(row=4, column=0, pady=(10, 20))
        
        login_btn = tk.Button(btn_frame, text="LOGIN", font=("Helvetica", 11, "bold"),
                             bg="#00f0ff", fg="#0a0e27", bd=0, padx=40, pady=12,
                             cursor="hand2", command=self.login)
        login_btn.pack(side="left", padx=5)
        
        register_btn = tk.Button(btn_frame, text="REGISTER", font=("Helvetica", 11, "bold"),
                                bg="#7a8bff", fg="#ffffff", bd=0, padx=40, pady=12,
                                cursor="hand2", command=self.register)
        register_btn.pack(side="left", padx=5)
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.login())
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Password dan username salah kocag goblok")
            return
        
        hashed_pw = self.hash_password(password)
        
        if username in self.users and self.users[username] == hashed_pw:
            self.current_user = username
            self.show_editor_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if username in self.users:
            messagebox.showerror("Error", "Username already exists")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        self.users[username] = self.hash_password(password)
        self.save_users()
        messagebox.showinfo("Success", "Registration successful! Please login.")
    
    def show_editor_screen(self):
        self.clear_window()
        
        # Top bar
        top_bar = tk.Frame(self.root, bg="#1a1f3a", height=60)
        top_bar.pack(fill="x", side="top")
        
        tk.Label(top_bar, text=f"Fedxi", 
                font=("Helvetica", 16, "bold"), fg="#00f0ff", 
                bg="#1a1f3a").pack(side="left", padx=20, pady=15)
        
        # Status label
        self.status_label = tk.Label(top_bar, text="Ready", 
                                    font=("Helvetica", 10), fg="#7fff7f", 
                                    bg="#1a1f3a")
        self.status_label.pack(side="left", padx=20)
        
        tk.Label(top_bar, text=f"User: {self.current_user}", 
                font=("Helvetica", 11), fg="#7a8bff", 
                bg="#1a1f3a").pack(side="right", padx=20)
        
        logout_btn = tk.Button(top_bar, text="Logout", font=("Helvetica", 10),
                              bg="#ff4757", fg="#ffffff", bd=0, padx=20, pady=8,
                              cursor="hand2", command=self.logout)
        logout_btn.pack(side="right", padx=10)
        
        # Main container
        main_container = tk.Frame(self.root, bg="#0a0e27")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel - Tools
        left_panel = tk.Frame(main_container, bg="#1a1f3a", width=280)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        tk.Label(left_panel, text="TOOLS", font=("Helvetica", 14, "bold"),
                fg="#00f0ff", bg="#1a1f3a").pack(pady=20)
        
        # Tool buttons
        tools = [
            ("📁 Open Image", self.open_image),
            ("🗑️ Remove Background", self.remove_background),
            ("🖼️ Change Background", self.change_background),
            ("📦 Compress Image", self.compress_image),
            ("✨ Enhance Quality", self.enhance_image),
            ("🔍 Sharpen Image", self.sharpen_image),
            ("💾 Save Image", self.save_image),
            ("🔄 Reset", self.reset_image)
        ]
        
        for text, command in tools:
            btn = tk.Button(left_panel, text=text, font=("Helvetica", 11),
                           bg="#2a3f5a", fg="#ffffff", bd=0, 
                           width=24, pady=12, cursor="hand2",
                           command=command, anchor="w", padx=20,
                           activebackground="#3a4f6a", activeforeground="#00f0ff")
            btn.pack(pady=5, padx=15)
        
        # Right panel - Image display
        right_panel = tk.Frame(main_container, bg="#0a0e27")
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Canvas for image
        self.canvas_frame = tk.Frame(right_panel, bg="#1a1f3a")
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="#0a0e27", 
                               highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Info label
        self.info_label = tk.Label(self.canvas, text="📷 Open an image to start editing",
                                   font=("Helvetica", 14), fg="#7a8bff", 
                                   bg="#0a0e27")
        self.info_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Force update to get proper canvas size
        self.root.update_idletasks()
    
    def update_status(self, message, color="#7fff7f"):
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message, fg=color)
            self.root.update()
    
    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp")]
        )
        if file_path:
            try:
                self.update_status("Loading image...", "#ffff7f")
                self.original_image = Image.open(file_path)
                self.current_image = self.original_image.copy()
                self.display_current_image()
                self.info_label.place_forget()
                self.update_status(f"Image loaded: {self.current_image.size[0]}x{self.current_image.size[1]}", "#7fff7f")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengambil gambar: {str(e)}")
                self.update_status("Error loading image", "#ff4757")
    
    def display_current_image(self):
        if self.current_image:
            # Get canvas size
            self.root.update_idletasks()
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width, canvas_height = 800, 600
            
            # Create a copy for display
            img_copy = self.current_image.copy()
            
            # Calculate scaling
            img_width, img_height = img_copy.size
            scale = min((canvas_width - 40) / img_width, (canvas_height - 40) / img_height)
            new_size = (int(img_width * scale), int(img_height * scale))
            
            img_copy = img_copy.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.display_image = ImageTk.PhotoImage(img_copy)
            
            # Display on canvas
            self.canvas.delete("all")
            x = canvas_width // 2
            y = canvas_height // 2
            self.canvas.create_image(x, y, image=self.display_image, anchor="center")
            
            print(f"Image displayed: {img_copy.size}")
    
    def remove_background(self):
        if not self.current_image:
            messagebox.showwarning("Warning", "Please open an image first")
            return
        
        def process():
            try:
                self.update_status("Removing background...", "#ffff7f")
                self.show_loading("🗑️ Removing Background")
                
                # Convert PIL to bytes
                img_byte_arr = io.BytesIO()
                self.current_image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                
                # Remove background
                print("Processing with rembg...")
                output = remove(img_byte_arr)
                self.current_image = Image.open(io.BytesIO(output)).convert("RGBA")
                
                self.hide_loading()
                self.display_current_image()
                self.update_status("Background removed successfully!", "#7fff7f")
                messagebox.showinfo("Success", "Background removed successfully!")
                
            except Exception as e:
                self.hide_loading()
                self.update_status("Error removing background", "#ff4757")
                messagebox.showerror("Error", f"Failed to remove background: {str(e)}")
        
        # Run in thread to prevent freezing
        thread = threading.Thread(target=process)
        thread.daemon = True
        thread.start()
    
    def change_background(self):
        if not self.current_image:
            messagebox.showwarning("Warning", "Please Ambil gambar dulu kocag goblok!")
            return
        
        bg_path = filedialog.askopenfilename(
            title="Select background image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if bg_path:
            try:
                self.update_status("Changing background...", "#ffff7f")
                background = Image.open(bg_path).convert("RGB")
                background = background.resize(self.current_image.size, Image.Resampling.LANCZOS)
                
                if self.current_image.mode == 'RGBA':
                    foreground = self.current_image
                else:
                    self.update_status("Removing background first...", "#ffff7f")
                    messagebox.showinfo("Info", "Removing background first...")
                    
                    img_byte_arr = io.BytesIO()
                    self.current_image.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    output = remove(img_byte_arr)
                    foreground = Image.open(io.BytesIO(output)).convert("RGBA")
                
                # Composite
                result = Image.new("RGB", background.size)
                result.paste(background, (0, 0))
                result.paste(foreground, (0, 0), foreground)
                
                self.current_image = result
                self.display_current_image()
                self.update_status("Background changed successfully!", "#7fff7f")
                messagebox.showinfo("Success", "Background changed successfully!")
                
            except Exception as e:
                self.update_status("Error changing background", "#ff4757")
                messagebox.showerror("Error", f"Failed to change background: {str(e)}")
    
    def compress_image(self):
        if not self.current_image:
            messagebox.showwarning("Warning", "Please open an image first")
            return
        
        # Create dialog for quality
        dialog = tk.Toplevel(self.root)
        dialog.title("Compress Image")
        dialog.geometry("350x200")
        dialog.configure(bg="#1a1f3a")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Quality (1-100):", font=("Helvetica", 12, "bold"),
                fg="#00f0ff", bg="#1a1f3a").pack(pady=20)
        
        quality_var = tk.IntVar(value=85)
        
        quality_frame = tk.Frame(dialog, bg="#1a1f3a")
        quality_frame.pack()
        
        quality_label = tk.Label(quality_frame, text="85%", font=("Helvetica", 14, "bold"),
                                fg="#ffffff", bg="#1a1f3a", width=6)
        quality_label.pack()
        
        def update_label(val):
            quality_label.config(text=f"{val}%")
        
        quality_scale = tk.Scale(dialog, from_=1, to=100, orient="horizontal",
                                variable=quality_var, bg="#2a3f5a", fg="#ffffff",
                                troughcolor="#0a0e27", highlightthickness=0,
                                length=250, command=update_label)
        quality_scale.pack(pady=10)
        
        def apply_compression():
            quality = quality_var.get()
            try:
                self.update_status(f"Compressing at {quality}% quality...", "#ffff7f")
                output = io.BytesIO()
                rgb_img = self.current_image.convert('RGB')
                rgb_img.save(output, format='JPEG', quality=quality, optimize=True)
                output.seek(0)
                self.current_image = Image.open(output)
                self.display_current_image()
                dialog.destroy()
                self.update_status(f"Compressed to {quality}% quality", "#7fff7f")
                messagebox.showinfo("Success", f"Image compressed with quality {quality}%")
            except Exception as e:
                self.update_status("Error compressing image", "#ff4757")
                messagebox.showerror("Error", f"Compression failed: {str(e)}")
        
        tk.Button(dialog, text="APPLY", bg="#00f0ff", fg="#0a0e27",
                 font=("Helvetica", 11, "bold"), bd=0, padx=40, pady=12,
                 command=apply_compression, cursor="hand2").pack(pady=20)
    
    def enhance_image(self):
        if not self.current_image:
            messagebox.showwarning("Warning", "Please open an image first")
            return
        
        try:
            self.update_status("Enhancing image quality...", "#ffff7f")
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(self.current_image)
            self.current_image = enhancer.enhance(1.5)
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(self.current_image)
            self.current_image = enhancer.enhance(1.2)
            
            # Enhance color
            enhancer = ImageEnhance.Color(self.current_image)
            self.current_image = enhancer.enhance(1.15)
            
            # Enhance brightness slightly
            enhancer = ImageEnhance.Brightness(self.current_image)
            self.current_image = enhancer.enhance(1.05)
            
            self.display_current_image()
            self.update_status("Image enhanced successfully!", "#7fff7f")
            messagebox.showinfo("Success", "Image quality enhanced successfully!")
            
        except Exception as e:
            self.update_status("Error enhancing image", "#ff4757")
            messagebox.showerror("Error", f"Enhancement failed: {str(e)}")
    
    def sharpen_image(self):
        if not self.current_image:
            messagebox.showwarning("Warning", "Please open an image first")
            return
        
        try:
            self.update_status("Sharpening image...", "#ffff7f")
            
            # Apply unsharp mask for better sharpening
            self.current_image = self.current_image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
            
            self.display_current_image()
            self.update_status("Image sharpened!", "#7fff7f")
            messagebox.showinfo("Success", "Image sharpened successfully!")
            
        except Exception as e:
            self.update_status("Error sharpening image", "#ff4757")
            messagebox.showerror("Error", f"Sharpening failed: {str(e)}")
    
    def save_image(self):
        if not self.current_image:
            messagebox.showwarning("Warning", "No image to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), 
                      ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.update_status("Saving image...", "#ffff7f")
                self.current_image.save(file_path)
                self.update_status(f"Image saved successfully!", "#7fff7f")
                messagebox.showinfo("Success", f"Image saved to:\n{file_path}")
            except Exception as e:
                self.update_status("Error saving image", "#ff4757")
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def reset_image(self):
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.display_current_image()
            self.update_status("Image reset to original", "#7fff7f")
            messagebox.showinfo("Success", "Image reset to original")
    
    def logout(self):
        self.current_user = None
        self.current_image = None
        self.original_image = None
        self.show_login_screen()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageEditorApp()
    app.run()