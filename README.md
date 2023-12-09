### Whisper and Vosk for streaming
```shell
pip install -r requirements.txt
```

### Download models.
```shell
bash download.sh
```


run whisper server
```shell
python whisper_server.py
```

run vosk server
```shell
python vosk_server.py
```

### Docker compose
```shell
docker compose build
docker compose up -d
```


 docker build - < DockerfileWhisper
