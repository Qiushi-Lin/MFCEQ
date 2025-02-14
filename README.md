# MFC-EQ

The code implementation for MFC-EQ: Mean Field Control with Envelope Q-learning for Moving Decentralized Agents in Formation.

![til](https://raw.githubusercontent.com/Qiushi-Lin/MFCEQ/master/assets/demonstration.gif)

## Setup
**Dependencies**
Create the virtual environment and install the required packages.
```
conda create -n mfceq python=3.10
pip install -r requirement.txt
conda activate mfceq
```

**Benchmarks**
Generate the test set used for evaluation.
```
cd benchmarks
python create_test.py
```

## Train
  ``python train.py``

## Evaluate
  ``python evaluate.py --load_from_dir path/to/dir``

# Contact
If you have any questions or issues, please contact me through this email, qiushi_lin@sfu.ca.
