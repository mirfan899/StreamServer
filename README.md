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
Use docker compose to build both docker images.
```shell
docker compose build
docker compose up -d
```


### Docker commands 
```shell
# build
docker build . -t whisper --file DockerfileWhisper

# run
docker run -d -p 5000:5000 whisper

# stop
docker ps stop <id>

# remove stopped containers
docker rm $(docker ps --filter status=exited -q)
```
