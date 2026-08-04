(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav# nvidia smi -L
nvidia: command not found
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav# nvidia-smi -L
GPU 0: NVIDIA A10G (UUID: GPU-4aa494b9-9659-a279-8cc5-12c1c9fbf439)
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav# nvidia-smi \
  --query-gpu=index,name,memory.total,memory.used,memory.free \
  --format=csv
index, name, memory.total [MiB], memory.used [MiB], memory.free [MiB]
0, NVIDIA A10G, 23028 MiB, 22403 MiB, 215 MiB
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav# nvidia-smi pmon -c 1
# gpu         pid   type     sm    mem    enc    dec    jpg    ofa    command
# Idx           #    C/G      %      %      %      %      %      %    name
    0    2354247     C      -      -      -      -      -      -    tritonserver
    0    3588267     C      -      -      -      -      -      -    python3.11
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav#

