import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import warnings
import time
import threading

warnings.filterwarnings("ignore")

class Notepad:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Notepad 2.0")
        
        # Optionally set the icon
        if sys.platform.startswith('win'):
            try:
                self.root.wm_iconbitmap('text-editor-logo.ico')
            except tk.TclError:
                pass  # Handle the case where setting the icon fails

        
        # Get the root geometry by itself from user window size
        width = self.root.winfo_screenwidth() - 100
        height = self.root.winfo_screenheight() - 100
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(True, True)
        self.root.configure(background="white")

        # Handle the window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Text area
        self.text_area = ctk.CTkTextbox(self.root, wrap='word', undo=True, font=("Arial", 14))
        self.text_area.pack(expand=1, fill='both')

        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.close)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Text font and size control
        self.text_font = tk.StringVar(value="Arial")
        self.text_size = tk.IntVar(value=14)

    
        
        # Font menu
        self.text_font_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.text_font_menu.add_radiobutton(label="Arial", variable=self.text_font, value="Arial", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Courier New", variable=self.text_font, value="Courier New", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Century Gothic", variable=self.text_font, value="Century Gothic", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Calibri", variable=self.text_font, value="Calibri", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Candara", variable=self.text_font, value="Candara", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Cambria", variable=self.text_font, value="Cambria", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Consolas", variable=self.text_font, value="Consolas", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Constantia", variable=self.text_font, value="Constantia", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Corbel", variable=self.text_font, value="Corbel", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Ebrima", variable=self.text_font, value="Ebrima", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Comic Sans MS", variable=self.text_font, value="Comic Sans MS", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Gill Sans", variable=self.text_font, value="Gill Sans", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Helvetica", variable=self.text_font, value="Helvetica", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Impact", variable=self.text_font, value="Impact", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Franklin Gothic Medium", variable=self.text_font, value="Franklin Gothic Medium", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Geneva", variable=self.text_font, value="Geneva", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Lucida Console", variable=self.text_font, value="Lucida Console", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Lucida Sans", variable=self.text_font, value="Lucida Sans", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Optima", variable=self.text_font, value="Optima", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Times New Roman", variable=self.text_font, value="Times New Roman", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Tahoma", variable=self.text_font, value="Tahoma", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Trebuchet MS", variable=self.text_font, value="Trebuchet MS", command=self.update_font)
        self.text_font_menu.add_radiobutton(label="Verdana", variable=self.text_font, value="Verdana", command=self.update_font)

        self.menu_bar.add_cascade(label="Font", menu=self.text_font_menu)

        # Text size menu
        self.text_size_menu = tk.Menu(self.menu_bar, tearoff=0)
        for size in range(8, 33, 2):
            self.text_size_menu.add_radiobutton(label=str(size), variable=self.text_size, value=size, command=self.update_font)
        self.menu_bar.add_cascade(label="Size", menu=self.text_size_menu)
        
        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Find", accelerator="Ctrl+F", command=self.find)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # undo menu redo menu cleanup text editor 
        self.undo_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.undo_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.undo)
        self.menu_bar.add_cascade(label="Undo", menu=self.undo_menu)
        self.redo_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.redo_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.redo)
        self.menu_bar.add_cascade(label="Redo", menu=self.redo_menu)
        # clear editor 
        self.clear_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.clear_menu.add_command(label=" Erase All Text ", accelerator="Ctrl+A+Delete", command=self.clear_editor)
        self.menu_bar.add_cascade(label="Clear Text", menu=self.clear_menu)

        # Print menu
        self.print_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.print_menu.add_command(label="Print", accelerator="Ctrl+P", command=self.print_file)
        self.menu_bar.add_cascade(label="Print", menu=self.print_menu)
        
        # View menu for dark mode
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.dark_mode = tk.BooleanVar()
        self.view_menu.add_checkbutton(label="Dark Mode", variable=self.dark_mode, command=self.toggle_dark_mode)
        self.menu_bar.add_cascade(label="Theme", menu=self.view_menu)

    
         
        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        #contact menu
        self.contact_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.contact_menu.add_command(label="Contact Us", command=self.contact)
        self.menu_bar.add_cascade(label="Contact Us", menu=self.contact_menu)

        self.root.config(menu=self.menu_bar)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ln 1, Col 1", anchor='e')
        self.status_bar.pack(side='bottom', fill='x')
        self.text_area.bind('<KeyRelease>', self.update_status_bar)
        
        self.file_path = None

        # Start auto-save thread
        self.auto_save_interval = 60  # Auto-save every 60 seconds
        self.auto_save_thread = threading.Thread(target=self.auto_save)
        self.auto_save_thread.daemon = True
        self.auto_save_thread.start()
        
        self.root.mainloop()
    
    def new_file(self, event=None):
        self.file_path = None
        self.text_area.delete(1.0, ctk.END)
        self.update_status_bar()
    
    def open_file(self, event=None):
        self.file_path = filedialog.askopenfilename(defaultextension=".txt",
                                                    filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.file_path:
            self.text_area.delete(1.0, ctk.END)
            with open(self.file_path, "r") as file:
                self.text_area.insert(1.0, file.read())
            self.update_status_bar()
    
    def save_file(self, event=None):
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                          filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get(1.0, ctk.END))
         
    def find(self):
        find_window = tk.Toplevel(self.root)
        find_window.title("Find")
        find_window.geometry("300x100")
        find_window.resizable(False, False)
        
        tk.Label(find_window, text="Find:").pack(side=tk.LEFT, padx=10, pady=10)
        
        self.find_entry = tk.Entry(find_window)
        self.find_entry.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Button(find_window, text="Find", command=self.find_text).pack(side=tk.LEFT, padx=10, pady=10)
    
    def find_text(self):
        start_pos = '1.0'
        key = self.find_entry.get()
        
        # Clear previous highlights
        self.text_area.tag_remove('highlight', '1.0', tk.END)
        
        if key:
            while True:
                start_pos = self.text_area.search(key, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(key)}c"
                self.text_area.tag_add('highlight', start_pos, end_pos)
                start_pos = end_pos  # Move past the last found position
            
            # Configure the highlight tag
            self.text_area.tag_config('highlight', foreground='white', background='blue')

    
    def close(self, event=None):
        self.root.destroy()
    
    def about(self):
        messagebox.showinfo("About", "Notepad 2.0 Application Developed by Ankit Tejwan")

    def contact(self, event=None):
        messagebox.showinfo("Contact Us", "Add Innovations Pvt Ltd First Floor, Plot No.78, Ecotech-2,Udyog Vihar ExtensionGreater Noida, UP 201306 \n+91 8375820921 info@addinnovations.in ")

    def print_file(self, event=None):
        try:
            # Try using the built-in os.startfile() method for printing (works on Windows)

            if os.name == 'nt':
                os.startfile(self.file_path, "print")
            else:
                messagebox.showinfo("Print", "Printing is not supported on this operating system")
        except Exception as e:
            messagebox.showerror("Print", f"Failed to print the file: {e} \n First you should save the file and Try Again...|")
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to save your work before quitting?"):
            self.save_file()
        self.root.destroy()
    
    # Clear the text editor when the user clicks on clear editor button
    def clear_editor(self, event=None):
        self.text_area.delete(1.0, ctk.END)
        self.update_status_bar()
    
    def undo(self, event=None):
        self.text_area.edit_undo()
    
    def redo(self, event=None):
        self.text_area.edit_redo()
    
    def cut(self, event=None):
        self.text_area.event_generate("<<Cut>>")
    
    def copy(self, event=None):
        self.text_area.event_generate("<<Copy>>")
    
    def paste(self, event=None):
        self.text_area.event_generate("<<Paste>>")
    
    def select_all(self, event=None):
        self.text_area.tag_add(tk.SEL, "1.0", ctk.END)
    
    def update_status_bar(self, event=None):
        row, col = self.text_area.index(tk.INSERT).split('.')
        text = self.text_area.get(1.0, ctk.END)
        word_count = len(text.split())
        char_count = len(text)
        self.status_bar.config(text=f"Ln {row}, Col {col} | Words: {word_count} | Characters: {char_count}")

    def toggle_dark_mode(self):
        if self.dark_mode.get():
            self.root.configure(background="black")
            self.text_area.configure(fg_color="black", text_color="white")
            self.status_bar.configure(background="black", foreground="white")
        else:
            self.root.configure(background="white")
            self.text_area.configure(fg_color="white", text_color="black")
            self.status_bar.configure(background="white", foreground="black")

    def update_font(self):
        self.text_area.configure(font=(self.text_font.get(), self.text_size.get()))

    

    def auto_save(self):
        while True:
            time.sleep(self.auto_save_interval)
            if self.file_path:
                with open(self.file_path, "w") as file:
                    file.write(self.text_area.get(1.0, ctk.END))
                print("Auto-saved at", time.strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    Notepad()
