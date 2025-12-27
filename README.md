# poe_turbo

A little Service to enable Turboclicking on the mouse back button and pressing "1" on the mouse forward button, when a PoE Windows is active.
Tested on CachyOS.

## Can be done with a small services

This file should be in `~/.config/systemd/user/poe_macro.service
```
[Unit]  
Description=PoE Mouse Macro  
After=graphical.target  
  
[Service]  
Type=simple  
ExecStart=/home/path/to/poe_macro/venv/bin/python /home/path/to/poe_macro/poe_macro.py  
WorkingDirectory=/home/path/to/poe_macro  
Restart=on-failure  
Environment=DISPLAY=:0  
# Optional: if using Wayland, adjust accordingly  
# Environment=XDG_SESSION_TYPE=wayland  
  
[Install]  
WantedBy=default.target
```
### Enable the service

```bash
systemctl --user daemon-reload
systemctl --user enable poe_macro.service
systemctl --user start poe_macro.service
```

### Status and Logs

```bash
systemctl --user status poe_macro.service  
journalctl --user -u poe_macro.service -f
```
