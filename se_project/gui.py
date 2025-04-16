import tkinter as tk
from tkinter import filedialog
import subprocess
import markdown2
import webbrowser
import tempfile
import os

current_folder = ""

selected_folder = ""

def open_help_url():
    webbrowser.open("https://github.com/Marlu0/softies_project/blob/main/HELP.md")  # Replace with your help URL

def browse_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()
    folder_label.config(text="Current folder: " + selected_folder)

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
    if error:
        output_text_area.insert("1.0", error.decode("utf-8"))
    else:
        output_text_area.insert("1.0", output.decode("utf-8"))
    output_text_area.config(state=tk.DISABLED)

        # Update the response.md file
    try:
        response_md_path = os.path.join(os.path.dirname(__file__), "response.md")
        with open(response_md_path, "w", encoding="utf-8") as f:
            f.write(output.decode("utf-8"))
    except Exception as e:
        tk.messagebox.showerror("Error", f"Error writing to response.md: {e}")

# Create the main window
window = tk.Tk()
window.title("Chatbot UI")
window.configure(bg="lightblue")

# Create a menu bar
menubar = tk.Menu(window)

# Create a file menu
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Select Folder", command=browse_folder)

menubar.add_cascade(label="File", menu=filemenu)

menubar.add_command(label="Help", command=open_help_url)

# Blacklist functionality
def open_blacklist_window():
    blacklist_window = tk.Toplevel(window)
    blacklist_window.title("Blacklist")

    # Listbox to display blacklisted items
    blacklist_listbox = tk.Listbox(blacklist_window, width=50)
    blacklist_listbox.pack(pady=10)

    # Button to add selected files/folders to the blacklist
    def add_to_blacklist():
        selected_items = filedialog.askopenfilenames()  # Allow multiple file selection
        for item in selected_items:
            blacklist_listbox.insert(tk.END, item)

    add_button = tk.Button(blacklist_window, text="Add to Blacklist", command=add_to_blacklist)
    add_button.pack(pady=5)

    # Button to remove selected items from the blacklist
    def remove_from_blacklist():
        selected_indices = blacklist_listbox.curselection()
        for index in reversed(selected_indices):  # Iterate in reverse to avoid index issues
            blacklist_listbox.delete(index)

    remove_button = tk.Button(blacklist_window, text="Remove from Blacklist", command=remove_from_blacklist)
    remove_button.pack(pady=5)

    # Store the blacklist in a variable (you might want to save this to a file later)
    def get_blacklist():
        blacklist = []
        for i in range(blacklist_listbox.size()):
            blacklist.append(blacklist_listbox.get(i))
        return blacklist

    # Example usage: Print the blacklist to the console
    def print_blacklist():
        blacklist = get_blacklist()
        print("Blacklist:", blacklist)

    print_button = tk.Button(blacklist_window, text="Print Blacklist", command=print_blacklist)
    print_button.pack(pady=5)

    # Save the blacklist to a file
    def save_blacklist():
        blacklist = get_blacklist()
        blacklist_path = os.path.join(os.path.dirname(__file__), "blacklist.txt")
        with open(blacklist_path, "w", encoding="utf-8") as f:
            for item in blacklist:
                f.write(item + "\n")
        tk.messagebox.showinfo("Blacklist", "Blacklist saved to blacklist.txt")
        blacklist_window.destroy()

    save_button = tk.Button(blacklist_window, text="Save Blacklist", command=save_blacklist)
    save_button.pack(pady=5)

    # Save the blacklist when the window is closed
    blacklist_window.protocol("WM_DELETE_WINDOW", save_blacklist)

# Add Blacklist option to the File menu
filemenu.add_command(label="Blacklist", command=open_blacklist_window)

# Add the menu bar to the window
window.config(menu=menubar)

folder_label = tk.Label(window, text="Current folder: ")
folder_label.pack(side=tk.TOP)

# Prompt Text Area
prompt_label = tk.Label(window, text="Prompt:")
prompt_label.pack(anchor=tk.W)

prompt_text_area = tk.Text(window, height=10, width=50)
prompt_text_area.pack()

# Send Button
send_button = tk.Button(window, text="Send Prompt", command=send_prompt, bg="white", fg="green")
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
display_button = tk.Button(window, text="Display Markdown", command=display_markdown,  bg="white", fg="green")
display_button.pack()

window.mainloop()
