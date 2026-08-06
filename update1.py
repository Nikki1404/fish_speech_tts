#17 [stage-0  9/16] RUN printf '%s\n'     'torch==2.4.1'     'torchvision==0.19.1'     'torchaudio==2.4.1'     > /app/pytorch-constraints.txt
#17 DONE 0.3s

#18 [stage-0 10/16] RUN python -m pip install     --no-cache-dir     --constraint /app/pytorch-constraints.txt     -e ".[stable]"
#18 2.485 Obtaining file:///app/fish-speech
#18 2.489   Installing build dependencies: started
#18 6.023   Installing build dependencies: finished with status 'done'
#18 6.024   Checking if build backend supports build_editable: started
#18 6.339   Checking if build backend supports build_editable: finished with status 'done'
#18 6.341   Getting requirements to build editable: started
#18 7.113   Getting requirements to build editable: finished with status 'done'
#18 7.114   Preparing editable metadata (pyproject.toml): started
#18 7.407   Preparing editable metadata (pyproject.toml): finished with status 'done'
#18 7.418 Requirement already satisfied: numpy in /app/.venv/lib/python3.10/site-packages (from fish-speech==2.0.0) (2.2.6)
#18 7.743 INFO: pip is looking at multiple versions of fish-speech to determine which version is compatible with other requirements. This could take a while.
#18 7.743 ERROR: Cannot install None because these package versions have conflicting dependencies.
#18 7.744
#18 7.744 The conflict is caused by:
#18 7.744     fish-speech 2.0.0 depends on torch==2.8.0
#18 7.744     The user requested (constraint) torch==2.4.1
#18 7.744
#18 7.744 Additionally, some packages in these conflicts have no matching distributions available for your environment:
#18 7.744     torch
#18 7.744
#18 7.744 To fix this you could try to:
#18 7.744 1. loosen the range of package versions you've specified
#18 7.744 2. remove package versions to allow pip to attempt to solve the dependency conflict
#18 7.744
#18 7.744 ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/topics/dependency-resolution/#dealing-with-dependency-conflicts
#18 ERROR: process "/bin/sh -c python -m pip install     --no-cache-dir     --constraint /app/pytorch-constraints.txt     -e \".[stable]\"" did not complete successfully: exit code: 1
------
 > [stage-0 10/16] RUN python -m pip install     --no-cache-dir     --constraint /app/pytorch-constraints.txt     -e ".[stable]":
7.744     The user requested (constraint) torch==2.4.1
7.744
7.744 Additionally, some packages in these conflicts have no matching distributions available for your environment:
7.744     torch
7.744
7.744 To fix this you could try to:
7.744 1. loosen the range of package versions you've specified
7.744 2. remove package versions to allow pip to attempt to solve the dependency conflict
7.744
7.744 ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/topics/dependency-resolution/#dealing-with-dependency-conflicts
------
ERROR: failed to build: failed to solve: process "/bin/sh -c python -m pip install     --no-cache-dir     --constraint /app/pytorch-constraints.txt     -e \".[stable]\"" did not complete successfully: exit code: 1
