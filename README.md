# NexMove
Repository for the source code of our project NexMove: An interactive app for mobility data interactivity. Made by Nerea Gonzalez, Raul Fuente, Laura Quiñonero, Mar Climente &amp; Daniel Amirian

## Teaser
[![Watch our teaser in Youtube](https://img.youtube.com/vi/SBpZzWt_Wc4/0.jpg)](https://www.youtube.com/watch?v=SBpZzWt_Wc4)

## Demo App

Check out our interactive app by clicking the badge below:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nexmove.streamlit.app/)


## Exploratory Data Analysis
[![Colab Notebook](https://colab.research.google.com/assets/colab-badge.svg)](https://github.com/daniampr/NexMove/blob/main/notebooks/EDA-project.ipynb)

Checkout our Exploratory Data Analysis of the dataset used in the project. The notebook is available in the link above.

## Setting up the environment

### 0. Prerequisites

Recommended to have the version of python 3.12.6. Upper versions may not work properly. If you are using Windows as operative system, you may download the [Windows Installer (64-bit)](https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe) executable, if you are using MacOS, you may download the [macOS 64-bit universal2 installer](https://www.python.org/ftp/python/3.12.6/python-3.12.6-macos11.pkg) version. For other operative systems or specific versions, checkout the [release page](https://www.python.org/downloads/release/python-3126/) of the python version.


**Important**: Make sure to check the box **"Add Python 3.12 to PATH"** during the installation process.


### 1. Clone the repository
Clone our repository to your local machine using the following command:
```bash
git clone https://github.com/daniampr/NexMove.git
```

### 2. Create a virtual environment
Create a virtual environment in the root directory of the project:
```bash
python -m venv .venv
```
To activate the virtual environment, run:
```bash
source .venv/bin/activate # For MacOS
.\.venv\Scripts\activate  # For Windows
```

### 3. Install the dependencies
Install the required dependencies using the following command:
```bash
pip install -r requirements.txt
```

### 4. Run the application
To run the application, execute the following commands:
```bash
cd src
streamlit run app.py
```

