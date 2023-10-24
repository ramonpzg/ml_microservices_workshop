# Building Machine Learning Microservices for Music Generation

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ramonpzg/ml_microservices_workshop)

## Description

This workshop focuses on building machine learning microservices for different uses cases in the 
music industry. To follow along, please go over the Set Up instructions below.

## Objectives

By the end of the workshop, you will be able to
- create different machine learning microservices
- build user interfaces for your applications
- connect different models together
- understand what music is and how to tweak it

## Assumptions about the Learner

1. At least a year of experience coding
2. Knows how to use virtual environments
3. Does not mind using jupyter notebooks 😎

## Ideal set up for the full workshop
- You will need to have `ffmpeg` and `docker` installed
- At least 15GB of disk space available
- At least 16 GB of memory ram available

For linux
```sh
sudo apt-get install ffmpeg
```

For Mac
```sh
brew install ffmpeg
```

## Step-by-Step Setup

#### First Step

Open up your terminal and navigate to a directory of your choosing in your computer. Once there, run the following command to get the code for the session.

```sh
 git clone https://github.com/ramonpzg/ml_microservices_workshop.git
```

Conversely, you can click on the green `download` button at the top and download all
files to your desired folder/directory. Once you download it, unzip it and move on
to the second step.

#### Second Step

To get all dependencies, packages and everything else that would be useful in this
tutorial, you can recreate the environment by first going into the directory for today.

```sh
cd ml_microservices_workshop
```

Then you will need to create an environment with all of the dependencies needed for the session by running the following command.

```sh
mamba create -n ml_micro_svc python=3.11
mamba activate ml_micro_svc
pip install -r requirements.txt

## OR

conda create -n ml_micro_svc python=3.11
conda activate ml_micro_svc
pip install -r requirements.txt

## OR

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
#### Third Step

Open up Jupyter Lab and you should be ready to go.

```sh
code .

## OR

jupyter lab
```

You're all set. Now navigate to `1_microservices` directory and open the `tutorial.ipynb` notebook.



## Resources

**Micro-Services**
- [MLServer](https://mlserver.readthedocs.io/en/latest/)
- [Gradio](gradio.app)
- [nicegui](nicegui.io)

**Music/Audio**
- [Music information retrieval with Python — Mateusz Modrzejewski](https://www.youtube.com/watch?v=kHM5pJoxh1A)
- [Neural Audio Effects || Christian Steinmetz](https://www.youtube.com/watch?v=qy6qNvV1RZY)
- [Lessons Learned from a Decade of Audio Programming](https://www.youtube.com/watch?v=Vjm--AqG04Y)
- [Working with Audio in Python (feat. Pedalboard) - presented by Peter Sobot](https://www.youtube.com/watch?v=NYhkqXpFAlg)

**Tools to Try**
- [FoxDot](https://foxdot.org/)
- [librosa](https://librosa.org/doc/latest/)
- [pedalboard](https://spotify.github.io/pedalboard/index.html)
- [demucs](https://github.com/facebookresearch/demucs)