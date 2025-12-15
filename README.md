# Valf Analitik – Real-time Valve Detection & Counting (YOLO + FastAPI)

This project runs a real-time valve detection and counting pipeline using a trained YOLO model.
It captures frames from a camera/video source, crops a fixed ROI, performs inference, counts valves,
optionally saves evidence screenshots, and sends results to an external API.

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
