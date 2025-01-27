# **Sakuya AC**
<div align=center>
   <img src="https://media1.tenor.com/m/zqopwoNZBvIAAAAd/sakuemon-pixel-art.gif" alt="sakuya walking gif" width=300px>
</div>

### Perfect and Elegant Anti Cheat your YSFlight server
---

## **Features**
- Intercepts and parses network packets to monitor gameplay.
- Detects and logs suspicious activities, like unauthorized modifications.
- Easy configuration via `config.py`.

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
2. Fix on ground re supply which triggers the cheat detection.
3. Negative g-values are wrong interpeted
4. Add more documentation.
5. Add black smoke emission on death
6. Add radar features
7. Add Plugin API
---

## **Contact**
If you have questions, feedback, or suggestions, feel free to reach out to me on Discord: **@theindiandev**

---

## **License**
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

---

## **Contributing**
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

---

## **Acknowledgments**
- Thanks to Vincet A's work on YS Protocol
- Thanks to my friends at 9th Matrix for helping me out
- Pixel art GIF credit: [Tenor](https://tenor.com/view/sakuemon-pixel-art-touhou-sakuya-maid-gif-27137533).

---
:star: Consider giving a star to this repo if you like this project
