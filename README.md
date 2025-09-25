# MIDI3000

🎵 **MIDI3000** is a standalone GUI tool for converting Python scripts into MIDI files.  
It features a user-friendly interface, allows you to select input `.py` scripts, choose output locations, and generates MIDI files with a single click. Perfect for use with ChatGPT-generated MIDI Python scripts.

---

## **Features**

- Converts Python scripts that generate MIDI into `.mid` files.
- Customizable output folder.
- Automatically handles filename conflicts (overwrite, auto-rename, cancel).
- The app includes a classic early-2000s inspired GUI.
- Standalone executable (`MIDI3000.exe`) — no Python installation required.

---

## **Download**

You can download the latest **MIDI3000.exe** from the [Releases](https://github.com/<your-username>/<repo-name>/releases) page.

---

## **How to Use**

1. Launch `MIDI3000.exe`.
2. Use the **“Select Python Script”** button to pick a `.py` file containing MIDI generation code.
3. Set the **output path** (pre-filled with the same name as the input file by default).
4. Click **“Generate MIDI”**.
5. On success, the output folder will open automatically.

---

## **Prompting ChatGPT for compatible Python scripts**

When asking ChatGPT to generate MIDI scripts for MIDI3000, keep these guidelines:

- Ensure the Python script either contains a `generate_midi(output_path)` function or produces a `.mid` file in the script’s directory.
- Always pass the output filename as a parameter when possible.
- Example prompt:
  Generate a Python script that creates a 16-bar drum pattern MIDI file and writes it to a given output path. The script should define a function called generate_midi(output_path) so it is compatible with MIDI3000.

- Avoid scripts that require interactive input, as MIDI3000 does not handle console input.

---

## **Building MIDI3000 from source**

If you want to make changes or rebuild the app:

1. Clone the repo:

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

2. Create and activate a virtual environment:

```bash
   python -m venv venv
   venv\Scripts\activate # Windows
```

3. Install dependencies:

```bash
   pip install -r requirements.txt
```

4. Build the standalone executable using PyInstaller:

```bash
   pyinstaller --onefile --windowed --name=MIDI3000 --icon=assets/midi_icon.ico --add-data "assets/midi_icon.ico;assets" app.py
```

5. The .exe will be in the dist/ folder.

Folder Structure

```bash
MIDI3000/
├── app.py
├── assets/
│ └── midi_icon.ico
├── requirements.txt
├── README.md
└── dist/
└── MIDI3000.exe # built executable
```

assets/ — contains icons or images used in the GUI.
dist/ — output folder created by PyInstaller when building the exe.

## Troubleshooting

If the app fails to find the icon, ensure it is in assets/midi_icon.ico.

If the app can’t generate MIDI, check that the Python script is compatible (see ChatGPT prompting guidelines).

On Windows, ensure the .exe is not already running when rebuilding with PyInstaller (prevents access errors).

## Contributing

Feel free to fork the repo and submit pull requests. When contributing:

Keep the assets/ folder organized.

Ensure Python scripts generated are compatible with generate_midi(output_path).

## License

This project is open-source and available under the MIT License.
