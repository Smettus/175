# Final working setup (but not very robust...):

Open the systemd service:
```bash
sudo nano /etc/systemd/system/xmas175.service
```

Then add the following lines:
```text
[Unit]
Description=xmastree
After=sound.target multi-user.target

[Service]
ExecStart=/usr/bin/python /home/smettus/Documenten/175/xmas-175/xmas_detector.py
WorkingDirectory=/home/smettus/Documenten/175/xmas-175
StandardOutput=append:/home/smettus/Documenten/175/xmas-175/service.log
StandardError=append:/home/smettus/Documenten/175/xmas-175/service.log
Restart=always
User=smettus
Group=smettus
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/smettus/.Xauthority
#Environment=PULSE_SERVER=unix:/run/user/1000/pulse/native

[Install]
WantedBy=multi-user.target
```

Add this in front of the `ExecStart` line if still problems:
```text
ExecStartPre=/usr/bin/pactl unload-module module-suspend-on-idle
ExecStartPre=/usr/bin/pactl load-module module-allow-passthrough
```



 - `Environment=DISPLAY=:0` and `Environment=XAUTHORITY=/home/pi/.Xauthority`: These ensure that the script can access the display if needed, particularly for audio output.


Reload the systemd daemon and enable the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable xmas175.service
sudo systemctl start xmas175.service
```

# Older stuff:
## Not working through rc local:
```
sudo nano /etc/rc.local
```
Add the following line:
su -s /bin/bash smettus -c '/usr/bin/python /home/smettus/Documenten/175/xmas-175/xmas_detector.py &'

```bash
sudo chmod +x /etc/rc.local
```

Then:
```bash
sudo reboot
```

## Non-working (yet)
Setup pulseaudio:

Make pulseaudio work system wide:
```bash
sudo nano /etc/pulse/daemon.conf
```
daemonize = no
Add or modify the line for system-wide access:
system-instance = yes

Then:
```bash
sudo nano /etc/systemd/system/pulseaudio.service
```
```text
[Unit]
Description=PulseAudio sound server
After=sound.target

[Service]
ExecStart=/usr/bin/pulseaudio --system --disallow-exit --daemonize=no
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```
Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable pulseaudio.service
sudo systemctl start pulseaudio.service
```


Run the script upon startup using `systemd`:

Steps:

1.  Create a new systemd service file: First, create a new service file in /etc/systemd/system/:
```bash
sudo nano /etc/systemd/system/xmas175.service
```
2. Add the following content to the service file:
```text
[Unit]
Description=My Python Script
After=network.target pulseaudio.service

[Service]
ExecStart=/usr/bin/python /home/smettus/Documenten/175/xmas-175/xmas_detector.py
WorkingDirectory=/home/smettus/Documenten/175/xmas-175
Environment="DISPLAY=:0"
Environment="PULSE_SERVER=unix:/run/user/1000/pulse/native"
StandardOutput=inherit
StandardError=inherit
Restart=always
User=smettus
Group=smettus

[Install]
WantedBy=multi-user.target
```

3. Enable the service:
```bash
sudo systemctl enable xmas175.service
```
4. Start the service:
```bash
sudo systemctl start xmas175.service
```
5. Check the status of your service:
```bash
sudo systemctl status xmas175.service
```
This will show you whether the script is running successfully.



Try it with `aplay` - only for .wav files though...


## Not needed
Force audio output to 3.5mm jack:
1.    Edit the /etc/rc.local file:
```bash
sudo nano /etc/rc.local
```
2. Add the following line before the exit 0 line:
```text
amixer cset numid=3 1
```
This will force the audio to use the 3.5mm jack. The numid=3 corresponds to the audio output device, and 1 sets it to the analog (3.5mm) output. 0 would set it to HDMI.

3. Save the file: Press Ctrl+X, then Y, and Enter to save and exit.

4. Reboot the Raspberry Pi:
```bash
sudo reboot
```