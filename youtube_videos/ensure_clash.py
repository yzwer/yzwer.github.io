#!/usr/bin/env python3
"""
确保 Clash 代理可用：
1. 检测 7890(mixed-port)/6789(socks)/1080 端口
2. 若全部不通，杀掉 clash-ninja 进程并重启（显式指定配置文件）
3. 等待端口就绪（最多 120 秒）
成功时【只输出端口号】到 stdout，其余日志全部打 stderr。
"""
import os
import sys
import time
import socket
import subprocess
from pathlib import Path

CLASH_EXE = r"D:\Program Files\Clash V-Ninja\clash-ninja.exe"
CONFIG_PATH = os.path.expanduser(r"~\.config\clash\config.yaml")
PORTS_TO_TRY = [7890, 6789, 1080, 7891, 8080]

def is_port_open(port, timeout=3):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex(('127.0.0.1', port)) == 0
    except Exception:
        return False

def find_open_port():
    for port in PORTS_TO_TRY:
        if is_port_open(port):
            return port
    return None

def kill_clash():
    for name in ['clash-ninja.exe', 'clash-ninja-service.exe']:
        try:
            subprocess.run(f'taskkill /F /IM "{name}" >NUL 2>NUL', shell=True, timeout=10)
        except Exception:
            pass
    time.sleep(2)

def start_clash():
    if not Path(CLASH_EXE).exists():
        print(f"[ERROR] Clash exe not found: {CLASH_EXE}", file=sys.stderr)
        return False
    clash_dir = os.path.dirname(CLASH_EXE)
    args = [CLASH_EXE]
    if Path(CONFIG_PATH).exists():
        args += ["-f", CONFIG_PATH]
        print(f"[Clash] Using config: {CONFIG_PATH}", file=sys.stderr)
    else:
        print(f"[WARN] Config not found: {CONFIG_PATH}", file=sys.stderr)
    subprocess.Popen(
        args,
        shell=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=clash_dir
    )
    print(f"[Clash] Started {CLASH_EXE}", file=sys.stderr)
    return True

def ensure_clash(timeout=120):
    port = find_open_port()
    if port:
        sys.stdout.write(str(port) + "\n")
        sys.stdout.flush()
        return port

    print("[Clash] All proxy ports down, restarting...", file=sys.stderr)
    kill_clash()
    if not start_clash():
        return None

    t0 = time.time()
    while time.time() - t0 < timeout:
        port = find_open_port()
        if port:
            elapsed = int(time.time() - t0)
            print(f"[Clash] Recovered on port {port} (took {elapsed}s)", file=sys.stderr)
            sys.stdout.write(str(port) + "\n")
            sys.stdout.flush()
            return port
        time.sleep(3)

    print(f"[Clash] ERROR: Proxy still down after {timeout}s", file=sys.stderr)
    return None

if __name__ == '__main__':
    try:
        port = ensure_clash()
        print(f"[DEBUG] ensure_clash returned: {port!r}", file=sys.stderr)
        sys.exit(0 if port else 1)
    except Exception as e:
        print(f"[FATAL] {e}", file=sys.stderr)
        sys.exit(2)
