import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import io
import fitz  # PyMuPDF
import os
from tkinterdnd2 import TkinterDnD, DND_FILES
import ebooklib
from ebooklib import epub

class BookImageExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Cover Image Extractor")
        self.root.geometry("800x500")

        # Create main frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Enable drag and drop
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop)

        # Title
        title_label = tk.Label(main_frame, text="Book Cover Image Extractor", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # Instructions
        instructions = tk.Label(main_frame, text="Drop a PDF or EPUB file here, or click 'Select File' to choose and extract the thumbnail image",
                                wraplength=400, justify=tk.CENTER)
        instructions.pack(pady=(0, 20))

        # File path display
        self.file_path_var = tk.StringVar()
        file_label = tk.Label(main_frame, text="Selected File:", font=("Arial", 10, "bold"))
        file_label.pack(pady=(10, 0))
        self.file_path_label = tk.Label(main_frame, textvariable=self.file_path_var, wraplength=400, fg="blue")
        self.file_path_label.pack(pady=(0, 20))

        # Select file button
        self.select_button = tk.Button(main_frame, text="Select File", command=self.select_file, font=("Arial", 12), bg="lightblue")
        self.select_button.pack(pady=5)
        
        # Select Output Directory button
        self.select_dir_button = tk.Button(main_frame, text="Select Output Directory", command=self.select_output_directory, font=("Arial", 12), bg="lightyellow")
        self.select_dir_button.pack(pady=5)
        
        # Output directory display
        self.output_dir_var = tk.StringVar()
        self.output_dir_var.set("No output directory selected")
        dir_label = tk.Label(main_frame, text="Output Directory:", font=("Arial", 10, "bold"))
        dir_label.pack(pady=(10, 0))
        self.dir_path_label = tk.Label(main_frame, textvariable=self.output_dir_var, wraplength=400, fg="green")
        self.dir_path_label.pack(pady=(0, 20))
        
        # Extract button
        self.extract_button = tk.Button(main_frame, text="Extract Image", command=self.extract_image, 
                                    state=tk.DISABLED, font=("Arial", 12), bg="lightgreen")
        self.extract_button.pack(pady=10)
        
        # Status
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = tk.Label(main_frame, textvariable=self.status_var, fg="gray")
        status_label.pack(pady=10)

        self.file_path = None
        self.output_dir = None
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select PDF or EPUB File",
            filetypes=[("PDF and EPUB files", "*.pdf;*.epub"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path = file_path
            self.file_path_var.set(os.path.basename(self.file_path))
            # Enable extract button only if output directory is selected
            if self.output_dir:
                self.extract_button.config(state=tk.NORMAL)
            self.status_var.set("File selected. Select output directory and click 'Extract Image'.")

    def select_output_directory(self):
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            # Verify that the directory exists and is writable
            if os.path.exists(dir_path) and os.access(dir_path, os.W_OK):
                self.output_dir = dir_path
                self.output_dir_var.set(os.path.basename(self.output_dir))
                # Enable extract button only if file is selected
                if self.file_path:
                    self.extract_button.config(state=tk.NORMAL)
                self.status_var.set("Output directory selected. Click 'Extract Image' to proceed.")
            else:
                messagebox.showerror("Error", "Selected directory does not exist or is not writable")

    def drop(self, event):
        if event.data:
            # Parse the dropped file path (remove braces if present)
            file_path = event.data.strip('{}')
            if file_path and os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()
                if ext in ['.pdf', '.epub']:
                    self.file_path = file_path
                    self.file_path_var.set(os.path.basename(self.file_path))
                    if self.output_dir:
                        self.extract_button.config(state=tk.NORMAL)
                    self.status_var.set("File dropped. Click 'Extract Image' to proceed.")
                else:
                    self.status_var.set("Please drop a PDF or EPUB file.")
            else:
                self.status_var.set("Invalid file dropped.")

    def extract_image(self):
        if not self.file_path or not os.path.exists(self.file_path):
            messagebox.showerror("Error", "Please select a valid PDF or EPUB file")
            return

        ext = os.path.splitext(self.file_path)[1].lower()
        if ext not in ['.pdf', '.epub']:
            messagebox.showerror("Error", "Selected file is not a PDF or EPUB")
            return

        if not self.output_dir:
            messagebox.showerror("Error", "Please select an output directory")
            return

        try:
            self.status_var.set("Processing...")
            self.root.update()

            file_name = os.path.splitext(os.path.basename(self.file_path))[0]
            output_file = os.path.join(self.output_dir, f"{file_name}_cover.png")

            if ext == '.pdf':
                # Open the PDF
                doc = fitz.open(self.file_path)

                # Check if PDF has at least one page
                if doc.page_count < 1:
                    messagebox.showerror("Error", "PDF file has no pages")
                    doc.close()
                    return

                page = doc.load_page(0)

                # Extract the first page as bitmap and save as PNG
                pix = page.get_pixmap()
                pix.save(output_file)
                doc.close()

            elif ext == '.epub':
                # Open the EPUB
                book = epub.read_epub(self.file_path)

                # Find first image
                images = [item for item in book.get_items() if item.get_type() == ebooklib.ITEM_IMAGE]
                if not images:
                    messagebox.showerror("Error", "EPUB file has no images")
                    return

                # Take first image, convert to PIL Image and save as PNG
                image_item = images[0]
                image_data = image_item.get_content()

                img = Image.open(io.BytesIO(image_data))
                img.save(output_file, "PNG")

            messagebox.showinfo("Success", f"Image extracted successfully!\nSaved as: {os.path.basename(output_file)}")
            self.status_var.set(f"Image saved as: {os.path.basename(output_file)}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while processing the file:\n{str(e)}")
            self.status_var.set("Error occurred")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = BookImageExtractor(root)
    root.mainloop()
