from ultralytics import YOLO
import pathlib

print('models exists', pathlib.Path('models').exists())
print('best.pt exists', pathlib.Path('models/best.pt').exists())
try:
    m = YOLO('models/best.pt')
    print('YOLO load ok', type(m))
except Exception:
    import traceback
    traceback.print_exc()
