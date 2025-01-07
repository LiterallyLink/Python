@echo off
pyinstaller --onefile ^
    --name "YouTube Downloader" ^
    --exclude-module tensorflow ^
    --exclude-module tensorflow_intel ^
    --exclude-module torch ^
    --exclude-module transformers ^
    --exclude-module keras ^
    --exclude-module sklearn ^
    --exclude-module huggingface_hub ^
    --exclude-module datasets ^
    --exclude-module safetensors ^
    --exclude-module langchain ^
    --exclude-module chainlit ^
    --exclude-module accelerate ^
    ytdownloader.py

echo Build complete! Check the dist folder.
pause