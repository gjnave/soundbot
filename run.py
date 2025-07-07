
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os

class AppLauncher(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SOUNDBot Launcher")
        self.geometry("600x600")
        self.configure(bg="#F0F0F0")

        # Determine the base directory of the main SOUND-BOT application
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.soundbot_base_dir = script_dir

        print(f"DEBUG: Current Working Directory: {os.getcwd()}")
        print(f"DEBUG: Script Directory: {script_dir}")
        print(f"DEBUG: Calculated SOUND-BOT Base Directory: {self.soundbot_base_dir}")

        # --- Styles ---
        style = ttk.Style(self)
        style.configure("TLabel", background="#F0F0F0", font=("Helvetica", 10))
        style.configure("TButton", font=("Helvetica", 10, "bold"))
        style.configure("TFrame", background="#F0F0F0")

        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")

        # --- Model Selection ---
        self.llm_model = self.create_file_selector(main_frame, "LLM Model (.gguf)", os.path.join(self.soundbot_base_dir, "models/llm"), ".gguf")
        self.image_model = self.create_file_selector(main_frame, "Image Model (.safetensors)", os.path.join(self.soundbot_base_dir, "models/image"), ".safetensors")
        self.story_file = self.create_file_selector(main_frame, "Story File (.json)", os.path.join(self.soundbot_base_dir, "models/stories"), ".json", blank_option=True)

        # --- Options ---
        self.use_microphone = tk.BooleanVar()
        mic_check = ttk.Checkbutton(main_frame, text="Use Microphone", variable=self.use_microphone)
        mic_check.pack(pady=10, anchor="w")

        self.browsing_option = tk.StringVar(value="private")
        private_radio = ttk.Radiobutton(main_frame, text="SOUND (Private) w/ No Memory", variable=self.browsing_option, value="private")
        default_radio = ttk.Radiobutton(main_frame, text="Default Browsing (Ability to Save)", variable=self.browsing_option, value="default")
        private_radio.pack(anchor="w")
        default_radio.pack(anchor="w")

        # --- Launch Button ---
        launch_button = ttk.Button(main_frame, text="Launch SOUNDBot", command=self.launch_soundbot)
        launch_button.pack(pady=20, ipady=10, fill="x")

    def create_file_selector(self, parent, label_text, folder_path, extension, blank_option=False):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=5)

        label = ttk.Label(frame, text=label_text)
        label.pack(side="left", padx=(0, 10))

        variable = tk.StringVar()
        combobox = ttk.Combobox(frame, textvariable=variable)
        
        normalized_folder_path = os.path.normpath(folder_path)
        files = [f for f in os.listdir(normalized_folder_path) if f.endswith(extension)] if os.path.exists(normalized_folder_path) else []
        if blank_option:
            files.insert(0, "Blank Slate")
        combobox['values'] = files
        if files:
            combobox.current(0)

        combobox.pack(side="left", expand=True, fill="x")
        return variable

    def launch_soundbot(self):
        # Get the base directory of the main SOUND-BOT application
        script_dir = os.path.dirname(os.path.abspath(__file__))
        soundbot_base_dir = os.path.abspath(os.path.join(script_dir, os.pardir, "SOUND-BOT"))

        llm_model_path = os.path.normpath(os.path.join(self.soundbot_base_dir, "models/llm", self.llm_model.get())) if self.llm_model.get() else None
        print(f"DEBUG: soundbot_base_dir: {self.soundbot_base_dir}")
        print(f"DEBUG: llm_model_path: {llm_model_path}")
        print(f"DEBUG: os.path.exists(llm_model_path): {os.path.exists(llm_model_path)}")
        if not llm_model_path or not os.path.exists(llm_model_path):
            messagebox.showerror("Error", "Please select a valid LLM model.")
            return

        koboldcpp_path = os.path.normpath(os.path.join(self.soundbot_base_dir, "koboldcpp.exe"))
        print(f"DEBUG: koboldcpp_path: {koboldcpp_path}")

        command = [
            koboldcpp_path,
            "--model", llm_model_path,
            "--sdquant",
            "--gpulayers", "99",
            "--smartcontext",
            "--quiet",
            "--highpriority",
            "--usecublas",
            "--contextsize", "12288"
        ]

        if self.image_model.get():
            image_model_path = os.path.normpath(os.path.join(self.soundbot_base_dir, "models/image", self.image_model.get()))
            if os.path.exists(image_model_path):
                command.extend(["--sdmodel", image_model_path, "--mmproj", os.path.normpath(os.path.join(self.soundbot_base_dir, "models/image/llava/mmproj-model-f16.gguf"))])

        if self.story_file.get() and self.story_file.get() != "Blank Slate":
            story_file_path = os.path.normpath(os.path.join(self.soundbot_base_dir, "models/stories", self.story_file.get()))
            if os.path.exists(story_file_path):
                command.extend(["--preloadstory", story_file_path])

        if self.use_microphone.get():
            command.extend(["--whispermodel", os.path.normpath(os.path.join(self.soundbot_base_dir, r"models\audio\ggml-large-v3.bin"))])

        if self.browsing_option.get() == "private":
            browser_path = os.path.normpath(os.path.join(self.soundbot_base_dir, r"venv\Scripts\midori\private_browsing.exe"))
            command.extend(["--onready", f'{browser_path} http://localhost:5001'])

        try:
            subprocess.Popen(command)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch SOUNDBot: {e}")

if __name__ == "__main__":
    app = AppLauncher()
    app.mainloop()
