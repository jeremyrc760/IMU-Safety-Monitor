
# TransferLog (Raspberry Pi 5 + MPU6050)

Full-stack demo for reading MPU6050 sensor data on Raspberry Pi 5, exposing a Flask backend API, and a simple Chart.js frontend dashboard.

## Structure
- backend/
  - transferlog_api.py — Flask API
  - mpu6050_reader.py — I2C MPU6050 reader
  - requirements.txt — dependencies
- frontend/
  - index.html — simple dashboard
- scripts/
  - run_backend.sh, run_reader.sh

## Quickstart
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python transferlog_api.py
```

In another terminal:
```bash
cd backend
source .venv/bin/activate
export API_BASE="http://127.0.0.1:5000"
python mpu6050_reader.py
```
