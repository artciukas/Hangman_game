# Hangman_game


Docker run:
1) To create docker image run: docker build -f Dockerfile -t "image name" .
2) Container run: docker run "container ID"
3) Get ip from container: docker inspect "container name"
4) run browser enter inspected container ip and 8000 port.

Local run:
1) create virtual environment: python3 -m venv "venv name"
2) install all libraries: pip install -r requirements.txt
3) enter to src directory: cd src
4) run file: run.py

## Clone code:
```
git@github.com:artciukas/Hangman_game.git
```

## Docker run:
1) To create docker image run: 
```
docker build -f Dockerfile -t <image name> .
```
2) Container run: 
```
docker run <container ID>
```
3) Get ip from container: 
```
docker inspect <container name>
```
4) Run: start browser enter inspected container ip and 8000 port.


## Local run:
1) Create virtual environment: 
```
python3 -m venv <venv name>
```
2) Install all libraries: 
```
pip install -r requirements.txt
```
3) Enter to src directory: 
```
cd src
```
4) Run file: 
```
python3 run.py
```

## Run unittest tests:
1) Run command:
```
python -m unittest
```

