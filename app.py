import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import importlib.util, sys, os, subprocess, shutil, glob, json, random, tempfile

CONFIG_PATH = os.path.join(
    os.path.expanduser("~"), "Documents", "MIDI Converter", "config.json"
)

# --- Asset paths for PyInstaller ---
if getattr(sys, "frozen", False):
    # Running as a PyInstaller bundle
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

icon_path = os.path.join(base_path, "assets", "midi_icon.ico")
# flame_path = os.path.join(base_path, "assets", "flames.gif")


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}


def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)


# -----------------------------
# Helper function to center a window
# -----------------------------
def center_window(window, width=500, height=200):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


# -----------------------------
# Custom dialog class
# -----------------------------
class FileExistsDialog(simpledialog.Dialog):
    def __init__(self, parent, filename):
        self.filename = filename
        self.choice = None
        super().__init__(parent, title="File Exists")

    def body(self, master):
        tk.Label(
            master,
            text=f"The file '{self.filename}' already exists.\nChoose an action:",
        ).pack(pady=10)

        self.var = tk.StringVar(value="overwrite")  # default option

        tk.Radiobutton(
            master, text="Overwrite", variable=self.var, value="overwrite"
        ).pack(anchor="w")
        tk.Radiobutton(
            master, text="Auto-rename", variable=self.var, value="auto"
        ).pack(anchor="w")
        tk.Radiobutton(master, text="Cancel", variable=self.var, value="cancel").pack(
            anchor="w"
        )

        return None  # no widget focus by default

    def apply(self):
        self.choice = self.var.get()


# -----------------------------
# Main App class
# -----------------------------
class MidiConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MIDI Converter 3000")
        self.root.geometry("550x480")
        self.root.iconbitmap(default=icon_path)
        self.root.configure(bg="#FF00FF")  # hot pink
        self.center_window(550, 480)
        self.flash_colors()  # flashing background

        # Variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()

        # Default output folder
        default_folder = os.path.join(
            os.path.expanduser("~"), "Documents", "MIDI Converter"
        )
        os.makedirs(default_folder, exist_ok=True)
        self.default_output_folder = default_folder

        # Autofill output filename based on input
        def autofill_output(*args):
            input_file = self.input_path.get()
            if input_file:
                base_name = os.path.splitext(os.path.basename(input_file))[0]
                default_midi_path = os.path.join(
                    self.default_output_folder, base_name + ".mid"
                )
                self.output_path.set(default_midi_path)

        self.input_path.trace("w", autofill_output)

        # Header
        header = tk.Label(
            root,
            text="🎵 MIDI CONVERTER 3000 🎵",
            font=("Impact", 24, "bold"),
            fg="#FFFFFF",
            bg="#0000FF",
            bd=5,
            relief="raised",
            padx=10,
            pady=10,
        )
        header.pack(pady=10)

        # Main frame
        frame = tk.Frame(root, bg="#00FFFF", bd=5, relief="sunken")
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Input
        tk.Label(
            frame,
            text="Select Python Script:",
            font=("Comic Sans MS", 12, "bold"),
            bg="#00FFFF",
        ).pack(pady=5)
        tk.Entry(frame, textvariable=self.input_path, width=40).pack(pady=5)
        tk.Button(
            frame,
            text="Browse",
            command=self.select_input,
            bg="#FFFF00",
            fg="#FF0000",
            font=("Comic Sans MS", 12, "bold"),
            bd=5,
            relief="raised",
        ).pack(pady=5)

        # Output
        tk.Label(
            frame,
            text="Select Output MIDI File:",
            font=("Comic Sans MS", 12, "bold"),
            bg="#00FFFF",
        ).pack(pady=5)
        tk.Entry(frame, textvariable=self.output_path, width=40).pack(pady=5)
        tk.Button(
            frame,
            text="Browse",
            command=self.select_output,
            bg="#00FF00",
            fg="#0000FF",
            font=("Comic Sans MS", 12, "bold"),
            bd=5,
            relief="raised",
        ).pack(pady=5)

        # Generate button
        tk.Button(
            frame,
            text="GENERATE MIDI",
            command=self.generate_midi,
            bg="#FF4500",
            fg="#FFFF00",
            font=("Impact", 14, "bold"),
            bd=5,
            relief="raised",
        ).pack(pady=20)

        # # Optional flame GIF (replace 'flames.gif' with your file)
        # try:
        #     self.flame_img = tk.PhotoImage(file="assets/flames.gif")
        #     tk.Label(frame, image=self.flame_img, bg="#00FFFF").pack()
        # except Exception:
        #     pass

    # --- Center window ---
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    # --- Flashing background ---
    def flash_colors(self):
        colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
        self.root.configure(bg=random.choice(colors))
        self.root.after(300, self.flash_colors)

    # --- File dialogs ---
    def select_input(self):
        path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if path:
            self.input_path.set(path)

    def select_output(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".mid", filetypes=[("MIDI files", "*.mid")]
        )
        if path:
            self.output_path.set(path)

    # --- Generate MIDI ---
    def generate_midi(self):
        script_path = self.input_path.get()
        midi_path = self.output_path.get()

        if not script_path:
            messagebox.showerror("Error", "Please select a Python script.")
            return
        if not midi_path:
            messagebox.showerror("Error", "Please select an output MIDI file path.")
            return

        os.makedirs(os.path.dirname(midi_path), exist_ok=True)

        # --- File exists handling ---
        if os.path.exists(midi_path):
            dialog = FileExistsDialog(self.root, os.path.basename(midi_path))
            choice = dialog.choice

            if choice == "cancel" or choice is None:
                return
            elif choice == "auto":
                base, ext = os.path.splitext(midi_path)
                counter = 1
                while os.path.exists(f"{base}_{counter}{ext}"):
                    counter += 1
                midi_path = f"{base}_{counter}{ext}"
                self.output_path.set(midi_path)

        # --- Load module ---
        module_name = os.path.splitext(os.path.basename(script_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # --- Call generate_midi if exists ---
        if hasattr(module, "generate_midi"):
            try:
                module.generate_midi(midi_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not generate MIDI:\n{e}")
                return
        else:
            try:
                script_dir = os.path.dirname(script_path)
                before_files = set(glob.glob(os.path.join(script_dir, "*.mid"))) | set(
                    glob.glob("*.mid")
                )
                subprocess.run(
                    [sys.executable, script_path], check=True, cwd=script_dir
                )
                after_files = set(glob.glob(os.path.join(script_dir, "*.mid"))) | set(
                    glob.glob("*.mid")
                )
                new_files = list(after_files - before_files)
                if not new_files:
                    messagebox.showerror(
                        "Error", "No MIDI file was created by the script."
                    )
                    return
                shutil.move(new_files[0], midi_path)
            except Exception as e:
                messagebox.showerror("Error", f"Error generating MIDI:\n{e}")
                return

        # --- Success ---
        messagebox.showinfo("Success", f"MIDI saved to {midi_path}")
        folder_path = os.path.dirname(midi_path)
        if os.path.exists(folder_path):
            os.startfile(folder_path)
        self.root.destroy()


# --- Run app ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MidiConverterApp(root)
    root.mainloop()
