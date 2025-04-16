import tkinter as tk
from tkinter import filedialog
import subprocess
import markdown2
import webbrowser
import tempfile
import os

selected_folder = ""

def open_help_url():
    webbrowser.open("https://www.example.com/help")  # Replace with your help URL

def browse_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()

def send_prompt():
    global selected_folder
    prompt = prompt_text_area.get("1.0", tk.END)
    
    if not selected_folder:
        tk.messagebox.showerror("Error", "Please select a folder first.")
        return

    # Call the context_creator.py script with the folder path and prompt
    command = ["python", "context_creator.py", selected_folder, prompt]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Display the output in the output_text_area
    output_text_area.config(state=tk.NORMAL)
    output_text_area.delete("1.0", tk.END)
    output_text_area.insert("1.0", output.decode("utf-8"))
    output_text_area.config(state=tk.DISABLED)

    # Update the response.md file
    try:
        with open("response.md", "w", encoding="utf-8") as f:
            f.write(output.decode("utf-8"))
    except Exception as e:
        tk.messagebox.showerror("Error", f"Error writing to response.md: {e}")

# Create the main window
window = tk.Tk()
window.title("Chatbot UI")
window.configure(bg="lightblue")

# Folder Path Selection
browse_button = tk.Button(window, text="Select Folder", command=browse_folder)
browse_button.pack(side=tk.TOP)

# Help Button
help_button = tk.Button(window, text="Help", command=open_help_url)
help_button.pack(side=tk.TOP)

# Prompt Text Area
prompt_label = tk.Label(window, text="Prompt:")
prompt_label.pack(anchor=tk.W)

prompt_text_area = tk.Text(window, height=10, width=50)
prompt_text_area.pack()

# Send Button
send_button = tk.Button(window, text="Send Prompt", command=send_prompt, bg="white", fg="blue")
send_button.pack()

def display_markdown():
    try:
        with open("response.md", "r", encoding="utf-8") as f:
            markdown_content = f.read()
        html_content = markdown2.markdown(markdown_content)

        # Create a temporary HTML file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        temp_file.write(html_content.encode("utf-8"))
        temp_file.close()

        # Open the HTML file in the default web browser
        webbrowser.open("file://" + temp_file.name)
    except Exception as e:
        print(f"Error: {e}")
        tk.messagebox.showerror("Error", str(e))

# Output Text Area
output_label = tk.Label(window, text="Output:")
output_label.pack(anchor=tk.W)

output_text_area = tk.Text(window, height=10, width=50, state=tk.DISABLED)
output_text_area.pack()

# Button to display markdown
display_button = tk.Button(window, text="Display Markdown", command=display_markdown,  bg="white", fg="blue")
display_button.pack()

window.mainloop()
