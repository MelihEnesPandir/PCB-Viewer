# PCB-Viewer
Interactive PCB component placement viewer built with Python, Tkinter and Matplotlib.

A Python-based **PCB component placement viewer** built with **Tkinter** and **Matplotlib**.  
It reads a component placement file (`.txt`), visualizes the PCB with colored footprints,  
and allows interactive inspection of each component.

## ✨ Features
- Load PCB placement data from a semicolon-separated `.txt` file  
- Display PCB with colored footprints by package type  
- Interactive component info popup (click on a reference designator to view details)  
- Rotate components directly from the popup (`+90°` each click, auto reset at 360°)  
- Updates both the visualization and the source `.txt` file in real-time  

## 📂 Example Data Format
The viewer expects a `.txt` file with the following structure:

Comp;Ref;X;Y;R;Package

10080001;D2;30,702;4,258;180;MELF

10080001;D1;30,691;14,766;0;MELF

10140017;Q1;38,1;16,655;0;8-PQFN

- **Ref** → Reference designator (R1, C1, Q1, etc.)  
- **X, Y** → Position in mm  
- **R** → Rotation in degrees (0–360)  
- **Package** → Component package type  

## ▶️ Usage
1-Click “Load File” and select your PCB placement .txt file

2-The PCB will be displayed

3-Click on a component’s reference (e.g., R3, Q1) to see details

4-Use the Rotate (+90°) button in the popup to rotate the component

## 📦 Requirements
Python 3.8+
Matplotlib
Pandas
NumPy
