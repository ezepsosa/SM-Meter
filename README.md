# SM-Meter Compilation Guide

Welcome! Here you will find the instructions to compile and run the project in your local environment. To get started, we have two options:

## Option A: GPU Usage

This option involves using a GPU compatible with TensorFlow to launch the project and make predictions. Make sure you have a GPU compatible with TensorFlow GPU. You can check the list of compatible GPUs [here](https://www.tensorflow.org/install/gpu?hl=en).

### Steps to follow:

1. Download and install Anaconda from [here](https://www.anaconda.com/products/distribution).
2. Open an Anaconda terminal (Anaconda PowerShell Prompt) and execute the following commands:
    ```bash
    conda create --name tf-gpu
    conda activate tf-gpu
    conda install python
    ```
3. Install all necessary packages by executing the following command in the Anaconda terminal:
    ```bash
    pip install -r requirements.txt
    ```
   Remember to execute the second line of code each time you want to launch the project.

## Option B: CPU Usage (Default Option)

This option involves using the CPU to launch the project and make predictions.

### Steps to follow:

1. Download and install Python from [here](https://www.python.org/downloads/). Python 3 is recommended.
2. Make sure you have pip installed. If it is not installed automatically with Python, follow the instructions [here](https://pip.pypa.io/en/stable/installation/).
3. Install all necessary packages by executing the following command in the terminal:
    ```bash
    pip install -r requirements.txt
    ```

Once you have completed the above steps, you will be ready to compile and run the project.

## Application Usage

**Note:** Before proceeding, please make sure to configure your own API credentials. You can either refer to the last section for instructions (***General Options, API Options & About***) or set up your credentials by creating a `config.ini` file using the example file provided in the repository.

### Home Window

The home window serves as a starting point to initiate various types of analysis. It includes an input field where you can specify the column to analyze in a CSV file. To begin using the application, simply execute the `main.py` file.
  <img src="https://github.com/ezepsosa/SM-Meter/blob/main/assets/main_screen.jpg" alt="Home window" width="600"/>
### Real-Time Analysis

In the real-time analysis window, you'll find three graphs displaying different metrics. These graphs are updated every 60 seconds, providing real-time insights based on the ongoing analysis. To start analyzing real-time data, execute the `main.py` file.

<img src="https://github.com/ezepsosa/SM-Meter/blob/main/assets/main_view_executed.jpg" alt="Real time analysis" width="600"/>

### Custom Analysis

The custom analysis window offers functionalities similar to real-time analysis, but with the flexibility to customize the parameters of the analysis. To initiate a custom analysis session, execute the `main.py` file and go to the custom analysis tab.

<img src="https://github.com/ezepsosa/SM-Meter/blob/main/assets/main_view_executed_2.jpg" alt="Real time analysis customized" width="600"/>

### General Options, API Options & About

The general options window allows you to manage the models used in the analysis. You can start or stop models as needed. To configure the application's general settings, execute the `main.py` file and access the general options tab.

For the API options, you have the flexibility to provide your own API credentials to interact with third-party services like Twitter and Reddit. By default, the application uses free APIs, but you can customize this configuration to enhance your usage. To adjust API settings, execute the `main.py` file and navigate to the API options tab.

<div style="display: flex;">
    <img src="https://github.com/ezepsosa/SM-Meter/blob/main/assets/general_tab.jpg" alt="General options tab" width="200" style="margin-right: 20px;"/>
    <img src="https://github.com/ezepsosa/SM-Meter/blob/main/assets/api_tab.jpg" alt="API options tab" width="200" style="margin-right: 20px;"/>
    <img src="https://github.com/ezepsosa/SM-Meter/blob/main/assets/about_tab.jpg" alt="About tab" width="200"/>
</div>
