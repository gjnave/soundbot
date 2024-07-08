@echo off

echo WARNING. For this auto installer to work you need to have installed Python 3.10.11 or 3.10.13 and C++ tools 
echo Follow this tutorial : https://youtu.be/-NjNy7afOQ0

pip install requests
pip install tqdm
git lfs install

REM Create SOUND-BOT subfolder
if not exist "SOUND-BOT" mkdir "SOUND-BOT"

REM Define array of URLs and corresponding filenames for downloads
setlocal EnableDelayedExpansion
set "downloads[0]=https://github.com/LostRuins/koboldcpp/releases/download/v1.65/koboldcpp.exe|SOUND-BOT\koboldcpp.exe"
set "downloads[1]=https://github.com/LostRuins/koboldcpp/releases/download/v1.65/koboldcpp_nocuda.exe|SOUND-BOT\koboldcpp_nocuda.exe"
set "downloads[8]=https://huggingface.co/Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix/resolve/main/L3-8B-Stheno-v3.2-IQ4_XS-imat.gguf?download=true|SOUND-BOT\L3_8b_Stheno.gguf"
set "downloads[3]=https://civitai.com/api/download/models/274807|SOUND-BOT\hybridRealityRealistic_hybridrealityV10.safetensors"
set "downloads[4]=https://huggingface.co/ChaoticNeutrals/LLaVA-Llama-3-8B-mmproj-Updated/resolve/main/llava-v1.5-8B-Updated-Stop-Token/mmproj-model-f16.gguf?download=true|SOUND-BOT\mmproj-model-f16.gguf"
set "downloads[5]=https://www.cognibuild.ai/wp-content/uploads/2024/05/aura1.png|SOUND-BOT\aura1.png"
set "downloads[6]=https://www.cognibuild.ai/wp-content/uploads/oneclick/saved_story.json|SOUND-BOT\saved_story.json|models\stories\Cognibrain.json"
set "downloads[7]=https://www.cognibuild.ai/wp-content/uploads/oneclick/midori.zip|SOUND-BOT\midori.zip"
set "downloads[2]=https://raw.githubusercontent.com/gjnave/cogni-scripts/main/SOUNDbot.py|SOUND-BOT\run.py" 

REM Download files with progress indication
for /L %%i in (0, 1, 8) do (
    for /F "tokens=1,2 delims=|" %%a in ("!downloads[%%i]!") do (
        echo Downloading %%b ...
        powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%%a', '%%b'); Write-Host 'Download complete.'"
    )
)

REM Unzip midori.zip if it exists
if exist "SOUND-BOT\midori.zip" (
    powershell -Command "Expand-Archive -Path 'SOUND-BOT\midori.zip' -DestinationPath 'SOUND-BOT\venv\Scripts' -Force"
    echo Unzipped Secure Browser
)

REM Show completion message
echo Virtual environment made and installed properly

REM Pause to keep the command prompt open
pause
