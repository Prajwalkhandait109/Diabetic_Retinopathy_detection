import requests
import os

URL = 'http://127.0.0.1:5000/predict'
IMAGE_PATH = os.path.join('sample_images', 'sample_0.png')

def run_test(model_name):
    if not os.path.exists(IMAGE_PATH):
        raise FileNotFoundError(f"Test image not found: {IMAGE_PATH}")
    with open(IMAGE_PATH, 'rb') as f:
        files = {
            'file': ('sample_0.png', f, 'image/png')
        }
        data = {
            'model': model_name
        }
        resp = requests.post(URL, files=files, data=data)
        print(f"Status: {resp.status_code}")
        print(resp.text)

if __name__ == '__main__':
    print('Testing model.h5...')
    run_test('model.h5')
    print('\nTesting custom_cnn.h5...')
    run_test('custom_cnn.h5')