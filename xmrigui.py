#!/usr/bin/env python3

import os
import json
import sys
import re
import platform
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, 
                             QTextEdit, QTabWidget, QGridLayout, QGroupBox, QSystemTrayIcon, QMenu)
from PyQt6.QtCore import QProcess, Qt, pyqtSlot
from PyQt6.QtGui import QIcon, QTextCursor, QAction

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widgets = {}
        self.processes = {}
        self.load_data()
        self.config = self.get_config()
        self.init_ui()
        
        # Start mining if configured
        for profile in self.profiles:
            if self.config[profile].get('mine'):
                self.start_mining(profile, save=False)

    def get_config(self):
        if not os.path.exists(self.settings_path):
            with open(self.settings_path, 'w') as f:
                f.write(self.raw_config)
        try:
            with open(self.settings_path, 'r') as f:
                return json.load(f)
        except:
            return json.loads(self.raw_config)

    def start_mining(self, profile, save=True):
        if save:
            self.config[profile]['mine'] = True
            self.save_config()
        
        self.widgets[profile]['status_label'].setText('Status: Mining...')

        args = []
        if not self.config[profile]['default_args']:
            args.extend(['--algo', self.algos[self.config[profile]['coin']]])
            args.extend(['--url', self.config[profile]['pool']])
            args.extend(['--user', self.config[profile]['user']])
            args.extend(['--pass', self.config[profile]['password']])
            args.extend(['--donate-level', str(self.config[profile]['donate'])])
            if self.config[profile]['threads'] != '0':
                args.extend(['--threads', self.config[profile]['threads']])
            if self.config[profile]['cuda']: 
                args.extend(['--cuda', '--cuda-loader', self.cuda_plugin_path])
            if self.config[profile]['opencl']: args.append('--opencl')
            if not self.config[profile]['cpu']: args.append('--no-cpu')
        
        if self.config[profile]['args']:
            args.extend(self.config[profile]['args'].split())

        process = QProcess(self)
        process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        process.readyReadStandardOutput.connect(lambda p=profile: self.update_log(p))
        process.start(self.xmrig_path, args)
        self.processes[profile] = process
    
    def stop_mining(self, profile, save=True):
        if profile in self.processes:
            self.processes[profile].terminate()
            self.processes[profile].waitForFinished(2000)
            del self.processes[profile]

        # Windows global kill logic (as requested before)
        if platform.system() == 'Windows':
            os.system('taskkill /F /IM xmrig.exe /T')
        
        self.widgets[profile]['status_label'].setText('Status: Stopped.')
        if save:
            self.config[profile]['mine'] = False
            self.save_config()

    def save_config(self):
        for profile in self.profiles:
            self.config[profile]['pool'] = self.widgets[profile]['pool_entry'].text()
            self.config[profile]['user'] = self.widgets[profile]['user_entry'].text()
            self.config[profile]['password'] = self.widgets[profile]['pass_entry'].text()
            self.config[profile]['donate'] = self.widgets[profile]['donate_entry'].text()
            self.config[profile]['threads'] = self.widgets[profile]['threads_entry'].text()
            self.config[profile]['cuda'] = self.widgets[profile]['cuda_switch'].isChecked()
            self.config[profile]['opencl'] = self.widgets[profile]['opencl_switch'].isChecked()
            self.config[profile]['cpu'] = self.widgets[profile]['cpu_switch'].isChecked()
            self.config[profile]['args'] = self.widgets[profile]['args_entry'].text()
            self.config[profile]['default_args'] = self.widgets[profile]['default_args_switch'].isChecked()
            self.config[profile]['coin'] = self.widgets[profile]['crypto_chooser'].currentIndex()

        with open(self.settings_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def init_ui(self):
        self.setWindowTitle('XMRiGUI Version 1.4.0')
        self.setWindowIcon(QIcon(self.icon_path))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.tabs = QTabWidget()
        for i, profile in enumerate(self.profiles):
            self.tabs.addTab(self.create_profile_tab(profile), f"Profile {i+1}")
        
        layout.addWidget(self.tabs)
        
        # System Tray
        self.tray_icon = QSystemTrayIcon(QIcon(self.icon_path), self)
        tray_menu = QMenu()
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def create_profile_tab(self, profile):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Header
        header = QHBoxLayout()
        self.widgets[profile]['status_label'] = QLabel("Status: Ready")
        self.widgets[profile]['info_label'] = QLabel("<b>Speed:</b> 0 H/s | <b>Shares:</b> 0/0")
        mine_btn = QPushButton("Start/Stop Mining")
        mine_btn.setCheckable(True)
        mine_btn.setChecked(self.config[profile].get('mine', False))
        mine_btn.clicked.connect(lambda checked, p=profile: self.on_mine_clicked(p, checked))
        
        header.addWidget(self.widgets[profile]['status_label'])
        header.addWidget(self.widgets[profile]['info_label'])
        header.addWidget(mine_btn)
        layout.addLayout(header)
        
        # Settings Grid
        grid = QGridLayout()
        self.widgets[profile]['pool_entry'] = QLineEdit(self.config[profile]['pool'])
        self.widgets[profile]['user_entry'] = QLineEdit(self.config[profile]['user'])
        self.widgets[profile]['pass_entry'] = QLineEdit(self.config[profile]['password'])
        self.widgets[profile]['donate_entry'] = QLineEdit(self.config[profile]['donate'])
        self.widgets[profile]['threads_entry'] = QLineEdit(self.config[profile]['threads'])
        
        grid.addWidget(QLabel("Pool:"), 0, 0)
        grid.addWidget(self.widgets[profile]['pool_entry'], 0, 1)
        grid.addWidget(QLabel("User:"), 1, 0)
        grid.addWidget(self.widgets[profile]['user_entry'], 1, 1)
        grid.addWidget(QLabel("Pass:"), 2, 0)
        grid.addWidget(self.widgets[profile]['pass_entry'], 2, 1)
        
        layout.addLayout(grid)
        
        # Advanced
        adv_group = QGroupBox("Advanced Options")
        adv_layout = QGridLayout(adv_group)
        self.widgets[profile]['cuda_switch'] = QCheckBox("NVidia GPU")
        self.widgets[profile]['cuda_switch'].setChecked(self.config[profile]['cuda'])
        self.widgets[profile]['opencl_switch'] = QCheckBox("AMD GPU")
        self.widgets[profile]['opencl_switch'].setChecked(self.config[profile]['opencl'])
        self.widgets[profile]['cpu_switch'] = QCheckBox("CPU")
        self.widgets[profile]['cpu_switch'].setChecked(self.config[profile]['cpu'])
        
        self.widgets[profile]['crypto_chooser'] = QComboBox()
        self.widgets[profile]['crypto_chooser'].addItems(self.cryptos)
        self.widgets[profile]['crypto_chooser'].setCurrentIndex(self.config[profile]['coin'])
        
        self.widgets[profile]['args_entry'] = QLineEdit(self.config[profile]['args'])
        self.widgets[profile]['default_args_switch'] = QCheckBox("Disable default args")
        self.widgets[profile]['default_args_switch'].setChecked(self.config[profile]['default_args'])

        adv_layout.addWidget(self.widgets[profile]['cuda_switch'], 0, 0)
        adv_layout.addWidget(self.widgets[profile]['opencl_switch'], 0, 1)
        adv_layout.addWidget(self.widgets[profile]['cpu_switch'], 0, 2)
        adv_layout.addWidget(QLabel("Coin:"), 1, 0)
        adv_layout.addWidget(self.widgets[profile]['crypto_chooser'], 1, 1, 1, 2)
        adv_layout.addWidget(QLabel("Extra Args:"), 2, 0)
        adv_layout.addWidget(self.widgets[profile]['args_entry'], 2, 1, 1, 2)
        
        layout.addWidget(adv_group)
        
        # Log
        self.widgets[profile]['log_view'] = QTextEdit()
        self.widgets[profile]['log_view'].setReadOnly(True)
        self.widgets[profile]['log_view'].setStyleSheet("background-color: #1e1e1e; color: #ffffff; font-family: monospace;")
        layout.addWidget(self.widgets[profile]['log_view'])
        
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_config)
        layout.addWidget(save_btn)
        
        return widget

    def on_mine_clicked(self, profile, checked):
        if checked:
            self.start_mining(profile)
        else:
            self.stop_mining(profile)

    def update_log(self, profile):
        process = self.processes.get(profile)
        if not process: return
        
        data = process.readAllStandardOutput().data().decode('utf-8', errors='replace')
        for line in data.splitlines():
            if line:
                lower_line = line.lower()
                color = "#ffffff"
                if "accepted" in lower_line:
                    color = "#2ecc71"
                elif "error" in lower_line or "rejected" in lower_line or "failed" in lower_line:
                    color = "#e74c3c"
                elif "net" in lower_line or "pool" in lower_line:
                    color = "#3498db"
                elif "speed" in lower_line:
                    color = "#f1c40f"

                self.widgets[profile]['log_view'].append(f'<span style="color:{color};">{line}</span>')
                
                # Parsen von Speed/Shares
                speed_match = re.search(r"speed 10s/60s/15m\s+([\d.]+)", line)
                if speed_match:
                    self.widgets[profile]['last_speed'] = speed_match.group(1)
                shares_match = re.search(r"accepted\s+\((\d+)/(\d+)\)", line)
                if shares_match:
                    self.widgets[profile]['last_shares'] = f"{shares_match.group(1)}/{shares_match.group(2)}"

                speed = self.widgets[profile].get('last_speed', '0.0')
                shares = self.widgets[profile].get('last_shares', '0/0')
                self.widgets[profile]['info_label'].setText(f"<b>Speed:</b> {speed} H/s | <b>Shares:</b> {shares}")

                if "connected to" in lower_line:
                    pool_addr = re.search(r"to\s+([^\s]+)", line)
                    self.widgets[profile]['status_label'].setText(f"Status: Connected to {pool_addr.group(1) if pool_addr else 'Pool'}")

    def load_data(self):
        self.profiles = ['profile-0', 'profile-1', 'profile-2']
        for p in self.profiles: self.widgets[p] = {}

        if platform.system() == 'Windows':
            self.settings_path = os.path.join(os.environ.get('APPDATA', '.'), 'xmrigui.json')
            self.xmrig_path = 'xmrig.exe'
            self.icon_path = 'xmrigui.png'
            self.cuda_plugin_path = 'libxmrig-cuda.dll'
            if not os.path.exists(self.xmrig_path):
                self.xmrig_path = os.path.join(os.path.dirname(__file__), 'xmrig.exe')
        else:
            self.settings_path = os.path.expanduser('~/.config/xmrigui.json')
            self.xmrig_path = '/opt/xmrigui/xmrig'
            self.icon_path = '/usr/share/icons/hicolor/256x256/apps/xmrigui.png'
            self.cuda_plugin_path = '/opt/xmrigui/libxmrig-cuda.so'

        self.cryptos = [
            'Monero',
            'Ravencoin',
            'Uplexa',
            'Chukwa',
            'Chukwa v2',
            'CCX',
            'Keva',
            'Dero',
            'Talleo',
            'Safex',
            'ArQmA',
            'NINJA',
            'Raptoreum',
            'Wownero',
            'Scala',
            'Haven Protocol',
            'MoneroV',
            'Epic Cash',
            'Graft',
            'Oxen',
            'Stellite'
        ]
        self.algos = [
            'rx/0',
            'kawpow',
            'cn/upx2',
            'argon2/chukwa',
            'argon2/chukwav2',
            'cn/ccx',
            'rx/keva',
            'astrobwt',
            'cn-pico/tlo',
            'rx/sfx',
            'rx/arq',
            'argon2/ninja',
            'gr',
            'rx/wow',
            'panthera',
            'cn-heavy/xhv',
            'rx/v',
            'rx/epic',
            'rx/graft',
            'rx/loki',
            'rx/xtl'
        ]
        self.raw_config = '''{
    "profile-0": {
        "mine": false,
        "pool": "POOL",
        "user": "49szz88CqMWGgyDxp7VqvBS62pGLQcV4YPSBHcLwtxAXLz1Wngf8vW6is4w13Au7C2RovrTiJQaGDV5VBhFnyMBsM44Pn2P",
        "password": "XMRiGUI",
        "donate": "1",
        "threads": "0",
        "cuda": false,
        "opencl": false,
        "cpu": true,
        "coin": 0,
        "args": "",
        "default_args": false
    },
    "profile-1": {
        "mine": false,
        "pool": "POOL",
        "user": "49szz88CqMWGgyDxp7VqvBS62pGLQcV4YPSBHcLwtxAXLz1Wngf8vW6is4w13Au7C2RovrTiJQaGDV5VBhFnyMBsM44Pn2P",
        "password": "XMRiGUI",
        "donate": "1",
        "threads": "0",
        "cuda": false,
        "opencl": false,
        "cpu": true,
        "coin": 0,
        "args": "",
        "default_args": false
    },
    "profile-2": {
        "mine": false,
        "pool": "de.monero.herominers.com:1111",
        "user": "49szz88CqMWGgyDxp7VqvBS62pGLQcV4YPSBHcLwtxAXLz1Wngf8vW6is4w13Au7C2RovrTiJQaGDV5VBhFnyMBsM44Pn2P",
        "password": "XMRiGUI",
        "donate": "1",
        "threads": "1",
        "cuda": false,
        "opencl": false,
        "cpu": true,
        "coin": 0,
        "args": "",
        "default_args": false
    }
    
}
'''
    
def main():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
