#!/usr/bin/env python3

import gi, os, json, sys, subprocess, re, threading
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk

# Windows taskbar icon fix
if sys.platform == "win32":
    import ctypes
    try:
        myappid = 'freetimemaker.xmrigui.1.1.0' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass

APP_VERSION = "v1.8.1"

class Window(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.widgets = {}
        self.processes = {}
        self.load_data()

        self._initialize_profile_widgets()
        self.config = self.get_config()

        # UI Setup
        self.set_resizable(False)
        self.apply_theme()
        self.draw()
        self.connect('destroy', Gtk.main_quit)

        # Start mining if configured
        for profile in self.profiles:
            if self.config[profile].get('mine', False):
                self.start_mining(profile, save=False)

        self.show_all()

    def load_data(self):
        # Handle PyInstaller path
        if getattr(sys, 'frozen', False):
            script_dir = sys._MEIPASS
        else:
            script_dir = os.path.dirname(os.path.realpath(__file__))

        # Linux / Windows differentiation for paths
        if sys.platform == "win32":
            self.settings_path = os.path.join(os.getenv('APPDATA'), 'XMRiGUI', 'xmrigui.json')
            os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
            # Look in app dir, then in "windows" subfolder (for development)
            self.xmrig_path = os.path.join(script_dir, 'xmrig.exe')
            if not os.path.exists(self.xmrig_path):
                self.xmrig_path = os.path.join(script_dir, 'windows', 'xmrig.exe')

            self.cpuminer_path = os.path.join(script_dir, 'minerd.exe')
            if not os.path.exists(self.cpuminer_path):
                self.cpuminer_path = os.path.join(script_dir, 'windows', 'minerd.exe')

            self.lolminer_path = os.path.join(script_dir, 'lolMiner.exe')
            if not os.path.exists(self.lolminer_path):
                self.lolminer_path = os.path.join(script_dir, 'windows', 'lolMiner.exe')

            self.cuda_plugin_path = os.path.join(script_dir, 'libxmrig-cuda.dll')
        else:
            if not os.path.exists(os.path.join(script_dir, 'xmrig')) and os.path.exists('/opt/xmrigui'):
                script_dir = '/opt/xmrigui'
            self.settings_path = os.path.expanduser('~/.config/xmrigui.json')
            self.xmrig_path = os.path.join(script_dir, 'xmrig')
            self.cpuminer_path = os.path.join(script_dir, 'minerd')
            self.lolminer_path = os.path.join(script_dir, 'lolMiner')
            self.cuda_plugin_path = os.path.join(script_dir, 'libxmrig-cuda.so')

        self.user = os.environ.get('USER') or os.environ.get('USERNAME') or 'user'
        self.icon_path = os.path.join(script_dir, 'xmrigui.png')
        # If not found, check standard Linux icon path
        if not os.path.exists(self.icon_path) and sys.platform != "win32":
            alt_icon = "/usr/share/icons/hicolor/256x256/apps/xmrigui.png"
            if os.path.exists(alt_icon):
                self.icon_path = alt_icon

        # Final fallback check to prevent crash
        if not os.path.exists(self.icon_path):
            self.icon_path = os.path.join(os.getcwd(), 'xmrigui.png')

        self.profiles = ['profile-0', 'profile-1', 'profile-2']
        self.cryptos = [
            'Monero', 'Ravencoin', 'Uplexa',
            'Chukwa', 'Chukwa v2', 'CCX', 'Keva', 'Dero', 'Talleo', 'Safex', 'ArQmA',
            'NINJA', 'Raptoreum', 'Wownero', 'Scala', 'Haven Protocol', 'MoneroV',
            'Epic Cash', 'Graft', 'Oxen', 'Stellite'
        ]
        self.algos = [
            'rx/0', 'kawpow', 'cn/upx2',
            'argon2/chukwa', 'argon2/chukwav2', 'cn/ccx', 'rx/keva', 'astrobwt',
            'cn-pico/tlo', 'rx/sfx', 'rx/arq', 'argon2/ninja', 'gr', 'rx/wow',
            'panthera', 'cn-heavy/xhv', 'rx/v', 'rx/epic', 'rx/graft', 'rx/loki', 'rx/xtl'
        ]
        self.raw_config = '''{
    "profile-0": {
        "mine": false,
        "pool": "pool.supportxmr.com:3333",
        "user": "49szz88CqMWGgyDxp7VqvBS62pGLQcV4YPSBHcLwtxAXLz1Wngf8vW6is4w13Au7C2RovrTiJQaGDV5VBhFnyMBsM44Pn2P",
        "password": "Donate",
        "donate": "0",
        "threads": "8",
        "cuda": false,
        "opencl": false,
        "cpu": true,
        "coin": 0,
        "args": "",
        "default_args": false
    },
    "profile-1": {
        "mine": false,
        "pool": "xmr-eu.kryptex.network:7029",
        "user": "49szz88CqMWGgyDxp7VqvBS62pGLQcV4YPSBHcLwtxAXLz1Wngf8vW6is4w13Au7C2RovrTiJQaGDV5VBhFnyMBsM44Pn2P",
        "password": "Donate",
        "donate": "0",
        "threads": "8",
        "cuda": false,
        "opencl": false,
        "cpu": true,
        "coin": 0,
        "args": "",
        "default_args": false
    },
    "profile-2": {
        "mine": false,
        "pool": "etc-eu1.nanopool.org:19444",
        "user": "49szz88CqMWGgyDxp7VqvBS62pGLQcV4YPSBHcLwtxAXLz1Wngf8vW6is4w13Au7C2RovrTiJQaGDV5VBhFnyMBsM44Pn2P",
        "password": "Donate",
        "donate": "0",
        "threads": "8",
        "cuda": false,
        "opencl": false,
        "cpu": true,
        "coin": 0,
        "args": "",
        "default_args": false
    }
}
'''

    def get_config(self):
        default_config = json.loads(self.raw_config)
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r') as f:
                    config = json.load(f)
                    # Ensure all profiles and keys exist by merging with default
                    for p in self.profiles:
                        if p not in config:
                            config[p] = default_config[p]
                        else:
                            for key, value in default_config[p].items():
                                if key not in config[p]:
                                    config[p][key] = value
                    return config
        except Exception as e:
            print(f"Config error, using defaults: {e}")

        # Fallback to default if file doesn't exist or is broken
        os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
        with open(self.settings_path, 'w') as f:
            f.write(self.raw_config)
        return default_config

    def apply_theme(self):
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", True)
        css_provider = Gtk.CssProvider()
        css = b"""
            window { background-color: #1e1e1e; color: #ffffff; }
            entry, combobox { background-color: #2d2d2d; color: white; border: 1px solid #3d3d3d; padding: 5px; border-radius: 4px; }
            frame { border: 1px solid #3d3d3d; border-radius: 8px; padding: 15px; background-color: #252525; margin: 10px; }
            textview { font-family: 'Consolas', monospace; background-color: #000000; color: #00ff00; }
            button { background-color: #3d3d3d; color: white; border-radius: 4px; padding: 8px; border: none; }
            button:hover { background-color: #4d4d4d; }
            label { color: #eeeeee; }

            /* Modern Switch Styling */
            switch {
                border-radius: 20px;
                outline-width: 0;
            }
            switch trough {
                border-radius: 20px;
                background-color: #3d3d3d;
                border: 1px solid #4d4d4d;
                min-width: 50px;
                min-height: 24px;
            }
            switch trough:checked {
                background-color: #2ecc71;
                border: 1px solid #27ae60;
            }
            switch slider {
                background-color: #ffffff;
                border-radius: 20px;
                min-width: 20px;
                min-height: 20px;
                margin: 2px;
            }
        """
        css_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def draw(self):
        self.set_title(f'XMRiGUI {APP_VERSION}')

        # Taskbar Fixes
        if sys.platform != "win32":
            # Linux: WM_CLASS must match the .desktop file name
            self.set_wmclass("xmrigui", "XMRiGUI")
            self.set_role("xmrigui")

        if os.path.exists(self.icon_path):
            try:
                Gtk.Window.set_default_icon_from_file(self.icon_path)
                self.set_icon_from_file(self.icon_path)
            except Exception as e:
                print(f"Error loading icon: {e}")

        self.set_border_width(20)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)

        for profile in self.profiles:
            self.widgets[profile]['box'] = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=30)
            self.widgets[profile]['main_box'] = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)

            if os.path.exists(self.icon_path):
                pix = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.icon_path, 128, 128, True)
                self.widgets[profile]['image'] = Gtk.Image.new_from_pixbuf(pix)
            else:
                self.widgets[profile]['image'] = Gtk.Image.new_from_icon_name("utilities-system-monitor", Gtk.IconSize.DIALOG)

            self.widgets[profile]['name'] = Gtk.Label()
            self.widgets[profile]['name'].set_markup('<big>XMRiGUI</big>\nmade by Freetime Maker\n<a href="https://github.com/FreetimeMaker/XMRiGUI">Source code</a>')

            self.widgets[profile]['mine_box'] = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            self.widgets[profile]['mine_label'] = Gtk.Label()
            self.widgets[profile]['mine_label'].set_markup('<big>Mine</big>')

            self.widgets[profile]['mine_switch'] = Gtk.Switch()
            self.widgets[profile]['mine_switch'].set_active(self.config[profile].get('mine', False))
            self.widgets[profile]['mine_switch'].connect('state-set', self.on_mine_switch, profile)
            self.widgets[profile]['mine_switch'].props.valign = Gtk.Align.CENTER

            self.widgets[profile]['mine_box'].pack_start(self.widgets[profile]['mine_label'], False, False, 10)
            self.widgets[profile]['mine_box'].pack_start(self.widgets[profile]['mine_switch'], False, False, 10)
            self.widgets[profile]['mine_box'].pack_start(self.widgets[profile]['status_label'], False, False, 10)
            self.widgets[profile]['mine_box'].pack_start(self.widgets[profile]['info_label'], False, False, 10)

            self.widgets[profile]['main_box'].pack_start(self.widgets[profile]['image'], False, False, 10)
            self.widgets[profile]['main_box'].pack_start(self.widgets[profile]['name'], False, False, 10)
            self.widgets[profile]['main_box'].pack_start(self.widgets[profile]['mine_box'], False, False, 10)

            # Log View
            self.widgets[profile]['log_expander'] = Gtk.Expander(label='Miner Output (Live)')
            self.widgets[profile]['log_expander'].set_expanded(True)
            self.widgets[profile]['log_view'] = Gtk.TextView(buffer=self.widgets[profile]['log_buffer'])
            self.widgets[profile]['log_view'].set_editable(False)
            self.widgets[profile]['log_view'].set_wrap_mode(Gtk.WrapMode.WORD)
            self.widgets[profile]['log_scroll'] = Gtk.ScrolledWindow()
            self.widgets[profile]['log_scroll'].set_min_content_height(150)
            self.widgets[profile]['log_scroll'].add(self.widgets[profile]['log_view'])
            self.widgets[profile]['log_expander'].add(self.widgets[profile]['log_scroll'])

            # Settings Grid
            self.widgets[profile]['settings'] = Gtk.Grid(column_homogeneous=True, column_spacing=10, row_spacing=10)
            w = self.widgets[profile]
            c = self.config[profile]
            w['pool_entry'] = Gtk.Entry(text=c['pool'])
            w['user_entry'] = Gtk.Entry(text=c['user'])
            w['pass_entry'] = Gtk.Entry(text=c.get('password', ''))
            w['donate_entry'] = Gtk.Entry(text=c.get('donate', '1'))
            w['threads_entry'] = Gtk.Entry(text=c.get('threads', '0'))

            w['settings'].attach(Gtk.Label(label='Pool:'), 0, 0, 1, 1); w['settings'].attach(w['pool_entry'], 1, 0, 1, 1)
            w['settings'].attach(Gtk.Label(label='User:'), 0, 1, 1, 1); w['settings'].attach(w['user_entry'], 1, 1, 1, 1)
            w['settings'].attach(Gtk.Label(label='Password:'), 0, 2, 1, 1); w['settings'].attach(w['pass_entry'], 1, 2, 1, 1)
            w['settings'].attach(Gtk.Label(label='Donate:'), 2, 0, 1, 1); w['settings'].attach(w['donate_entry'], 3, 0, 1, 1)
            w['settings'].attach(Gtk.Label(label='Threads:'), 2, 1, 1, 1); w['settings'].attach(w['threads_entry'], 3, 1, 1, 1)

            save_btn = Gtk.Button(label='Save')
            save_btn.connect('clicked', lambda b: self.save())
            w['settings'].attach(save_btn, 3, 2, 1, 1)

            # Advanced
            w['advanced_settings'] = Gtk.Expander(label='Advanced options')
            adv_grid = Gtk.Grid(column_homogeneous=True, row_spacing=10, column_spacing=10)
            w['cuda_switch'] = Gtk.CheckButton(label='NVIDIA GPU (CUDA)'); w['cuda_switch'].set_active(c.get('cuda', False))
            w['opencl_switch'] = Gtk.CheckButton(label='AMD GPU (OpenCL)'); w['opencl_switch'].set_active(c.get('opencl', False))
            w['cpu_switch'] = Gtk.CheckButton(label='CPU'); w['cpu_switch'].set_active(c.get('cpu', True))
            w['crypto_chooser'] = Gtk.ComboBoxText()
            for crypto in self.cryptos: w['crypto_chooser'].append_text(crypto)
            w['crypto_chooser'].set_active(c.get('coin', 3))
            w['default_args_switch'] = Gtk.CheckButton(label='Disable default args'); w['default_args_switch'].set_active(c.get('default_args', False))
            w['args_entry'] = Gtk.Entry(text=c.get('args', ''))

            adv_grid.attach(w['cpu_switch'], 0, 0, 1, 1)
            adv_grid.attach(w['cuda_switch'], 0, 1, 1, 1)
            adv_grid.attach(w['opencl_switch'], 0, 2, 1, 1)
            adv_grid.attach(w['crypto_chooser'], 1, 0, 1, 1)
            adv_grid.attach(w['default_args_switch'], 1, 1, 1, 1)
            adv_grid.attach(Gtk.Label(label='Extra args:'), 1, 2, 1, 1)
            adv_grid.attach(w['args_entry'], 1, 3, 1, 1)
            w['advanced_settings'].add(adv_grid)

            w['box'].pack_start(w['main_box'], False, False, 10)
            w['box'].pack_start(w['settings'], False, False, 10)
            w['box'].pack_start(w['advanced_settings'], False, False, 10)
            w['box'].pack_start(w['log_expander'], True, True, 10)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        for profile in self.profiles:
            self.stack.add_titled(self.widgets[profile]['box'], profile, f"Profile {int(profile[-1])+1}")

        self.stack_switcher = Gtk.StackSwitcher()
        self.stack_switcher.set_stack(self.stack)
        self.stack_switcher.set_halign(Gtk.Align.CENTER)

        self.box.pack_start(self.stack_switcher, False, False, 10)
        self.box.pack_start(self.stack, True, True, 10)
        self.add(self.box)

    def on_mine_switch(self, widget, state, profile):
        if state: self.start_mining(profile)
        else: self.stop_mining(profile)

    def start_mining(self, profile, save=True):
        if save:
            self.config[profile]['mine'] = True
            self.save()

        cmd = self.get_miner_command(profile)
        binary = cmd.split(' ')[0].replace('"', '')
        if not os.path.exists(binary):
            self.log(profile, f"Error: Miner not found at {binary}", "error")
            self.widgets[profile]['mine_switch'].set_active(False)
            return

        self.widgets[profile]['status_label'].set_text('Status: Mining...')
        creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        try:
            self.processes[profile] = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=creationflags
            )
            GLib.io_add_watch(self.processes[profile].stdout, GLib.IO_IN | GLib.IO_HUP, self.update_log, profile)
        except Exception as e:
            self.log(profile, f"Error: {str(e)}", "error")

    def stop_mining(self, profile, save=True):
        if profile in self.processes:
            self.processes[profile].terminate()
            del self.processes[profile]
        self.widgets[profile]['status_label'].set_text('Status: Stopped.')
        if save:
            self.config[profile]['mine'] = False
            self.save()

    def save(self):
        for profile in self.profiles:
            w = self.widgets[profile]
            self.config[profile].update({
                'pool': w['pool_entry'].get_text(), 'user': w['user_entry'].get_text(), 'password': w['pass_entry'].get_text(),
                'donate': w['donate_entry'].get_text(), 'threads': w['threads_entry'].get_text(),
                'cuda': w['cuda_switch'].get_active(), 'opencl': w['opencl_switch'].get_active(), 'cpu': w['cpu_switch'].get_active(),
                'args': w['args_entry'].get_text(), 'default_args': w['default_args_switch'].get_active(), 'coin': w['crypto_chooser'].get_active()
            })
        with open(self.settings_path, 'w') as f: json.dump(self.config, f, indent=4)

    def get_miner_command(self, profile):
        c = self.config[profile]
        coin = self.cryptos[c['coin']]
        pool = c['pool']; user = c['user']; password = c.get('password', '')
        binary = self.xmrig_path
        args = '--no-color'
        if not c.get('default_args', False):
            args += f' --algo={self.algos[c["coin"]]} --url={pool} --user={user} --pass={password if password else "x"}'
            args += f' --donate-level={c.get("donate", "1")}'
            if c.get('threads', '0') != '0': args += f' --threads={c["threads"]} --randomx-init={c["threads"]}'
            if c.get('cuda', False): args += f' --cuda --cuda-loader="{self.cuda_plugin_path}"'
            if c.get('opencl', False): args += ' --opencl'
            if not c.get('cpu', True): args += ' --no-cpu'

        if c.get('args'): args += f' {c["args"]}'

        # On Windows, wrap the binary in quotes if it contains spaces
        if sys.platform == "win32":
            return f'"{binary}" {args}'
        return f'{binary} {args}'

    def update_log(self, source, condition, profile):
        if condition & GLib.IO_HUP: return False
        line = source.readline().decode('utf-8', errors='replace')
        if line:
            self.log(profile, line.strip())
            spd = re.search(r"speed 10s/60s/15m\s+([\d.]+)", line.lower())
            shr = re.search(r"accepted\s+\((\d+)/(\d+)\)", line.lower())
            if spd: self.widgets[profile]['s'] = spd.group(1)
            if shr: self.widgets[profile]['h'] = f"{shr.group(1)}/{shr.group(2)}"
            s = self.widgets[profile].get('s', '0.0'); h = self.widgets[profile].get('h', '0/0')
            self.widgets[profile]['info_label'].set_markup(f"<b>Speed:</b> {s} H/s | <b>Shares:</b> {h}")
            return True
        return False

    def log(self, profile, msg, tag=None):
        buf = self.widgets[profile]['log_buffer']
        buf.insert(buf.get_end_iter(), msg + "\n")
        adj = self.widgets[profile]['log_scroll'].get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())

    def _initialize_profile_widgets(self):
        for profile in self.profiles:
            self.widgets[profile] = {
                'status_label': Gtk.Label(label='Status: Stopped.'), 'info_label': Gtk.Label(), 'log_buffer': Gtk.TextBuffer()
            }
            self.widgets[profile]['info_label'].set_markup('<b>Speed:</b> 0 H/s | <b>Shares:</b> 0/0')

if __name__ == "__main__":
    win = Window()
    Gtk.main()
