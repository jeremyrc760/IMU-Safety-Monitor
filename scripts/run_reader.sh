#!/bin/bash
cd ../backend
source .venv/bin/activate
export API_BASE="http://127.0.0.1:5000"
python mpu6050_reader.py
