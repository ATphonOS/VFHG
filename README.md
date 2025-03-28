# ATphonOS VFHG (Version File Hash Generator)

The **Version File Hash Generator** is a Python-based desktop application designed to generate SHA-1 hashes for files within a specified directory and its subdirectories. The tool outputs these hashes into a text file, optionally appending a version string.
## Compilation

Since this is a Python script, no traditional compilation is required. However, it depends on Python and specific libraries. Follow these steps to prepare and run the program:

### Prerequisites
- **Python 3.6+**: Ensure Python is installed on your system. Download it from [python.org](https://www.python.org/downloads/) 
- **Required Libraries**:
  
  - `PyInstaller`: Install via pip:
    
   ```bash
  pip install pyinstaller
  ```
  - `tkinter`: Typically included with Python standard installations.
 
   - No additional external libraries are required beyond the standard library (`os`, `sys`, `hashlib`, `threading`, `queue`).


For further assistance, refer to the [PyInstaller documentation](https://pyinstaller.org/en/stable/) or open an issue in this repository.
### Option 1: Single Executable File

This option bundles the application into a single `.exe` file, making it easy to distribute.

**Command:**
```bash
pyinstaller --onefile --windowed --icon=icon/logo_app.ico --add-data "icon/logo_app.png;icon" --name "ATphonOS Version File Integrity Check" VFHG.py
```

- **`--onefile`**: Packages everything into a single executable.
- **`--windowed`**: Runs the GUI without a console window.
- **`--icon=icon/logo_app.png`**: Sets the application icon.
- **`--add-data "icon/logo_app.png;icon"`**: Includes the icon file in the bundle. 
- **`--name "ATphonOS Version File Hash Generator"`**: Names the output file `Version File Hash Generator.exe`.
- **`VFHG.py`**: The source script to compile.

**Output**: A single `ATphonOS Version File Hash Generator.exe` file will be created in the `dist/` directory.

### Option 2: Directory with Dependencies

This option creates a folder containing the executable and all required dependencies, useful for debugging or when dependencies need to be modified.

**Command:**
```bash
pyinstaller --onedir --windowed --icon=icon/logo_app.ico --add-data "icon/logo_app.png;icon" --name "ATphonOS Version File Integrity Check" VFHG.py
```

- **`--onedir`**: Creates a directory with the executable and dependencies.
- Other flags are identical to Option 1 (see descriptions above)

**Output**: A `ATphonOS Version File Hash Generator` folder will be created in the `dist/` directory, containing `ATphonOS Version File Integrity Generator.exe` and supporting files.

### Installation
1. **Clone or Download the Repository**:
   ```bash
   git clone https://github.com/ATphonOS/VFHG.git
   cd VFHG
   ```
   Alternatively, download the ZIP file and extract it.

2. **Verify Dependencies**:
   Ensure `tkinter` is available by running:
   ```bash
   python -c "import tkinter"
   ```
 
 
 
For further assistance, refer to the [PyInstaller documentation](https://pyinstaller.org/en/stable/) or open an issue in this repository.
 
 
### Running the Program
Execute the script directly with Python or run the exe file.
```bash
python VFHG.py
```

## Usage

The application provides a simple GUI to generate hash files. Here’s how to use it:

1. **Launch the Application**:
   Run the script as described above.

   ![VFHG1](https://github.com/user-attachments/assets/28cc7163-c6c5-441e-9b3d-e7ee26ef88d6)


3. **Select a Directory**:
   - Click the "Browse" button next to "Directory Path".
   - Choose a directory containing the files to hash.
   - The progress bar will immediately display "Progress: 0/N files", where N is the total number of files in the directory and its subdirectories.

4. **Configure Options**:
   - **Version Name**: Enter a version string in the "Version name" field. This will be appended to the hash file. Leave blank and check "Only Hash" if no version is desired.
   - **Only Hash**: Check this box to disable the version field and use a default "--NO VERSION--" string.
   - **Custom Filename**: Check this box to specify a custom output filename. If unchecked, the default is "file_hashes.txt".

5. **Generate the Hash File**:
   - Click "Generate Hash File".
   - The log window will display progress messages (e.g., "Found N files to process", "Progress: X/N files processed - filename: hash").
   - The progress bar will update in real-time, filling as files are processed.
   - Upon completion, a success message appears, and a clickable link ("Click here to open {filename}") is added to the log.
     
![VFHG2](https://github.com/user-attachments/assets/ef54e2a0-d5c2-4d71-b6bf-fe194c329feb)


6. **View the Output**:
   - Click the link in the log to open the generated hash file in your default text editor.
   - The file contains relative file paths and their 16-character SHA-1 hashes, with the version string (if specified) on the last line.

![VFHG3](https://github.com/user-attachments/assets/900ca0e3-9480-47fd-aff5-a15a9a9e7b74)


### Notes
- The log window does not have a scrollbar; use the mouse wheel or arrow keys to navigate if the content exceeds the visible area.
- The program runs hashing in a separate thread to keep the GUI responsive, especially for large directories (1000+ files).
- Errors (e.g., invalid directory, file access issues) are logged and shown in a dialog box.

## Documentation for ATphonOS Version File Hash Generator

This document outlines how to generate and access the documentation for the `VFHG.py` script using Pydoc and `wget`. The generated documentation is stored in the `docs/` directory of this repository and is currently supported only on Windows.

## Overview

The documentation is generated using Python’s built-in `pydoc` module, which creates HTML files for the script and its imported standard library modules. These files are included in the `docs/` directory. To view the documentation, you must run a Pydoc server and access the HTML files locally. To regenerate the documentation, you’ll use `wget` with a provided `modules.txt` file to download the HTML files from the Pydoc server.

## Prerequisites

- **Python 3.6+**: Required to run the script and Pydoc. Download from [python.org](https://www.python.org/downloads/).
- **`wget` for Windows**: Version 1.21.4 (x64) is included in this repository in the root directory (`wget.exe`). If missing, download it from [GNU Wget](https://eternallybored.org/misc/wget/) and place it in the same directory as `VFHG.py`.
- **Project Files**: Ensure you have:
  - `VFHG.py` (the main script).
  - `modules.txt` (list of module URLs, located in the root directory).
 

## Accessing Existing Documentation

The pre-generated documentation is included in the `docs/` directory. To view it:

1. **Start the Pydoc Server**:
   Open a terminal (CMD) in the repository’s root directory (where `VFHG.py` is located) and run:
   ```bash
   python -m pydoc -p 8000
   ```
   This starts a local server on port 8000, serving documentation for all Python modules in the current directory.

2. **Access the Documentation**:
   - While the server is running, open a web browser or file explorer.
   - Navigate to the `docs/` directory in the repository (e.g., `file:///<path-to-repo>/docs/`).
   - Open `index.html` or any module-specific file. The links (index, module index, keywords, topics) will work as long as the Pydoc server is active on `http://localhost:8000`.

## Regenerating Documentation

To regenerate the documentation (e.g., after modifying the script), follow these steps:

1. **Start the Pydoc Server**:
   In a terminal (CMD) in the repository’s root directory, run:
   ```bash
   python -m pydoc -p 8000
   ```
   Keep this terminal open and the server running.

2. **Download Documentation with `wget`**:
   - Open a new terminal (CMD) in the same directory.
   - Ensure `wget.exe` (version 1.21.4 x64) is in the root directory alongside `VFHG.py`.
   - Run the following command:
     ```bash
     wget -i modules.txt -P docs -p -k
     ```
     - **`-i modules.txt`**: Reads URLs from `modules.txt` (e.g., `http://localhost:8000/os.html`), which lists the modules used in the script.
     - **`-P docs`**: Saves the downloaded HTML files to the `docs/` directory. If it doesn’t exist, `wget` will create it.
     - **`-p`**: Downloads additional resources (e.g., CSS) needed for the HTML pages.
     - **`-k`**: Converts links in the HTML files to work locally without the server.

3. **Verify Output**:
   - After running the command, check the `docs/` directory for updated HTML files.
   - Stop the Pydoc server (Ctrl+C in the first terminal) once the download is complete.

## Contents of `modules.txt`

The `modules.txt` file (included in the repository) contains URLs pointing to the Pydoc server for each module used in the script:
- `http://localhost:8000/os.html`
- `http://localhost:8000/sys.html`
- `http://localhost:8000/hashlib.html`
- `http://localhost:8000/tkinter.html`
- `http://localhost:8000/tkinter.ttk.html`
- `http://localhost:8000/tkinter.messagebox.html`
- `http://localhost:8000/tkinter.filedialog.html`
- `http://localhost:8000/tkinter.simpledialog.html`
- `http://localhost:8000/threading.html`
- `http://localhost:8000/queue.html`

These correspond to the imports in `VFHG.py`.

## Notes

- **Windows-Only**: This documentation process relies on `wget.exe` for Windows and the `os.startfile` function in the script, making it Windows-specific. For cross-platform support, additional modifications would be needed.
- **Server Requirement**: The Pydoc server must be running to access live links in the HTML files. For offline use, ensure all files are downloaded with `wget` and use the converted local links.
- **File Paths**: Run all commands from the repository’s root directory to ensure correct relative paths.

## Troubleshooting

- **Missing `wget`**: If `wget.exe` is not found, download it and place it in the root directory, or adjust the command to point to its location. Download [wget](https://eternallybored.org/misc/wget/).
- **Empty `docs/` Directory**: Ensure the Pydoc server is running and `modules.txt` contains valid URLs before running `wget`.
- **404 Errors**: Verify you’re in the correct directory when starting the Pydoc server, as it serves modules from the current working directory.

For further assistance, refer to the [Pydoc documentation](https://docs.python.org/3/library/pydoc.html) or [Wget manual](https://www.gnu.org/software/wget/manual/wget.html), or open an issue in this repository.

## License
This project is licensed under the [MIT License](LICENSE). See the `LICENSE` file for details.
