import tkinter as tk
from tkinter import filedialog
import threading
from pytube import YouTube
import pyperclip

# Check and install required dependencies
try:
    from pytube import YouTube
except ImportError:
    print("pytube library is not installed. Installing...")
    try:
        import pip
        pip.main(['install', 'pytube'])
        from pytube import YouTube
        print("pytube installed successfully!")
    except Exception as e:
        print(f"Error installing pytube: {str(e)}")
        exit(1)

try:
    import pyperclip
except ImportError:
    print("pyperclip library is not installed. Installing...")
    try:
        import pip
        pip.main(['install', 'pyperclip'])
        import pyperclip
        print("pyperclip installed successfully!")
    except Exception as e:
        print(f"Error installing pyperclip: {str(e)}")
        exit(1)

def download_video():
    url = entry.get()
    save_path = filedialog.askdirectory()

    # Function to perform the download
    def perform_download():
        try:
            yt = YouTube(url)
            yt_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

            if yt_stream:
                download_path = filedialog.asksaveasfilename(defaultextension=".mp4", initialfile=yt.title, initialdir=save_path)
                yt_stream.download(download_path)
                download_progress[0] = 100
                result_label.config(text="Download successful!", fg="green")
            else:
                result_label.config(text="No suitable stream found.", fg="red")
        except Exception as e:
            result_label.config(text=f"Error: {str(e)}", fg="red")
        finally:
            download_complete[0] = True

    # Create a thread for downloading
    download_thread = threading.Thread(target=perform_download)

    # Start the download thread
    download_thread.start()

def paste_clipboard():
    url_from_clipboard = pyperclip.paste()
    entry.delete(0, tk.END)  # Clear the entry
    entry.insert(0, url_from_clipboard)  # Paste the clipboard content into the entry

# Create the main window
root = tk.Tk()
root.title("MesaTech™")

# Set the window background to black
root.configure(bg="black")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size and position it at the center of the screen
window_width = 350
window_height = 250
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create and pack the GUI components with updated styles
label = tk.Label(root, text="Enter YouTube URL:", fg="white", bg="black")
label.pack(pady=10)

entry = tk.Entry(root, width=40, bg="white", fg="black")
entry.pack(pady=10)

# Create "Choose where file is saved" button
browse_button = tk.Button(root, text="Choose where file is saved", command=download_video, bg="grey", fg="white")
browse_button.pack(pady=window_height * 0.1)  # Move down by 10%

result_label = tk.Label(root, text="", fg="white", bg="black")
result_label.pack(pady=10)

# Variables to track download progress and completion
download_progress = [0]
download_complete = [False]

# Create "Paste Clipboard" button
paste_button = tk.Button(root, text="Paste Clipboard", command=paste_clipboard, bg="grey", fg="white")
paste_button.pack(pady=10)

# Start the GUI application
root.mainloop()
