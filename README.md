# Quadric Surface Visualizer

A professional 3D interactive viewer and classifier for standard quadric surfaces with a modern GUI.

## Quick Start - Double-Click to Run!

**EASIEST WAY:** Just double-click the ready EXE file:

```
📂 dist/QuadricVisualizer.exe  ← Double-click this!
```

✅ No Python installation needed!  
✅ No dependencies to install!  
✅ Works immediately!

See [QUICK_START.md](QUICK_START.md) for more details.

## Features

- Interactive 3D visualization of quadric surfaces
- Support for 7 types of quadric surfaces:
  - Ellipsoid
  - Elliptic Cone
  - Hyperboloid of One Sheet
  - Hyperboloid of Two Sheets
  - Elliptic Paraboloid
  - Hyperbolic Paraboloid
  - Cylinder
- Customizable parameters and center coordinates
- Real-time analysis with equations and descriptions
- Dark mode UI with CustomTkinter

## Project Structure

```
Analytic-Geometry-Prefinal/
├── main.py                 # Entry point
├── src/
│   ├── __init__.py
│   ├── models/            # Mathematical models
│   │   ├── __init__.py
│   │   └── quadric_surfaces.py
│   ├── ui/                # User interface
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── control_panel.py
│   │   └── plot_panel.py
│   └── utils/             # Utility functions
│       ├── __init__.py
│       ├── equations.py
│       └── descriptions.py
├── quadric_visualizer.py  # Legacy file (deprecated)
└── README.md
```

## Installation

### Requirements

- Python 3.8+
- customtkinter
- numpy
- matplotlib

### Install dependencies

```bash
pip install customtkinter numpy matplotlib
```

## Usage

### Method 1: Quick Start (Double-click)

Simply double-click the `run.bat` file in the project root:

```
📂 Analytic-Geometry-Prefinal/
   └── run.bat  ← Double-click this!
```

### Method 2: Command Line

```bash
python main.py
```

### Method 3: Create Standalone EXE

Build a standalone executable that doesn't require Python:

```bash
python build_exe.py
```

Then double-click `dist/QuadricVisualizer.exe`

**See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) for detailed instructions.**

## Features by Module

### Models (`src/models/`)
- `quadric_surfaces.py`: Mathematical definitions and coordinate generation for all quadric surfaces
- `SurfaceType`: Enum for surface types
- `SurfaceParameters`: Data class for surface parameters
- `QuadricSurface`: Main class for surface generation

### UI (`src/ui/`)
- `main_window.py`: Main application window
- `control_panel.py`: Left panel with controls and parameter inputs
- `plot_panel.py`: Right panel with 3D plot and analysis

### Utils (`src/utils/`)
- `equations.py`: Generates canonical equations for surfaces
- `descriptions.py`: Provides qualitative descriptions

## Author

Nurdaulet Sovetkhan
Astana IT University
