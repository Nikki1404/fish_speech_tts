nvidia-smi \
  --query-gpu=index,name,memory.total,memory.used,memory.free \
  --format=csv

nvidia-smi pmon -c 1

