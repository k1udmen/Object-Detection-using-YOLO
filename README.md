# Real-time Detection & Counting (YOLO + FastAPI)

This repository contains a computer vision project developed during an industrial internship. 
The goal of the project was to design a real-time system for detecting and counting industrial valves from live video streams under different environmental conditions
It captures frames from a camera/video source, crops a fixed ROI, performs inference, counts valves, saves screenshots, and sends results to an API.

## Important Note
Some file paths in the code are currently defined using local Windows paths.
Before running the project on a different machine, please update the paths (model path, camera source,and output directories) according to your  setup.


## Project Structure
- `main.py` – FastAPI service and main runtime loop
- `predict.py` – ROI crop, preprocess, YOLO inference, postprocess, counting
- `camera.py` – OpenCV capture wrapper
- `helper.py` – API communication + timestamp helper
- `schema/` – request schema (Pydantic model)
- `config/` – configuration files (`config.example.ini`)
- `weights/` – model weights folder (model would be here)
- `ss_folder/` – screenshots output folder 

## Setup
1) Create a virtual environment 
```bash
conda activate env
pip install -r requirements.txt
python main.py
