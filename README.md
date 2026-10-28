# QRShield: Smart QR Code Safety Checker

**Team CipherX** | Akilandeshwari P, Atchaya S | SRM TRP Engineering College

QR codes hide their links, and attackers paste fake QR codes over real ones. QRShield checks the link inside a QR code before the user opens it and warns them if it looks unsafe.

## Features
- Scan a QR with the camera, or upload a QR image
- Risk score (0-100) with verdict: Safe, Suspicious or Dangerous
- Plain-language reasons
- Report this QR: reported links get a higher score next time
- Recent scans list

## Run locally
pip install -r requirements.txt
python app.py
Open http://localhost:5000

## Deploy (Render)
Build command: pip install -r requirements.txt
Start command: gunicorn app:app

## Tech stack
Python, Flask, HTML/CSS/JavaScript, html5-qrcode
