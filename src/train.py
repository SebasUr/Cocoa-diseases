# This is intended to be running in a cluster environment with at least 1 GPU and 16 cores.
DATA_ROOT = "../data/COCOA_DATASET_CLEAN"
DATA_YAML = os.path.join(DATA_ROOT, "data.yaml")

# 1) Load pre-trained model, e.g., YOLOv8n, yolo11n.pt
model = YOLO("yolo11x.pt")

# 2) Train
model.train(
    data=DATA_YAML,
    epochs=80,
    imgsz=640,
    batch=16,
    name="cocoa_detect_v1",
    device='cuda'
)
