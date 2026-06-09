import requests

url = 'http://127.0.0.1:8000/video-detect'
files = {'file': open('temp_test.mp4', 'rb')}
try:
    r = requests.post(url, files=files, timeout=120)
    print('status', r.status_code)
    print('text', r.text)
except Exception:
    import traceback
    traceback.print_exc()
finally:
    files['file'].close()
