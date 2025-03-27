import os
import sys
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import threading
import queue

# Style constants
BACKGROUND_COLOR = "#1E1E1E"
FOREGROUND_COLOR = "#E0E0E0"
ACCENT_COLOR = "#0288D1"
ACCENT_COLOR_ACTIVE = "#03A9F4"
CARD_COLOR = "#2C2C2C"
PADDING = 10
FONT_DEFAULT = ("Helvetica", 10)
FONT_BOLD = ("Helvetica", 10, "bold")
BUTTON_FONT = ("Helvetica", 9)
BUTTON_PADDING = 3

class AppUtils:
    """Utility class for application-specific helper methods."""
    
    @staticmethod
    def set_window_icon(window):
        """Set the window icon from a PNG file.

        Args:
            window (tk.Tk): The Tkinter window to set the icon for.

        Returns:
            tk.PhotoImage or None: The loaded icon if successful, None otherwise.
        """
        try:
            base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
            icon_path = os.path.join(base_path, "icon", "logo_app.png")  # Adjusted path to match --add-data
            print(f"Attempting to load icon from: {icon_path}")  # Debug output
            icon = tk.PhotoImage(file=icon_path)
            window.iconphoto(True, icon)
            return icon  # Returning icon to keep it alive
        except Exception as e:
            print(f"Error loading icon: {e}")
            return None

class CustomDialog(simpledialog.Dialog):
    """Custom dialog for entering a filename with styled appearance."""
    
    def __init__(self, parent, title):
        """Initialize the custom dialog.

        Args:
            parent (tk.Tk): The parent window.
            title (str): The title of the dialog.
        """
        self.result = None
        super().__init__(parent, title)

    def body(self, master):
        """Create the dialog body with a label and entry field.

        Args:
            master (tk.Frame): The frame to place widgets in.

        Returns:
            ttk.Entry: The entry widget for focus.
        """
        self.configure(bg=BACKGROUND_COLOR)
        master.configure(bg=BACKGROUND_COLOR)
        
        label = ttk.Label(master, 
                         text="Enter filename for hash file (include extension):",
                         background=BACKGROUND_COLOR,
                         foreground=FOREGROUND_COLOR,
                         font=FONT_DEFAULT)
        label.pack(pady=5)
        
        self.entry = ttk.Entry(master, 
                             width=40,
                             style='Custom.TEntry')
        self.entry.pack(pady=5)
        return self.entry

    def buttonbox(self):
        """Override the default button box with custom styled buttons."""
        box = tk.Frame(self, bg=BACKGROUND_COLOR)
        
        ok_button = ttk.Button(box, 
                             text="OK", 
                             width=10, 
                             command=self.ok,
                             style='Custom.TButton')
        ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        cancel_button = ttk.Button(box, 
                                 text="Cancel", 
                                 width=10, 
                                 command=self.cancel,
                                 style='Custom.TButton')
        cancel_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        
        box.pack()

    def apply(self):
        """Store the entered filename as the dialog result."""
        self.result = self.entry.get()

class HashGeneratorApp(AppUtils):
    """Main application class for generating file hashes with a GUI."""
    
    def __init__(self, root):
        """Initialize the hash generator application.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("ATphonOS Version File Hash Generator")
        self.root.geometry("600x480")
        self.root.resizable(False, False)
        self.root.configure(bg=BACKGROUND_COLOR)

        # Queue for thread communication
        self.log_queue = queue.Queue()
        self.running = False

        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background=BACKGROUND_COLOR)
        style.configure('TLabel', background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR, font=FONT_DEFAULT)
        style.configure('TLabelframe', background=CARD_COLOR, foreground=FOREGROUND_COLOR)
        style.configure('TLabelframe.Label', background=CARD_COLOR, foreground=FOREGROUND_COLOR, font=FONT_BOLD)
        
        style.configure('TButton', 
                       background=ACCENT_COLOR,
                       foreground=FOREGROUND_COLOR,
                       font=BUTTON_FONT,
                       padding=BUTTON_PADDING)
        style.map('TButton',
                 background=[('active', ACCENT_COLOR_ACTIVE)],
                 foreground=[('active', FOREGROUND_COLOR)])
        
        style.configure('Custom.TButton', 
                       background=ACCENT_COLOR,
                       foreground=FOREGROUND_COLOR,
                       font=BUTTON_FONT,
                       padding=BUTTON_PADDING)
        style.map('Custom.TButton',
                 background=[('active', ACCENT_COLOR_ACTIVE)],
                 foreground=[('active', FOREGROUND_COLOR)])
        
        style.configure('TEntry',
                       fieldbackground=CARD_COLOR,
                       foreground=FOREGROUND_COLOR,
                       insertcolor=FOREGROUND_COLOR)
        style.configure('Custom.TEntry',
                       fieldbackground=CARD_COLOR,
                       foreground=FOREGROUND_COLOR,
                       insertcolor=FOREGROUND_COLOR)
        
        style.configure('TCheckbutton',
                       background=BACKGROUND_COLOR,
                       foreground=FOREGROUND_COLOR,
                       font=FONT_DEFAULT)
        style.map('TCheckbutton',
                 background=[('active', BACKGROUND_COLOR), ('!disabled', BACKGROUND_COLOR)],
                 foreground=[('active', FOREGROUND_COLOR)],
                 indicatorbackground=[('selected', ACCENT_COLOR), ('!selected', CARD_COLOR)],
                 indicatorforeground=[('selected', FOREGROUND_COLOR)])

        style.configure('TProgressbar',
                       background=ACCENT_COLOR,
                       troughcolor=CARD_COLOR)

        # Set and store the icon to prevent garbage collection
        self.icon = self.set_window_icon(self.root)
        if self.icon is None:
            print("Failed to set window icon.")

        main_frame = ttk.Frame(self.root, padding=PADDING)
        main_frame.pack(expand=True, fill="both")

        ttk.Label(main_frame, text="Directory Path:").grid(row=0, column=0, sticky="w", pady=5)
        self.dir_entry = ttk.Entry(main_frame, width=50)
        self.dir_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_directory).grid(row=0, column=2, padx=5)

        ttk.Label(main_frame, text="Version name:").grid(row=1, column=0, sticky="w", pady=5)
        self.version_entry = ttk.Entry(main_frame, width=50)
        self.version_entry.grid(row=1, column=1, padx=5, pady=5)
        self.version_entry.insert(0, "")

        # Checkbox frame
        checkbox_frame = ttk.Frame(main_frame)
        checkbox_frame.grid(row=1, column=2, rowspan=2, padx=5, pady=5, sticky="n")

        self.only_hash_var = tk.BooleanVar()
        self.only_hash_check = ttk.Checkbutton(checkbox_frame, 
                                             text="Only Hash", 
                                             variable=self.only_hash_var,
                                             command=self.toggle_version_entry)
        self.only_hash_check.pack(anchor="w", pady=2)

        self.custom_filename_var = tk.BooleanVar()
        self.custom_filename_check = ttk.Checkbutton(checkbox_frame, 
                                                   text="Custom Filename", 
                                                   variable=self.custom_filename_var)
        self.custom_filename_check.pack(anchor="w", pady=2)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        self.generate_button = ttk.Button(button_frame, text="Generate Hash File", command=self.start_hash_generation)
        self.generate_button.pack(side=tk.LEFT, padx=5)

        # Log area without scrollbar
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding=5)
        log_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=5)
        
        self.log_text = tk.Text(log_frame, 
                              height=15, 
                              width=70, 
                              state='disabled', 
                              wrap=tk.WORD,
                              bg=CARD_COLOR,
                              fg=FOREGROUND_COLOR,
                              insertbackground=FOREGROUND_COLOR,
                              font=FONT_DEFAULT,
                              borderwidth=0)
        self.log_text.pack(side=tk.LEFT, fill="both", expand=True)
        
        self.log_text.tag_configure("hyperlink", foreground=ACCENT_COLOR_ACTIVE, underline=1)
        self.log_text.tag_bind("hyperlink", "<Enter>", lambda e: self.log_text.config(cursor="hand2"))
        self.log_text.tag_bind("hyperlink", "<Leave>", lambda e: self.log_text.config(cursor=""))
        self.log_text.tag_bind("hyperlink", "<Button-1>", self._on_link_click)

        # Progress bar and label
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=5, column=0, columnspan=3, pady=5, sticky="ew")
        
        self.progress_label = ttk.Label(progress_frame, text="Progress: 0/0 files")
        self.progress_label.pack(side=tk.LEFT, padx=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, 
                                          orient=tk.HORIZONTAL, 
                                          length=400, 
                                          mode='determinate',
                                          style='TProgressbar')
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)

        # Start checking the queue
        self.root.after(100, self.check_queue)

    def _on_link_click(self, event):
        """Handle click on hyperlink in the log to open the generated file.

        Args:
            event (tk.Event): The event object from the click.
        """
        self.open_generated_file()

    def toggle_version_entry(self):
        """Enable/disable version entry based on the 'Only Hash' checkbox state."""
        if self.only_hash_var.get():
            self.version_entry.config(state='disabled')
        else:
            self.version_entry.config(state='normal')

    def browse_directory(self):
        """Open a directory selection dialog and update the UI with the selected path."""
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
            self.log(f"Selected directory: {directory}")
            total_files = sum(len(files) for _, _, files in os.walk(directory))
            self.progress_bar['maximum'] = total_files
            self.progress_bar['value'] = 0
            self.progress_label.config(text=f"Progress: 0/{total_files} files")

    def calculate_file_hash(self, filepath: str) -> str:
        """Calculate the SHA-1 hash of a file, truncated to 16 characters.

        Args:
            filepath (str): Path to the file to hash.

        Returns:
            str: The hash value or an error message if calculation fails.
        """
        try:
            with open(filepath, 'rb') as f:
                sha1 = hashlib.sha1()
                for chunk in iter(lambda: f.read(4096), b''):
                    sha1.update(chunk)
                hash_value = sha1.hexdigest()[:16]
                return hash_value
        except Exception as e:
            return f"Error: {e}"

    def start_hash_generation(self):
        """Start the hash file generation process in a separate thread."""
        if self.running:
            messagebox.showinfo("Info", "Hash generation is already in progress.")
            return

        directory = self.dir_entry.get().strip()
        if not directory:
            messagebox.showerror("Error", "Please enter or select a directory path.")
            return
        
        if not os.path.isdir(directory):
            messagebox.showerror("Error", "The specified path is not a valid directory.")
            self.log(f"Error: '{directory}' is not a valid directory")
            return

        only_hash = self.only_hash_var.get()
        version_text = self.version_entry.get().strip() if not only_hash else "--NO VERSION--"
        
        if not only_hash and not version_text:
            messagebox.showerror("Error", "Enter Version name or check 'Only Hash'.")
            return

        custom_filename = self.custom_filename_var.get()
        if custom_filename:
            dialog = CustomDialog(self.root, "Custom Filename")
            output_file = dialog.result
            if not output_file:
                messagebox.showerror("Error", "Filename cannot be empty. Operation cancelled.")
                return
            if not output_file.endswith('.txt'):
                output_file += '.txt'
        else:
            output_file = "file_hashes.txt"

        self.running = True
        self.generate_button.config(state='disabled')
        self.progress_bar['value'] = 0
        self.log("\n--- Starting hash generation ---")

        thread = threading.Thread(target=self.generate_hash_file, args=(directory, output_file, version_text))
        thread.start()

    def generate_hash_file(self, directory, output_file, version_text):
        """Generate a hash file with file paths and hashes in a separate thread.

        Args:
            directory (str): The directory to scan for files.
            output_file (str): The path to save the hash file.
            version_text (str): The version text to append at the end of the file.
        """
        try:
            total_files = sum(len(files) for _, _, files in os.walk(directory))
            self.log_queue.put(f"Found {total_files} files to process across all subdirectories")
            self.log_queue.put(("progress_total", total_files))
            processed_files = 0

            with open(output_file, 'w', encoding='utf-8') as out_f:
                for root_dir, _, files in os.walk(directory):
                    for filename in files:
                        if not self.running:
                            return
                        file_path = os.path.join(root_dir, filename)
                        relative_path = os.path.relpath(file_path, directory)
                        file_hash = self.calculate_file_hash(file_path)
                        out_f.write(f"{relative_path}  {file_hash}\n")
                        processed_files += 1
                        self.log_queue.put(f"Progress: {processed_files}/{total_files} files processed - {os.path.basename(file_path)}: {file_hash}")
                        self.log_queue.put(("progress_update", processed_files, total_files))
                
                out_f.write(f"{version_text}\n")
                self.log_queue.put(f"Added Version: {version_text}")

            success_msg = f"Hash file '{output_file}' created successfully with {total_files} entries."
            self.log_queue.put(success_msg)
            self.log_queue.put(("link", f"Click here to open {output_file}", output_file))
            self.log_queue.put(("success", success_msg))
            self.last_generated_file = output_file
        except Exception as e:
            error_msg = f"Error creating hash file: {e}"
            self.log_queue.put(error_msg)
            self.log_queue.put(("error", error_msg))
        finally:
            self.running = False

    def check_queue(self):
        """Process messages from the queue to update the UI."""
        try:
            while True:
                item = self.log_queue.get_nowait()
                if isinstance(item, tuple):
                    if item[0] == "link":
                        self.log_link(item[1], item[2])
                    elif item[0] == "success":
                        messagebox.showinfo("Success", item[1])
                    elif item[0] == "error":
                        messagebox.showerror("Error", item[1])
                    elif item[0] == "progress_total":
                        self.progress_bar['maximum'] = item[1]
                        self.progress_label.config(text=f"Progress: 0/{item[1]} files")
                    elif item[0] == "progress_update":
                        self.progress_bar['value'] = item[1]
                        self.progress_label.config(text=f"Progress: {item[1]}/{item[2]} files")
                else:
                    self.log(item)
        except queue.Empty:
            pass
        if not self.running:
            self.generate_button.config(state='normal')
        self.root.after(100, self.check_queue)

    def open_generated_file(self):
        """Open the last generated hash file in the default system application."""
        output_file = getattr(self, 'last_generated_file', "file_hashes.txt")
        try:
            if os.path.exists(output_file):
                os.startfile(output_file)
                self.log(f"Opened {output_file}")
            else:
                messagebox.showerror("Error", f"File '{output_file}' not found. Generate Hash File.")
                self.log(f"Error: '{output_file}' not found")
        except Exception as e:
            error_msg = f"Error opening file: {e}"
            self.log(error_msg)
            messagebox.showerror("Error", error_msg)

    def log(self, message):
        """Add a message to the log text widget.

        Args:
            message (str): The message to log.
        """
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def log_link(self, message, file_path):
        """Add a clickable hyperlink to the log text widget.

        Args:
            message (str): The message to display as a hyperlink.
            file_path (str): The file path associated with the link.
        """
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{message}\n", "hyperlink")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = HashGeneratorApp(root)
    root.mainloop()