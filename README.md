# Twitter Data Analysis
Code for retrieving and analysing useful tweets from Twitter.

## Setup
First, clone the code:
```
$ cd /path/to/your/folder
$ git clone https://github.com/Swadesh13/Tweet-Analysis.git
$ cd Tweet-Analysis
```

There are 3 files for setting up the environment. Choose any one -
* requirements.txt
* environment.yml (Conda)
*  spec-file.txt (Conda)

It is recommended to setup a Conda environment for this project. You can use Miniconda from [here](https://docs.conda.io/en/latest/miniconda.html) to get a lightweight, bootstrap version of Anaconda.

For using the environment.yml provided with the code, run:
```
$ conda env create -f environment.yml -p ./env
```
OR
```
$ conda create --file spec-file.txt -p ./env
```

Finally, to activate the environment:
```
$ conda activate ./env
```

You can also download the dependencies from the requirements.txt:
```
$ pip install -r requirements.txt
```

If you are using VS Code, the .vscode/settings.json file might be useful for you. Note that, if you are adding any new folder in src/ then add the path to the list "python.analysis.extraPaths" or else pylance will give an error.