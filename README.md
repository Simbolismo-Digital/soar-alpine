# Soar Docker Build

Versão da Soar: `9.6.4`

Este Dockerfile cria uma **build do Soar** (versão de desenvolvimento) no Alpine Linux, incluindo:

- Kernel Soar
- CLI
- Python SML bindings
- TCL SML bindings
- Java SML bindings
- Headers e bibliotecas
- Python Server TCP

O build final é armazenado em `/opt/soar`, contendo apenas o que estava em `out/` do repositório original.

---

## Run Docker
https://hub.docker.com/r/daviaws/soar-alpine/
```bash
# enter Soar cli
docker run --name soar-alpine-cli -it --entrypoint /opt/soar/soar daviaws/soar-alpine:9.6.4
# run python server
docker run --name soar-alpine-server -it -p 12122:12122 daviaws/soar-alpine:9.6.4
```

## After Running Python Server
```bash
# Use simple commands via nc terminated by ';;'
echo "version;;" | nc localhost 12122
```
<img width="816" height="62" alt="image" src="https://github.com/user-attachments/assets/dcec206b-e39b-422f-8291-dc043e4bfa7a" />


```bash
# Use script commands terminated by ';;' character
nc localhost 12122 < test.soar
```
<img width="757" height="279" alt="image" src="https://github.com/user-attachments/assets/4da4abe2-b6dc-4d69-befe-27c9079c165e" />


## Local Client SML
```bash
# I discovered this creates Soar in the python thread without need of external connections
# but by default Soar opens port 12121
python3 debian_python_soar/sml_client.py
```

## Build local (you don't need, only for dev)
```bash
# build
docker build -t soar-alpine:9.6.4 .
```
