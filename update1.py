(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/Fish_audio_s1mini# DOCKER_BUILDKIT=1 docker build --secret id=hf_token,src=hf_token.txt --progress=plain -t fish-s1-mini-realtime:latest .
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 4.56kB done
#1 DONE 0.0s

#2 [auth] docker/dockerfile:pull token for registry-1.docker.io
#2 DONE 0.0s

#3 resolve image config for docker-image://docker.io/docker/dockerfile:1.7
#3 DONE 0.3s

#4 docker-image://docker.io/docker/dockerfile:1.7@sha256:a57df69d0ea827fb7266491f2813635de6f17269be881f696fbfdf2d83dda33e
#4 CACHED

#5 [internal] load metadata for docker.io/nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04
#5 ...

#6 [auth] nvidia/cuda:pull token for registry-1.docker.io
#6 DONE 0.0s

#5 [internal] load metadata for docker.io/nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04
#5 DONE 0.5s

#7 [internal] load .dockerignore
#7 transferring context: 142B done
#7 DONE 0.0s

#8 [internal] load build context
#8 transferring context: 13.27kB done
#8 DONE 0.0s

#9 [stage-0 10/17] RUN python -m pip install     --no-cache-dir     --constraint /app/s1-constraints.txt     -r requirements.txt
#9 CACHED

#10 [stage-0  9/17] RUN printf '%s\n'     'torch==2.4.1+cu124'     'torchvision==0.19.1+cu124'     'torchaudio==2.4.1+cu124'     'numpy==1.26.4'     > /app/s1-constraints.txt
#10 CACHED

#11 [stage-0  2/17] RUN apt-get update &&     apt-get install -y --no-install-recommends         git         git-lfs         curl         ca-certificates         build-essential         cmake         ffmpeg         libsndfile1         libsndfile1-dev         portaudio19-dev         libasound2-dev         libsm6         libxext6         libjpeg-dev         zlib1g-dev         protobuf-compiler         python3.10         python3.10-dev         python3.10-venv         python3-pip &&     rm -rf /var/lib/apt/lists/*
#11 CACHED

#12 [stage-0  5/17] WORKDIR /app/fish-speech
#12 CACHED

#13 [stage-0  6/17] RUN python3.10 -m venv /app/.venv
#13 CACHED

#14 [stage-0  7/17] RUN python -m pip install --upgrade pip setuptools wheel
#14 CACHED

#15 [stage-0  4/17] RUN git clone         https://huggingface.co/spaces/fishaudio/s1-mini         /app/fish-speech &&     cd /app/fish-speech &&     git checkout "492fb712a1cf1a662f5be0c971272b696501115f" &&     rm -rf .git
#15 CACHED

#16 [stage-0  3/17] WORKDIR /app
#16 CACHED

#17 [stage-0  8/17] RUN python -m pip install     --no-cache-dir     torch==2.4.1     torchvision==0.19.1     torchaudio==2.4.1     --index-url https://download.pytorch.org/whl/cu124
#17 CACHED

#18 [stage-0 11/17] COPY requirements-server.txt /app/requirements-server.txt
#18 ERROR: failed to calculate checksum of ref df342f6d-5d3e-4045-80a0-9a044ee86345::hq42msbmkekpua6cqpdxgeev4: "/requirements-server.txt": not found

#19 [stage-0  1/17] FROM docker.io/nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04@sha256:2fcc4280646484290cc50dce5e65f388dd04352b07cbe89a635703bd1f9aedb6
#19 resolve docker.io/nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04@sha256:2fcc4280646484290cc50dce5e65f388dd04352b07cbe89a635703bd1f9aedb6 0.0s done
#19 sha256:0bb88834d973ca1b450fcc2a05333c6fe45510bee289912a5391274c351c4a4d 2.42kB / 2.42kB done
#19 sha256:2fcc4280646484290cc50dce5e65f388dd04352b07cbe89a635703bd1f9aedb6 743B / 743B done
#19 sha256:a029a877f7e33ada4e4eaadf085ff5ad517994f2f0e416845ff109ece2331f4b 14.29kB / 14.29kB done
#19 DONE 0.3s
------
 > [stage-0 11/17] COPY requirements-server.txt /app/requirements-server.txt:
------
ERROR: failed to build: failed to solve: failed to compute cache key: failed to calculate checksum of ref df342f6d-5d3e-4045-80a0-9a044ee86345::hq42msbmkekpua6cqpdxgeev4: "/requirements-server.txt": not found
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/Fish_audio_s1mini#
