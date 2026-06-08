import cv2
import numpy as np
from pathlib import Path

out = Path('temp_test.mp4')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter(str(out), fourcc, 10.0, (320, 240))
for i in range(5):
    frame = np.full((240, 320, 3), 255, dtype=np.uint8)
    cv2.putText(frame, 'test', (80, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    writer.write(frame)
writer.release()
print('created', out, out.exists(), out.stat().st_size)
