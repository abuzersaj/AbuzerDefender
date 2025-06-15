import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import logging

class DefenderGUI:
    def __init__(self, master):
        self.master = master
        master.title("AbuzerDefender AI")
        master.geometry("600x400")
        
        self.log_area = scrolledtext.ScrolledText(master, state='disabled', font=('Courier', 10))
        self.log_area.pack(expand=True, fill='both')
        
        self.start_button = tk.Button(master, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(pady=5)
        
        # Setup logger to write to GUI
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.log_handler = logging.StreamHandler(self)
        logging.getLogger().addHandler(self.log_handler)

    def write(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message)
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def flush(self):
        pass

    def start_monitoring(self):
        # Run your existing abuzer_defender.py functions in a thread here.
        self.start_button.config(state='disabled')
        threading.Thread(target=self.monitor, daemon=True).start()

    def monitor(self):
        while True:
            # Simulate log messages or connect to your main logic
            logging.info("Monitoring active...")
            time.sleep(5)

if __name__ == "__main__":
    root = tk.Tk()
    gui = DefenderGUI(root)
    root.mainloop()
