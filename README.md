# ServeLite

**Instant local file sharing — zero dependencies, one command.**

Share files between any devices on the same Wi-Fi network. No cloud. No signup. No frameworks.


## Tech Stack

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTTP](https://img.shields.io/badge/HTTP-Server-FF6C37?style=for-the-badge&logo=python&logoColor=white)
![Zero Dependencies](https://img.shields.io/badge/Zero-Dependencies-4CAF50?style=for-the-badge&logo=zero&logoColor=white)
![Open Source](https://img.shields.io/badge/Open-Source-3DA639?style=for-the-badge&logo=open-source-initiative&logoColor=white)

## Quick Start

```bash
chmod +x start.sh
./start.sh
```

That's it. Your browser opens automatically.  
Other devices on the same network visit the printed URL (e.g. `http://192.168.1.42:8000`).


## File Structure

```
ServeLite/
├── index.html   ← Web UI (drag-drop upload, file list, download)
├── server.py    ← Custom Python HTTP server (GET + POST /upload)
├── start.sh     ← One-click launcher (detects IP, opens browser)
└── uploads/     ← All uploaded files land here (auto-created)
```


## Features

| Feature | Detail |
|---|---|
| Upload | Drag & drop or click-to-browse, XHR with progress bar |
| Download | Click any file in the list |
| File listing | Live JSON API at `GET /files` |
| Cross-device | Served on `0.0.0.0` — any LAN device can connect |
| Zero deps | Pure Python 3 stdlib + plain HTML/CSS/JS |


## Manual Start (no script)

```bash
python3 server.py
# then open http://localhost:8000
```


## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Serves `index.html` |
| `GET` | `/files` | Returns JSON array of uploaded files |
| `GET` | `/uploads/<name>` | Downloads a specific file |
| `POST` | `/upload` | Uploads a file (multipart/form-data, field: `file`) |


## Requirements

- Python 3.6+ (standard library only)
- A modern browser
- Devices on the same Wi-Fi / LAN


## 👨‍💻 Developer

**ANTHONY KARANJA**

[![Portfolio](https://img.shields.io/badge/Portfolio-anthonyke.netlify.app-FF5722?style=for-the-badge&logo=netlify&logoColor=white)](https://anthonyke.netlify.app)
[![Email](https://img.shields.io/badge/Email-anthonykaranja018%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:anthonykaranja018@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-ALPHACODEKE-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/alphacodeke)


## License

MIT © ANTHONY KARANJA
