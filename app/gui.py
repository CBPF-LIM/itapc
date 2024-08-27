try:
    import tkinter as tk
except ImportError:
    print("Tkinter is not installed. Please install Tkinter to use this application.")
    exit()

import tkinter.messagebox as msgbox
from tkinter import simpledialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os
import signal
import time

class ExitDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="What to do with the server?").grid(row=0, column=0, columnspan=2)
        return None

    def buttonbox(self):
        box = tk.Frame(self)

        # Custom buttons
        tk.Button(box, text="Kill", width=10, command=lambda: self.custom_response("kill")).grid(row=0, column=0)
        tk.Button(box, text="Keep running", width=10, command=lambda: self.custom_response("keep")).grid(row=0, column=1)
        tk.Button(box, text="Cancel", width=10, command=lambda: self.custom_response("cancel")).grid(row=0, column=2)

        box.pack()

    def custom_response(self, response):
        self.result = response
        self.destroy()

class FileMonitor(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        if event.src_path.endswith('data.csv'):
            self.callback()

class ITAPCGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ITAPC GUI")

        self.pid_file = 'itapc_server.pid'

        self.pid = None

        # Create a Canvas for scrolling
        self.canvas = tk.Canvas(self, borderwidth=0, width=600, height=400)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a Scrollbar for the Canvas
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a Frame to hold the grid of labels
        self.grid_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.grid_frame, anchor='nw')

        # Configure Canvas and Scrollbar
        self.grid_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Bind mouse wheel event to the canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)  # Windows
        self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)    # Linux
        self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)    # Linux

        # Create a button to start the process
        self.run_button = tk.Button(self, text="Run server", command=self.start_server)
        self.run_button.pack()

        # Initial file position
        self.file_position = 0

        # exit mode, for the buttons
        self.exit_mode = "keep"

        # Create a button to exit the application and kill the server
        self.exit_button = tk.Button(self, text="Exit", command=self.exit_button)
        self.exit_button.pack()

        self.process = None
        self.file_observer = None

        # Default width and specific column widths
        self.default_width = 10
        self.column_widths = [20, 7, 7]  # Customize as needed

        # To store the number of columns
        self.num_cols = 0
        # To store the row index for the next new row
        self.row_index = 0

        # data.csv file exists:
        if os.path.exists('data.csv'):
            self.start_file_monitor()
            self.update_file_content()

        # Check if the server is already running. If running, do nothing. If not, start the server
        if os.path.exists(self.pid_file):
            with open(self.pid_file, 'r') as file:
                pid = file.read()
                remove_pid = False
                if pid:
                    if self.is_process_running(pid):
                        self.pid = int(pid)
                        self.run_button.config(state=tk.DISABLED)
                        msgbox.showinfo("Server running", "PID: " + pid)
                    else:
                        msgbox.showinfo("Server not running", "PID file found but server not running. Removing PID file.")
                        remove_pid = True

            if remove_pid:
                self.remove_pid_file()

    def server_is_running(self):
        if self.process or self.pid is not None:
            return True

    def start_server(self):
        # Start the ita server
        if self.process is None:
            self.process = subprocess.Popen(
                ["itapc"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                #["python", "-m", "app.main"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            print(self.process.pid)
            self.pid = int(self.process.pid)
            with open(self.pid_file, 'w') as file:
                file.write(str(self.pid))

            # disable button:
            self.run_button.config(state=tk.DISABLED)

            # Start file monitoring
            self.start_file_monitor()

    def start_file_monitor(self):
        # Initialize file monitoring
        event_handler = FileMonitor(self.update_file_content)
        self.file_observer = Observer()
        self.file_observer.schedule(event_handler, path='.', recursive=False)
        self.file_observer.start()

    def update_file_content(self):
        print('Updating file content')
        try:
            with open('data.csv', 'r') as file:
                # Move to the last known position
                file.seek(self.file_position)
                # Read new content
                new_content = file.read()
                if new_content:
                    # Process new content into rows and columns
                    rows = new_content.split('\n')
                    for row in rows:
                        if row.strip():  # Ignore empty rows
                            cols = row.split('\t')
                            self.num_cols = max(self.num_cols, len(cols))  # Update column count if needed
                            # Add new row to the grid frame
                            for col_index, col in enumerate(cols):
                                # Determine column width
                                col_width = self.column_widths[col_index] if col_index < len(self.column_widths) else self.default_width
                                # Create and place new labels
                                formatted_col = col.strip().strip('"')
                                label = tk.Label(self.grid_frame, text=formatted_col, borderwidth=1, relief='solid', width=col_width)
                                label.grid(row=self.row_index, column=col_index, sticky='nsew')
                                label.bind("<Button-1>", self.copy_text)

                            # Update the row index for the next new row
                            self.row_index += 1
                    # Update the file position
                    self.file_position = file.tell()
        except FileNotFoundError:
            pass

    def copy_text(self, event):
        # Copy the text of the clicked label to the clipboard
        label = event.widget
        self.clipboard_clear()
        self.clipboard_append(label.cget("text"))

    def on_frame_configure(self, event):
        # Update the Canvas scroll region to encompass the entire frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        # Windows
        if event.num == 4:  # Scroll up
            self.canvas.yview_scroll(-1, 'units')
        elif event.num == 5:  # Scroll down
            self.canvas.yview_scroll(1, 'units')
        else:  # For Mac and other platforms
            # Scroll units depend on the platform
            scroll_units = -event.delta // 120 if event.delta else -1
            self.canvas.yview_scroll(scroll_units, 'units')

    def kill_server(self):
        if self.process:
            # The server was booted up by the process. Terminate the process
            self.process.terminate()
            self.process.wait()
            self.process = None
        elif self.pid is not None:
            # The server was already running. Use the PID to kill the process
            os.kill(self.pid, signal.SIGTERM)
            while self.is_process_running(self.pid):
                time.sleep(0.1)
                pass

        self.remove_pid_file()

    def stop_file_monitor(self):
        # Stop the file monitor
        if self.file_observer:
            self.file_observer.stop()
            self.file_observer.join()
            self.file_observer = None

    def exit_and_kill(self):
        # Stop the ita server and file monitor
        self.exit_mode = "kill"
        self.kill_server()
        self.stop_file_monitor()
        self.destroy()

    def exit_and_keep(self):
        # Stop the file monitor
        self.exit_mode = "keep"
        self.stop_file_monitor()
        self.destroy()

    def exit_button(self):
        if self.server_is_running():
            dialog = ExitDialog(self)
            if dialog.result == "kill":
                response = msgbox.askyesnocancel("Kill server", f"Are you sure you want to kill the server?")
                if response:
                    self.exit_and_kill()

            elif dialog.result == "keep":
                self.exit_and_keep()
        else:
            self.exit_and_keep()

    def on_exit(self):
        self.exit_and_keep()

    def is_process_running(self, pid):
        try:
            os.kill(int(pid), 0)
            return True
        except OSError:
            return False

    def remove_pid_file(self):
        if os.path.exists(self.pid_file):
            os.remove(self.pid_file)

def main():
    app = ITAPCGUI()
    app.protocol("WM_DELETE_WINDOW", app.on_exit)  # Handle window close
    app.mainloop()

if __name__ == "__main__":
    main()
