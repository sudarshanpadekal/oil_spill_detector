from ultralytics import YOLO
m = YOLO('models/best.pt')
print('task=', getattr(m, 'task', None))
print('overrides=', getattr(m, 'overrides', None))
print('model type=', type(m.model))
