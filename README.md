## Description
Flask server ran with docker to enable file upload/serving. Designed to run alongside SPT/FIKA.

## Server Instructions

[Follow this guide to setup SPT/Fika with Docker](https://github.com/OnniSaarni/SPT-Fika-Docker-Guide)

**Create Directories**

Copy the scripts to your server, follow the below folder structure:

```
flaskserv/
│
├── app/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
└── apache/
    ├── html/
```

**Build**

From the project directory:

```
docker build -t flaskserv ./app
```

**Run**

```
docker run -d --name flaskserv --restart unless-stopped -p 5000:5000 -v $(pwd)/apache/html:/var/www/html -e ALLOWED_IPS="yourip1, yourip2" flaskserv
```

**Check Logs**

```
docker logs -f flaskserv
```

## Client Instructions

```
SPT Folder
├── update.py
├── Aki-AutoPatch-Launcher.bat
│
├── BepInEx
│   ├── commit.py
```

**commit.py**

Configure this script with your server IP, when ran it will compress `config` and `plugins` folders to `bepinex.zip` and uploads it via flask.

**Aki-AutoPatch-Launcher.bat**

Use this to start the game, it will check the md5 hash of the `bepinex.zip` in `/BepInEx` against the servers `bepinex.zip.md5`.

If they don't match it will download and extract the bepinex.zip from the server.
