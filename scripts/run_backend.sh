#!/bin/bash
cd ../backend
source .venv/bin/activate || python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python transferlog_api.py
