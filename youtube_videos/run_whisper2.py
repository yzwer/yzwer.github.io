# -*- coding: utf-8 -*-
"""Run Whisper on cUwEpv2EGaQ.wav"""
import subprocess, sys, os

wav = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cUwEpv2EGaQ.wav')
cmd = [
    'whisper', wav,
    '--model', 'base',
    '--language', 'zh',
    '--output_format', 'json',
    '--output_dir', os.path.dirname(os.path.abspath(__file__))
]
print(f'Running: {" ".join(cmd)}')
sys.stdout.flush()
result = subprocess.run(cmd, capture_output=False, text=True)
print(f'Whisper exited with code: {result.returncode}')
