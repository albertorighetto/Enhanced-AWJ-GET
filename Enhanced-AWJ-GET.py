import tkinter as tk
from tkinter import scrolledtext
import threading
import socket
from datetime import datetime
import webbrowser

# Define the TCP port
TCP_PORT = 10606

class TCPGuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced AWJ-GET - v1.0")
        self.root.geometry("1300x450")
        self.root.configure(bg="#393939")
        # Base64 encoded image data
        # Your base64-encoded PNG icon string (example with a tiny red dot PNG)
        icon_base64 = """
        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"        
        """

        # Decode base64, create PhotoImage, and set as iconphoto
        icon_image = tk.PhotoImage(data=icon_base64)
        root.iconphoto(True, icon_image)

        # Connection Section
        self.connection_frame = tk.Frame(root, bg="#393939")
        self.connection_frame.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.ip_entry = tk.Entry(self.connection_frame, bg="#282b40", fg="#ffffff", insertbackground="#282b40", font=("Arial", 14), justify="center")
        self.ip_entry.insert(0, "192.168.2.140")  # Default IP
        self.ip_entry.pack(pady=(10, 10), padx=5)

        button_frame = tk.Frame(self.connection_frame, bg="#393939")
        button_frame.pack(pady=(0, 10))

        self.connect_button = tk.Button(button_frame, text="Connect", bg="#ffffff", fg="#000000", width=10, command=self.start_tcp_client)
        self.connect_button.bind("<Button-1>", lambda e: self.connect_button.focus_set())
        self.connect_button.pack(side="left", padx=(0, 5))

        self.disconnect_button = tk.Button(button_frame, text="Disconnect", bg="#ffffff", fg="#000000", width=10, command=self.disconnect_tcp_client)
        self.disconnect_button.bind("<Button-1>", lambda e: self.disconnect_button.focus_set())
        self.disconnect_button.pack(side="left", padx=(5, 0))

        # Auto Scroll Checkbox
        self.auto_scroll_var = tk.BooleanVar(value=True)
        self.auto_scroll_checkbox = tk.Checkbutton(
            self.connection_frame, text="Auto scroll messages", variable=self.auto_scroll_var,
            bg="#393939", fg="#ffffff", activebackground="#196ebf", activeforeground="#B9C6AE",
            selectcolor="#757083"
        )
        self.auto_scroll_checkbox.pack(pady=(10, 10), padx=5)

        # Filters Section
        self.filters_label = tk.Label(self.connection_frame, text="Filter out (remove)", fg="#ffffff", bg="#393939", font=("Arial", 16))
        self.filters_label.pack(pady=(10, 5))

        self.filter_vars = {
            "Subscriptions": tk.BooleanVar(value=True),
            "Temperature": tk.BooleanVar(value=True),
            #"Duplicate answers": tk.BooleanVar(),
            #"Debug": tk.BooleanVar(),
            "Timer": tk.BooleanVar(value=True)
        }

        for text, var in self.filter_vars.items():
            tk.Checkbutton(
                self.connection_frame, text=text, variable=var,
                bg="#393939", fg="#ffffff", activebackground="#196ebf", activeforeground="#B9C6AE",
                selectcolor="#757083", command=lambda v=var, t=text: self.on_filter_change(v, t)
            ).pack(anchor="w", padx=20)

        self.match_clear_button = tk.Button(
            self.connection_frame, text="Clear all messages", bg="#ffffff", fg="#000000",
            command=self.clear_all_messages,
        )
        self.match_clear_button.pack(pady=(10, 0))
        self.match_clear_button.config(width=20)

        # Add note with clickable link
        self.note_label = tk.Label(
            self.connection_frame, text="Written by Alberto Righetto (arighetto88@gmail.com)\n" \
            "Source code on GitHub at\n" \
            "https://github.com/albertorighetto/enhanced-awj-get\n" \
            "\n" \
            "This software is not affiliated with,\n" \
            "endorsed by, or supported by Analog Way",
            fg="#ffffff", bg="#393939", font=("Arial", 10), cursor="hand2", justify="center"
        )
        self.note_label.bind("<Button-1>", lambda e: self.open_github_link())
        self.note_label.pack(side="bottom", pady=(10, 0))

        # Messages Section
        self.console_frame = tk.Frame(root, bg="#393939")
        self.console_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        filter_line_frame = tk.Frame(self.console_frame, bg="#393939")
        filter_line_frame.pack(fill="x", pady=1)

        # Match text section
        self.match_label = tk.Label(filter_line_frame, text="Match text:", fg="#FFFFFF", bg="#393939")
        self.match_label.pack(side="left", padx=(0, 10))

        self.match_entry = tk.Entry(filter_line_frame, bg="#282b40", fg="#FFFFFF", insertbackground="#282b40")
        self.match_entry.bind("<FocusIn>", lambda e: self.match_entry.configure(bg="#f5a936", fg="#000000"))
        self.match_entry.bind("<FocusOut>", lambda e: self.match_entry.configure(bg="#282b40", fg="#FFFFFF"))
        self.match_entry.pack(side="left", fill="x", expand=True)
        self.match_entry.bind("<KeyRelease>", self.refresh_filter)

        self.match_clear_button = tk.Button(filter_line_frame, text="Clear", bg="#ffffff", fg="#000000", command=self.clear_match_filter)
        self.match_clear_button.pack(side="left", padx=(10, 0))

        self.match_case_sensitive_var = tk.BooleanVar(value=False)
        self.match_case_sensitive_checkbox = tk.Checkbutton(
            filter_line_frame, text="Case Sensitive", variable=self.match_case_sensitive_var,
            bg="#393939", fg="#ffffff", activebackground="#196ebf", activeforeground="#B9C6AE",
            selectcolor="#757083", command=self.refresh_filter
        )
        self.match_case_sensitive_checkbox.pack(side="left", padx=(10, 0))

        # Exclude text section
        exclude_line_frame = tk.Frame(self.console_frame, bg="#393939")
        exclude_line_frame.pack(fill="x", pady=1)

        self.exclude_label = tk.Label(exclude_line_frame, text="Exclude text:", fg="#FFFFFF", bg="#393939")
        self.exclude_label.pack(side="left", padx=(0, 10))

        self.exclude_entry = tk.Entry(exclude_line_frame, bg="#282b40", fg="#FFFFFF", insertbackground="#282b40")
        self.exclude_entry.bind("<FocusIn>", lambda e: self.exclude_entry.configure(bg="#f5a936", fg="#000000"))
        self.exclude_entry.bind("<FocusOut>", lambda e: self.exclude_entry.configure(bg="#282b40", fg="#FFFFFF"))
        self.exclude_entry.pack(side="left", fill="x", expand=True)
        self.exclude_entry.bind("<KeyRelease>", self.refresh_filter)

        self.exclude_clear_button = tk.Button(exclude_line_frame, text="Clear", bg="#ffffff", fg="#000000", command=self.clear_exclude_filter)
        self.exclude_clear_button.pack(side="left", padx=(10, 0))

        self.exclude_case_sensitive_var = tk.BooleanVar(value=False)
        self.exclude_case_sensitive_checkbox = tk.Checkbutton(
            exclude_line_frame, text="Case Sensitive", variable=self.exclude_case_sensitive_var,
            bg="#393939", fg="#ffffff", activebackground="#196ebf", activeforeground="#B9C6AE",
            selectcolor="#757083", command=self.refresh_filter
        )
        self.exclude_case_sensitive_checkbox.pack(side="left", padx=(10, 0))

        self.messages_area = scrolledtext.ScrolledText(
            self.console_frame, state='disabled', wrap='none', height=20, bg="#282b40", fg="#ffffff"
        )

        # Add right-click context menu for copy functionality
        self.messages_area.bind("<Button-3>", self.show_context_menu)
        self.context_menu = tk.Menu(self.messages_area, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_selected_text)

        # Add horizontal scrollbar
        self.h_scrollbar = tk.Scrollbar(self.console_frame, orient="horizontal", command=self.messages_area.xview)
        self.messages_area.configure(xscrollcommand=self.h_scrollbar.set)
        self.h_scrollbar.pack(fill="x", side="bottom", padx=2, pady=2)

        self.messages_area.pack(fill="both", expand=True, padx=2, pady=2)

        self.messages = []
        self.filtered_messages = []
        self.message_buffer = []
        self.update_pending = False
        self.client_socket = None

    def open_github_link(self):
        webbrowser.open("https://github.com/albertorighetto/enhanced-awj-get")    

    def clear_all_messages(self):
        self.messages = []
        self.filtered_messages = []
        self.messages_area.config(state='normal')
        self.messages_area.delete(1.0, tk.END)
        self.messages_area.config(state='disabled')
        self.append_console("All messages cleared.")
    
    def clear_match_filter(self):
        self.match_entry.delete(0, tk.END)
        self.refresh_filter()
    
    def clear_exclude_filter(self):
        self.exclude_entry.delete(0, tk.END)
        self.refresh_filter()
        
    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def copy_selected_text(self):
        try:
            selected_text = self.messages_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_text)
            self.root.update()  # Keeps the clipboard updated
        except tk.TclError:
            pass  # No text selected
    def start_tcp_client(self):
        ip = self.ip_entry.get()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client_socket.connect((ip, TCP_PORT))
            self.append_console(f"Connected to {ip}:{TCP_PORT}")
            self.ip_entry.configure(bg="#90ee90", fg="#000000") # Green color for success

            # Send the initial message
            initial_message = '{"op":"replace","path":"Subscriptions", "value":["DeviceObject"]}' + chr(4)
            self.client_socket.sendall(initial_message.encode('ascii'))

            threading.Thread(target=self.receive_tcp_messages, daemon=True).start()
        except Exception as e:
            self.append_console(f"Connection failed: {e}")
            self.ip_entry.configure(bg="#ff6565", fg="#000000") # Red color for error

    def disconnect_tcp_client(self):
        if self.client_socket:
            try:
                self.client_socket.close()
                self.append_console("Disconnected from server.")
                self.ip_entry.configure(bg="#ff6565", fg="#000000") # Red color for error
            except Exception as e:
                self.append_console(f"Error disconnecting: {e}")
            finally:
                self.client_socket = None
        else:
            self.append_console("No active connection to disconnect.")
    
    def receive_tcp_messages(self):
        try:
            while True:
                data = self.client_socket.recv(4096)
                if not data:
                    self.append_console("Connection closed by server.")
                    break
                messages = data.decode(errors="ignore").split(chr(4))  # Split messages based on EOT (ASCII 4)
                for message in messages:
                    message = message.strip()
                    if message:
                        self.messages.append(message)
                        if self.should_display_message(message, self.match_entry.get().strip(), self.exclude_entry.get().strip()):
                            self.append_console(message)
        except Exception as e:
            self.append_console(f"Error receiving data: {e}")
            self.ip_entry.configure(bg="#ff6565", fg="#000000") # Red color for error indication on Connect button

    def append_console(self, text):
            self.message_buffer.append(text + "\n")
            if not self.update_pending:
                self.update_pending = True
                if self.message_buffer:
                    self.root.after(100, self.update_console)
    
    def update_console(self):
        if str(self.messages_area.cget('state')) != 'normal':
            self.messages_area.config(state='normal')
        self.messages_area.insert(tk.END, ''.join(self.message_buffer))
        self.message_buffer.clear()
        if str(self.messages_area.cget('state')) != 'disabled':
            self.messages_area.config(state='disabled')
        if self.auto_scroll_var.get():
            self.messages_area.see(tk.END)
        self.update_pending = False

    def should_display_message(self, message, match_text, exclude_text):
        if self.filter_vars["Timer"].get() and "DeviceObject/$timer/@items/TIMER_" in message:
            return False
        if self.filter_vars["Temperature"].get() and "/temperature/control/@props/" in message:
            return False
        if self.filter_vars["Subscriptions"].get() and '{"path":"Subscriptions","value":' in message:
            return False
        if self.match_case_sensitive_var.get():
            if match_text in message and (not exclude_text or 
                (self.exclude_case_sensitive_var.get() and exclude_text not in message) or 
                (not self.exclude_case_sensitive_var.get() and exclude_text.lower() not in message.lower())):
                return True
        else:
            if match_text.lower() in message.lower() and (
                not exclude_text or 
                (self.exclude_case_sensitive_var.get() and exclude_text not in message) or 
                (not self.exclude_case_sensitive_var.get() and exclude_text.lower() not in message.lower())
            ):
                return True
        return False

    def refresh_filter(self, event=None):
        match_text = self.match_entry.get()
        exclude_text = self.exclude_entry.get()

        self.messages_area.config(state='normal')
        self.messages_area.delete(1.0, tk.END)

        # Apply the filter to the messages
        for message in self.messages:
            if self.should_display_message(message, match_text, exclude_text):
                self.append_console(message)
    
    def on_filter_change(self, var, text):
        #if var.get():
        #    self.append_console(f"Filtering out: {text}")
        #else:
        #    self.append_console(f"Not filtering out: {text}")
        self.refresh_filter()

# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = TCPGuiApp(root)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.mainloop()
