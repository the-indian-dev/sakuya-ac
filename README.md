# **Sakuya AC**
<div align=center>
   <img src="https://media1.tenor.com/m/zqopwoNZBvIAAAAd/sakuemon-pixel-art.gif" alt="sakuya walking gif" width=300px>
</div>

### Perfect and Elegant Anti Cheat for your YSFlight server
---
Well it started as an anti cheat... and now aims to add more features to make YSFlight more realstic server side
for vanilla clients.

## Test Server

I have a server running at ``9m.theindiandev.in`` and port ``7915``
with [2ch map](https://w.atwiki.jp/ysflight/pages/26.html) and latest version of
Sakuya AC and G Limiter at 20. It also has all the experimental options turned on.

---

## Contributors

- Skipper
- Biry (Emotional Support)

---

## **Features**
- Intercepts and parses network packets to monitor gameplay.
- Adds features like G Limiter and Smoke Emission on Death.
- All features are server side, vanilla client can join
- Supports clients post 20150425 version to join the server (Experimental)
- Easy configuration via `config.py`.
- Plugin Support

---

## **Getting Started**

### **Prerequisites**
- Python 3.9+

### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/the-indian-dev/sakuya-ac.git
   cd sakuya-ac
   ```

2. Edit `config.py` to match your server and client setup.
> **Warning**
> Please ensure that you have put the correct YSFlight version in YSF_VERSION variable in `config.py`. This is important for the proxy to work correctly.

3. Run the proxy server:
   ```bash
   python proxy.py
   ```
---

## **Configuration**
All configuration is done via the `config.py` file. Example:

```python
# config.py
SERVER_HOST = "127.0.0.1"  # YSFlight server IP
SERVER_PORT = 7915         # YSFlight server port
PROXY_PORT = 9000          # Port where the proxy listens
```

---

## **Usage**
1. Point your YSFlight client to the proxy server (e.g., `127.0.0.1:9000`).
2. Monitor logs to view real-time parsing and activity tracking.

---
## **TODO :memo:**
1. Add more detection rules.
2. Radar.
3. More documentation.
---

## **Contact**
- If you have questions, feedback, or suggestions, feel free to reach out to me on Discord: **@theindiandev**
- You can email me at **theindiandev@theindiandev.in**
- Join our discord server [here](https://discord.gg/CgEdmBQQMr)
---

## **License**
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

---

## **Reporting Issues**
1. Use Github issues tab to open an issue.
2. Please provide detailed information about the issue you are facing.
3. Give us all the log from console, it would be better if logging level was set to ``DEBUG``
4. Please also give us the replay .yfs file while reporting issue
5. If you have a feature request, please open an issue with the label `enhancement`.
---

## **Acknowledgments**
- Thanks to Vincet A's work on YS Protocol
- Thanks to my friends at 9th Matrix for helping me out
- Pixel art GIF credit: [Tenor](https://tenor.com/view/sakuemon-pixel-art-touhou-sakuya-maid-gif-27137533).

---
:star: Consider giving a star to this repo if you like this project
