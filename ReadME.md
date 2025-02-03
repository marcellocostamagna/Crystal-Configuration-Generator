# Crystal Configuration Generator

## Overview

The **Crystal Configuration Generator** is a Python-based tool designed to generate and visualize different configurations of crystal structures. Users can modify the coordination sphere and the number of Bromine (Br) atoms in the script to generate unique configurations. The generator uses symmetry operations to normalize configurations and reduce redundancy.



---

## Installation

### 1. Clone the Repository
First, clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/crystal-config-generator.git
cd crystal-config-generator
```

### 2. Set up the Conda Environment

This project uses a Conda environment, so you’ll need to install dependencies from the `environment.yml` file. Run the following commands to set up the environment:

```bash
conda env create -f environment.yml
conda activate crys_conf
```
This will create a Conda environment named `crys_conf` with all required dependencies.

## Running the Script

Once the environment is activated, you can run the script to generate configurations:

```bash
python generate_configurations.py
```

## Run with Streamlit

You can also interact with the Crystal Configuration Generator using a Streamlit web app interface.

To run the app, in the `scripts` folder, use the following command:

```bash
streamlit run CCG.py
```

## Run online

The easiest way to run the Crystal Configuration Generator!

https://crystal-configuration-generator-42dau7snrjleakmbof5pxd.streamlit.app/
