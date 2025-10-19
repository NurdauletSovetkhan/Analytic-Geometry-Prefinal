"""
Control Panel Module
Handles all user input controls and parameters for the quadric visualizer.
"""

import customtkinter as ctk
import numpy as np
from typing import Optional, Dict

from models.quadric_surfaces import SurfaceType, SurfaceParameters


class ControlPanel(ctk.CTkFrame):
    """Left control panel with all user inputs and controls"""
    
    def __init__(self, master):
        super().__init__(master, width=350)
        self.grid_propagate(False)
        
        # Surface types
        self.surface_type_map = {
            "Ellipsoid": SurfaceType.ELLIPSOID,
            "Elliptic Cone": SurfaceType.ELLIPTIC_CONE,
            "Hyperboloid of One Sheet": SurfaceType.HYPERBOLOID_ONE_SHEET,
            "Hyperboloid of Two Sheets": SurfaceType.HYPERBOLOID_TWO_SHEETS,
            "Elliptic Paraboloid": SurfaceType.ELLIPTIC_PARABOLOID,
            "Hyperbolic Paraboloid": SurfaceType.HYPERBOLIC_PARABOLOID,
            "Cylinder": SurfaceType.CYLINDER
        }
        
        # Initialize variables
        self.current_surface = ctk.StringVar(value="Ellipsoid")
        self.orientation = ctk.StringVar(value="Z")
        
        # Default parameters
        self.default_params = {
            'a': 2.0,
            'b': 3.0,
            'c': 4.0,
            'h': 0.0,
            'k': 0.0,
            'l': 0.0,
            'range_min': -10.0,
            'range_max': 10.0
        }
        
        self.plot_panel = None
        
        # Build UI
        self._create_widgets()
    
    def set_plot_panel(self, plot_panel):
        """Set the plot panel reference"""
        self.plot_panel = plot_panel
    
    def _create_widgets(self):
        """Create all control widgets"""
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Quadric Surface Controls",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(10, 20), padx=10)
        
        # Surface Selection
        surface_label = ctk.CTkLabel(
            self,
            text="Surface Type:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        surface_label.pack(pady=(5, 5), padx=10, anchor="w")
        
        self.surface_menu = ctk.CTkOptionMenu(
            self,
            variable=self.current_surface,
            values=list(self.surface_type_map.keys()),
            command=self._on_surface_change,
            width=320
        )
        self.surface_menu.pack(pady=(0, 15), padx=10)
        
        # Orientation Selection
        self.orientation_label = ctk.CTkLabel(
            self,
            text="Axis of Symmetry:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.orientation_label.pack(pady=(5, 5), padx=10, anchor="w")
        
        self.orientation_menu = ctk.CTkOptionMenu(
            self,
            variable=self.orientation,
            values=["X", "Y", "Z"],
            width=320
        )
        self.orientation_menu.pack(pady=(0, 15), padx=10)
        
        # Parameters Frame
        params_frame = ctk.CTkFrame(self)
        params_frame.pack(pady=(5, 10), padx=10, fill="x")
        
        param_label = ctk.CTkLabel(
            params_frame,
            text="Parameters (a, b, c > 0):",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        param_label.pack(pady=(10, 10), padx=10, anchor="w")
        
        # Parameter inputs
        self.param_entries = {}
        params = [('a', 'Semi-axis a:'), ('b', 'Semi-axis b:'), ('c', 'Semi-axis c:')]
        
        for param_name, param_label_text in params:
            self._create_parameter_entry(params_frame, param_name, param_label_text)
        
        # Center coordinates
        center_label = ctk.CTkLabel(
            params_frame,
            text="Center (h, k, l):",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        center_label.pack(pady=(15, 10), padx=10, anchor="w")
        
        centers = [('h', 'h:'), ('k', 'k:'), ('l', 'l:')]
        
        for param_name, param_label_text in centers:
            self._create_parameter_entry(params_frame, param_name, param_label_text)
        
        # Axis Range
        range_label = ctk.CTkLabel(
            params_frame,
            text="Axis Range:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        range_label.pack(pady=(15, 10), padx=10, anchor="w")
        
        ranges = [('range_min', 'Min:'), ('range_max', 'Max:')]
        
        for param_name, param_label_text in ranges:
            self._create_parameter_entry(params_frame, param_name, param_label_text)
        
        # Buttons Frame
        self._create_buttons()
        
        # Update orientation visibility
        self._on_surface_change(self.current_surface.get())
    
    def _create_parameter_entry(self, parent, param_name: str, label_text: str):
        """Create a single parameter entry row"""
        param_container = ctk.CTkFrame(parent, fg_color="transparent")
        param_container.pack(pady=3, padx=10, fill="x")
        
        label = ctk.CTkLabel(param_container, text=label_text, width=100, anchor="w")
        label.pack(side="left", padx=(0, 5))
        
        entry = ctk.CTkEntry(param_container, width=200)
        entry.insert(0, str(self.default_params[param_name]))
        entry.pack(side="left")
        
        self.param_entries[param_name] = entry
    
    def _create_buttons(self):
        """Create action buttons"""
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(pady=20, padx=10, fill="x")
        
        plot_button = ctk.CTkButton(
            buttons_frame,
            text="Plot Surface",
            command=self.plot_surface,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        plot_button.pack(pady=5)
        
        randomize_button = ctk.CTkButton(
            buttons_frame,
            text="Randomize Parameters",
            command=self.randomize_parameters,
            width=150,
            height=35
        )
        randomize_button.pack(pady=5)
        
        clear_button = ctk.CTkButton(
            buttons_frame,
            text="Clear Plot",
            command=self.clear_plot,
            width=150,
            height=35,
            fg_color="gray40",
            hover_color="gray30"
        )
        clear_button.pack(pady=5)
    
    def _on_surface_change(self, choice: str):
        """Handle surface type change"""
        if choice == "Ellipsoid":
            self.orientation_label.pack_forget()
            self.orientation_menu.pack_forget()
        elif choice == "Cylinder":
            self.orientation_label.configure(text="Missing Axis (extends infinitely):")
            self._repack_orientation()
        else:
            self.orientation_label.configure(text="Axis of Symmetry:")
            self._repack_orientation()
    
    def _repack_orientation(self):
        """Repack orientation widgets in correct position"""
        # Get the index before params frame
        children = list(self.winfo_children())
        params_frame_index = children.index([w for w in children if isinstance(w, ctk.CTkFrame) and w != self][0])
        
        self.orientation_label.pack(pady=(5, 5), padx=10, anchor="w", before=children[params_frame_index])
        self.orientation_menu.pack(pady=(0, 15), padx=10, before=children[params_frame_index])
    
    def validate_and_get_params(self) -> Optional[Dict]:
        """Validate and retrieve all parameters"""
        try:
            params = {}
            for key, entry in self.param_entries.items():
                value = float(entry.get())
                
                # Validate that a, b, c are positive
                if key in ['a', 'b', 'c'] and value <= 0:
                    raise ValueError(f"Parameter {key} must be positive (> 0)")
                
                params[key] = value
            
            # Validate range
            if params['range_min'] >= params['range_max']:
                raise ValueError("Range minimum must be less than range maximum")
            
            return params
        
        except ValueError as e:
            self._show_error(str(e))
            return None
    
    def _show_error(self, message: str):
        """Display error message"""
        error_window = ctk.CTkToplevel(self)
        error_window.title("Input Error")
        error_window.geometry("400x150")
        error_window.transient(self.master)
        error_window.grab_set()
        
        label = ctk.CTkLabel(
            error_window,
            text=message,
            font=ctk.CTkFont(size=13),
            wraplength=350
        )
        label.pack(pady=20, padx=20)
        
        button = ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy,
            width=100
        )
        button.pack(pady=10)
    
    def randomize_parameters(self):
        """Generate random parameters"""
        for param in ['a', 'b', 'c']:
            value = np.random.uniform(1, 10)
            self.param_entries[param].delete(0, 'end')
            self.param_entries[param].insert(0, f"{value:.2f}")
        
        for param in ['h', 'k', 'l']:
            value = np.random.uniform(-3, 3)
            self.param_entries[param].delete(0, 'end')
            self.param_entries[param].insert(0, f"{value:.2f}")
    
    def clear_plot(self):
        """Clear the plot and reset parameters"""
        if self.plot_panel:
            self.plot_panel.clear_plot()
        
        # Reset to default parameters
        for key, value in self.default_params.items():
            self.param_entries[key].delete(0, 'end')
            self.param_entries[key].insert(0, str(value))
    
    def plot_surface(self):
        """Trigger surface plotting"""
        params_dict = self.validate_and_get_params()
        if params_dict is None or self.plot_panel is None:
            return
        
        # Create surface parameters
        params = SurfaceParameters(
            a=params_dict['a'],
            b=params_dict['b'],
            c=params_dict['c'],
            h=params_dict['h'],
            k=params_dict['k'],
            l=params_dict['l']
        )
        
        # Get surface type
        surface_name = self.current_surface.get()
        surface_type = self.surface_type_map[surface_name]
        
        # Plot
        self.plot_panel.plot_surface(
            surface_type=surface_type,
            params=params,
            orientation=self.orientation.get(),
            range_min=params_dict['range_min'],
            range_max=params_dict['range_max']
        )
