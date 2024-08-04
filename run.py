import subprocess
import os

def choose_loader():
    while True:
        print("Choose a loader:")
        print("1: Classic Loader")
        print("2: SOUND Loader")
        choice = input("Enter the number of your choice: ").strip()
        if choice == '1':
            return "Classic"
        elif choice == '2':
            return "SOUND"
        else:
            print("Invalid choice. Please try again.")

loader_choice = choose_loader()

if loader_choice == "Classic":
    try:
        subprocess.run(["koboldcpp.exe"], check=True)
        print("Classic Loader executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing Classic Loader: {e}")
    exit()

url2 = "http://localhost:5001"
private_browser_path = r"venv\Scripts\midori\private_browsing.exe"
default_browser_path = ""

def list_files(folder, extension):
    return [f for f in os.listdir(folder) if f.endswith(extension)]

def choose_file(files, blank_option=False):
    if not files:
        print("No files found.")
        return None
    if len(files) == 1 and not blank_option:
        return files[0]
    print("\nChoose a file:\n")
    for idx, file in enumerate(files, start=1):
        print(f"{idx}: {file}")
    if blank_option:
        print(f"{len(files) + 1}: Blank Slate")
    while True:
        choice = input("Enter the number of the file you want to choose: ")
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            return files[int(choice) - 1]
        elif blank_option and choice == str(len(files) + 1):
            return "Blank Slate"
        else:
            print("Invalid choice. Please try again.")

def main(folder, extension, blank_option=False):
    files = list_files(folder, extension)
    chosen_file = choose_file(files, blank_option)
    if chosen_file and chosen_file != "Blank Slate":
        print(f"You chose: {chosen_file}\n")
    else:
        print("No file chosen or Blank Slate selected.")
    return chosen_file

def get_browsing_option():
    while True:
        print("Choose browsing option:")
        print("1: SOUND (Private) w/ No Memory")
        print("2: Default Browsing (Ability to Save)")
        choice = input("Enter the number of your choice: ").strip()
        if choice == '1':
            return private_browser_path
        elif choice == '2':
            return default_browser_path
        else:
            print("Invalid choice. Please try again.")

def get_microphone_option():
    while True:
        print("Do you want to use a microphone?")
        print("1: Yes")
        print("2: No")
        choice = input("Enter the number of your choice: ").strip()
        if choice == '1':
            return True
        elif choice == '2':
            return False
        else:
            print("Invalid choice. Please try again.")

# Example usage
llm_folder_path = "models/llm"  # Replace with your LLM folder path
selected_llm_file = main(llm_folder_path, '.gguf')

if selected_llm_file:
    selected_llm_file_path = os.path.join(llm_folder_path, selected_llm_file)
    load_image_model = input("Do you want to load an image model as well? (y/n): ").strip().lower()
    if load_image_model == 'y':
        image_folder_path = "models/image"  # Replace with your image folder path
        selected_image_file = main(image_folder_path, '.safetensors')
        if selected_image_file:
            selected_image_file_path = os.path.join(image_folder_path, selected_image_file)
        else:
            selected_image_file_path = None
    else:
        selected_image_file_path = None

    # Get browsing option
    browser_path = get_browsing_option()

    # Choose a story to preload with Blank Slate option
    story_folder_path = "models/stories"  # Replace with your stories folder path
    selected_story_file = main(story_folder_path, '.json', blank_option=True)

    if selected_story_file and selected_story_file != "Blank Slate":
        selected_story_file_path = os.path.join(story_folder_path, selected_story_file)
    else:
        selected_story_file_path = None

    # Get microphone option
    use_microphone = get_microphone_option()

    # Kobold config
    command = [
        "koboldcpp.exe",
        "--model",
        selected_llm_file_path,
        "--sdquant",
        "--gpulayers",
        "99",
        "--smartcontext",
        "--quiet",
        "--highpriority",
        "--usecublas",
        "--contextsize",
        "12288"
    ]

    if selected_story_file_path:
        command.extend(["--preloadstory", selected_story_file_path])

    if browser_path:
        command.extend(["--onready", f"{browser_path} {url2}"])

    # Add the image model parameter if selected
    if selected_image_file_path:
        command.insert(3, "--sdmodel")
        command.insert(4, selected_image_file_path)
        command.insert(5, "--mmproj")
        command.insert(6, "models/image/llava/mmproj-model-f16.gguf")

    # Add the whisper model parameter if microphone is used
    if use_microphone:
        command.extend(["--whispermodel", r"models\audio\ggml-large-v3.bin"])

    # Execute the command
    try:
        subprocess.run(command, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
else:
    print("No LLM model selected, command not executed.")
