"""
Main Application Window
Contains the main UI logic and widget setup for the Quadric Visualizer.
"""

import customtkinter as ctk
import warnings

from .control_panel import ControlPanel
from .plot_panel import PlotPanel

warnings.filterwarnings('ignore')

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class QuadricApp(ctk.CTk):
    """Main application class for Quadric Surface Visualizer"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Quadric Surface Visualizer - Interactive 3D Viewer")
        self.geometry("1400x900")
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main panels
        self.control_panel = ControlPanel(self)
        self.control_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.plot_panel = PlotPanel(self)
        self.plot_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Connect panels
        self.control_panel.set_plot_panel(self.plot_panel)
        
        # Initial plot
        self.control_panel.plot_surface()
