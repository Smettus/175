

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
After=network.target

[Service]
ExecStart=/usr/bin/python /home/smettus/Documenten/175/xmas-175/xmas_detector.py
WorkingDirectory=/home/smettus/Documenten/175/xmas-175
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