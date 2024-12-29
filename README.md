<br />
<div align="center">
  <a href="https://github.com/ThorTuwy/WallaReq">
    <img src="frontend/src/assets/Wallareq-ico.webp" alt="Logo" width="126" height="116">
  </a>

<h3 align="center">WallaReq</h3>

  <p align="center">
    Get all new products uploaded to Wallapop easier than ever.
  </p>
</div>

## About The Project
A simple app that use the API of wallapop to get all the new products in the platform, with a frontend to make using it as easy as possible.

The backend is made with FastAPI and the frontend with SolidJS

## Getting Started

The recomended way to use this project is Docker

### Docker

You can run the docker with this command:

```sh
docker run -p 8000:8000 ghcr.io/thortuwy/wallareq:latest
```

### Python+Node

#### Prerequisites

You need python3 and node installed on your system.

#### Clone the repository
```sh
git clone https://github.com/ThorTuwy/WallaReq
cd WallaReq
```
#### Run the start script
>[!WARNING]
>The script use pnpm to install and work with frontend dependencies, change it if you need it.
```sh
./start.sh
```

# Developers

## Run the project

For development I recomend to use the devstart.sh script:
>[!WARNING]
>The script use pnpm to install and work with frontend dependencies, change it if you need it.
```sh
./devstart.sh
```

## Build docker

I recommend before trying a pull request to build the docker to check if all is working properly:
```sh
./makeDocker.sh
```

## Roadmap

- [ ] Refactor code
- [ ] Improve easiness of adding new Notifications Methods (Mainly in the frontend side)
- [ ] Add new notifications methods
    - [ ] Discord (Webhook and Bot)
    - [ ] Telegram
    - [ ] ...

