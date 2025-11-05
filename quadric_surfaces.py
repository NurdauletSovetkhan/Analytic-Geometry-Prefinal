"""
Interactive Quadric Surfaces Visualizer
Design an interactive Python program that visualizes and classifies all standard quadric surfaces
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk, messagebox
import random


class QuadricSurfaceVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Quadric Surfaces in R³")
        self.root.geometry("1400x900")
        
        # Surface types
        self.surface_types = {
            1: "Ellipsoid",
            2: "Elliptic Cone",
            3: "Hyperboloid of One Sheet",
            4: "Hyperboloid of Two Sheets",
            5: "Elliptic Paraboloid",
            6: "Hyperbolic Paraboloid",
            7: "Cylinders"
        }
        
        self.cylinder_types = ["Elliptic", "Hyperbolic", "Parabolic"]
        self.orientations = ["z-axis", "y-axis", "x-axis"]
        
        # Quality settings for performance
        self.quality_level = 50  # Lower = faster, Higher = smoother
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Ensure the left control column has a sensible minimum width so controls don't overflow
        main_frame.columnconfigure(0, minsize=360)
        
        # Left panel - Controls
        control_frame = ttk.LabelFrame(main_frame, text="Control Panel", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Surface Type Selection
        ttk.Label(control_frame, text="Surface Type:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.surface_var = tk.IntVar(value=1)
        for i, (key, name) in enumerate(self.surface_types.items()):
            ttk.Radiobutton(control_frame, text=f"{key}. {name}", 
                           variable=self.surface_var, value=key,
                           command=self.on_surface_change).grid(row=i+1, column=0, sticky=tk.W, padx=10)
        
        # Cylinder Type (for cylinder selection)
        self.cylinder_frame = ttk.Frame(control_frame)
        self.cylinder_frame.grid(row=8, column=0, sticky=tk.W, padx=20)
        ttk.Label(self.cylinder_frame, text="Cylinder Type:").grid(row=0, column=0, sticky=tk.W)
        self.cylinder_var = tk.StringVar(value="Elliptic")
        for i, ctype in enumerate(self.cylinder_types):
            ttk.Radiobutton(self.cylinder_frame, text=ctype, 
                           variable=self.cylinder_var, value=ctype).grid(row=i+1, column=0, sticky=tk.W, padx=10)
        self.cylinder_frame.grid_remove()
        
        # Orientation Selection
        ttk.Label(control_frame, text="Orientation (axis of symmetry):", 
                 font=("Arial", 10, "bold")).grid(row=9, column=0, sticky=tk.W, pady=(10,5))
        self.orientation_var = tk.StringVar(value="z-axis")
        self.orientation_frame = ttk.Frame(control_frame)
        self.orientation_frame.grid(row=10, column=0, sticky=tk.W, padx=10)
        for i, orient in enumerate(self.orientations):
            ttk.Radiobutton(self.orientation_frame, text=f"Along {orient}", 
                           variable=self.orientation_var, value=orient).grid(row=i, column=0, sticky=tk.W, padx=10)
        
        # Parameters
        param_frame = ttk.LabelFrame(control_frame, text="Parameters", padding="10")
        param_frame.grid(row=11, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(param_frame, text="a (> 0):").grid(row=0, column=0, sticky=tk.W)
        self.a_var = tk.StringVar(value="2")
        ttk.Entry(param_frame, textvariable=self.a_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(param_frame, text="b (> 0):").grid(row=1, column=0, sticky=tk.W)
        self.b_var = tk.StringVar(value="1.5")
        ttk.Entry(param_frame, textvariable=self.b_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(param_frame, text="c (> 0):").grid(row=2, column=0, sticky=tk.W)
        self.c_var = tk.StringVar(value="1")
        ttk.Entry(param_frame, textvariable=self.c_var, width=10).grid(row=2, column=1, padx=5)
        
        ttk.Label(param_frame, text="p (for parabolic):").grid(row=3, column=0, sticky=tk.W)
        self.p_var = tk.StringVar(value="1")
        ttk.Entry(param_frame, textvariable=self.p_var, width=10).grid(row=3, column=1, padx=5)
        
        # Center coordinates
        center_frame = ttk.LabelFrame(control_frame, text="Center (h, k, l)", padding="10")
        center_frame.grid(row=12, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(center_frame, text="h:").grid(row=0, column=0, sticky=tk.W)
        self.h_var = tk.StringVar(value="0")
        ttk.Entry(center_frame, textvariable=self.h_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(center_frame, text="k:").grid(row=1, column=0, sticky=tk.W)
        self.k_var = tk.StringVar(value="0")
        ttk.Entry(center_frame, textvariable=self.k_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(center_frame, text="l:").grid(row=2, column=0, sticky=tk.W)
        self.l_var = tk.StringVar(value="0")
        ttk.Entry(center_frame, textvariable=self.l_var, width=10).grid(row=2, column=1, padx=5)
        
        # Range settings
        range_frame = ttk.LabelFrame(control_frame, text="Visible Range", padding="10")
        range_frame.grid(row=13, column=0, sticky=(tk.W, tk.E), pady=10)
        # Allow the Visible Range frame columns to expand/shrink responsively
        for _col in range(4):
            range_frame.columnconfigure(_col, weight=1)
        
        ranges = [("xmin", "xmax"), ("ymin", "ymax"), ("zmin", "zmax")]
        self.range_vars = {}
        for i, (rmin, rmax) in enumerate(ranges):
            ttk.Label(range_frame, text=f"{rmin}:").grid(row=i, column=0, sticky=tk.W)
            self.range_vars[rmin] = tk.StringVar(value="-10")
            ttk.Entry(range_frame, textvariable=self.range_vars[rmin], width=8).grid(row=i, column=1, padx=2, sticky=(tk.W, tk.E))
            
            ttk.Label(range_frame, text=f"{rmax}:").grid(row=i, column=2, sticky=tk.W, padx=(10,0))
            self.range_vars[rmax] = tk.StringVar(value="10")
            ttk.Entry(range_frame, textvariable=self.range_vars[rmax], width=8).grid(row=i, column=3, padx=2, sticky=(tk.W, tk.E))
        
        # Quality settings
        quality_frame = ttk.LabelFrame(control_frame, text="Rendering Quality", padding="10")
        quality_frame.grid(row=13, column=0, sticky=(tk.W, tk.E), pady=10)
        quality_frame.grid_remove()  # Hide for now, can be shown if needed
        
        ttk.Label(quality_frame, text="Quality (25-100):").grid(row=0, column=0, sticky=tk.W)
        self.quality_var = tk.IntVar(value=50)
        quality_slider = ttk.Scale(quality_frame, from_=25, to=100, orient=tk.HORIZONTAL,
                                   variable=self.quality_var, length=150)
        quality_slider.grid(row=0, column=1, padx=5)
        self.quality_label = ttk.Label(quality_frame, text="50")
        self.quality_label.grid(row=0, column=2)
        
        def update_quality_label(event=None):
            val = self.quality_var.get()
            self.quality_label.config(text=str(val))
            self.quality_level = val
        
        quality_slider.configure(command=lambda v: update_quality_label())
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=14, column=0, pady=10)
        
        ttk.Button(button_frame, text="Plot", command=self.plot_surface, 
                  width=12).grid(row=0, column=0, padx=3, pady=5)
        ttk.Button(button_frame, text="Randomize", command=self.randomize_parameters,
                  width=12).grid(row=0, column=1, padx=3, pady=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_plot,
                  width=12).grid(row=0, column=2, padx=3, pady=5)
        
        # Quality buttons
        quality_btn_frame = ttk.LabelFrame(control_frame, text="⚡ Quick Quality", padding="5")
        quality_btn_frame.grid(row=15, column=0, pady=5)
        
        ttk.Button(quality_btn_frame, text="Low (Fast)", 
                  command=lambda: self.set_quality(15), width=10).grid(row=0, column=0, padx=2)
        ttk.Button(quality_btn_frame, text="Medium", 
                  command=lambda: self.set_quality(50), width=10).grid(row=0, column=1, padx=2)
        ttk.Button(quality_btn_frame, text="High", 
                  command=lambda: self.set_quality(75), width=10).grid(row=0, column=2, padx=2)
        
        # Right panel - Visualization and Analysis
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # 3D Plot
        self.fig = plt.Figure(figsize=(10, 7), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Enable better performance
        self.ax.set_proj_type('persp')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add navigation toolbar for zoom/pan
        toolbar_frame = ttk.Frame(right_frame)
        toolbar_frame.grid(row=0, column=0, sticky=(tk.N, tk.W))
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()
        
        # Analysis Results
        analysis_frame = ttk.LabelFrame(right_frame, text="📊 Analysis Results", padding="10")
        analysis_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.analysis_text = tk.Text(analysis_frame, height=8, width=80, wrap=tk.WORD, 
                                     font=("Consolas", 9))
        self.analysis_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        scrollbar = ttk.Scrollbar(analysis_frame, orient=tk.VERTICAL, command=self.analysis_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.analysis_text['yscrollcommand'] = scrollbar.set
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        
    def on_surface_change(self):
        surface_type = self.surface_var.get()
        
        # Show/hide cylinder type selection
        if surface_type == 7:
            self.cylinder_frame.grid()
        else:
            self.cylinder_frame.grid_remove()
        
        # Show/hide orientation for ellipsoid
        if surface_type == 1:
            self.orientation_frame.grid_remove()
        else:
            self.orientation_frame.grid()
    
    def validate_inputs(self):
        try:
            a = float(self.a_var.get())
            b = float(self.b_var.get())
            c = float(self.c_var.get())
            p = float(self.p_var.get())
            h = float(self.h_var.get())
            k = float(self.k_var.get())
            l = float(self.l_var.get())
            
            if a <= 0 or b <= 0 or c <= 0:
                messagebox.showerror("Invalid Input", "Parameters a, b, c must be greater than 0!")
                return None
            
            ranges = {}
            for key, var in self.range_vars.items():
                ranges[key] = float(var.get())
            
            return {
                'a': a, 'b': b, 'c': c, 'p': p,
                'h': h, 'k': k, 'l': l,
                'ranges': ranges
            }
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values!")
            return None
    
    def randomize_parameters(self):
        self.a_var.set(str(round(random.uniform(1, 10), 2)))
        self.b_var.set(str(round(random.uniform(1, 10), 2)))
        self.c_var.set(str(round(random.uniform(1, 10), 2)))
        self.p_var.set(str(round(random.uniform(0.5, 5), 2)))
    
    def set_quality(self, quality):
        """Set rendering quality level"""
        self.quality_level = quality
        self.root.update_idletasks()
    
    def clear_plot(self):
        self.ax.clear()
        self.canvas.draw()
        self.analysis_text.delete(1.0, tk.END)
    
    def plot_surface(self):
        params = self.validate_inputs()
        if params is None:
            return
        
        self.clear_plot()
        
        surface_type = self.surface_var.get()
        orientation = self.orientation_var.get()
        
        a, b, c, p = params['a'], params['b'], params['c'], params['p']
        h, k, l = params['h'], params['k'], params['l']
        ranges = params['ranges']
        
        # Create meshgrid with adjustable quality
        resolution = self.quality_level
        x = np.linspace(ranges['xmin'], ranges['xmax'], resolution)
        y = np.linspace(ranges['ymin'], ranges['ymax'], resolution)
        z = np.linspace(ranges['zmin'], ranges['zmax'], resolution)
        
        analysis_info = f"--- Analysis Results ---\n"
        analysis_info += f"Surface Type: {self.surface_types[surface_type]}\n"
        
        if surface_type == 7:
            analysis_info += f"Cylinder Type: {self.cylinder_var.get()}\n"
        
        if surface_type != 1:
            analysis_info += f"Orientation: Along {orientation}\n"
        
        analysis_info += f"Parameters: a={a}, b={b}, c={c}"
        if surface_type == 7 and self.cylinder_var.get() == "Parabolic":
            analysis_info += f", p={p}"
        analysis_info += f"\nCenter: ({h}, {k}, {l})\n"
        analysis_info += f"Range: x in [{ranges['xmin']}, {ranges['xmax']}], "
        analysis_info += f"y in [{ranges['ymin']}, {ranges['ymax']}], "
        analysis_info += f"z in [{ranges['zmin']}, {ranges['zmax']}]\n"
        
        try:
            if surface_type == 1:
                self.plot_ellipsoid(a, b, c, h, k, l, analysis_info)
            elif surface_type == 2:
                self.plot_elliptic_cone(a, b, c, h, k, l, orientation, analysis_info)
            elif surface_type == 3:
                self.plot_hyperboloid_one_sheet(a, b, c, h, k, l, orientation, analysis_info)
            elif surface_type == 4:
                self.plot_hyperboloid_two_sheets(a, b, c, h, k, l, orientation, analysis_info)
            elif surface_type == 5:
                self.plot_elliptic_paraboloid(a, b, c, h, k, l, orientation, analysis_info)
            elif surface_type == 6:
                self.plot_hyperbolic_paraboloid(a, b, c, h, k, l, orientation, analysis_info)
            elif surface_type == 7:
                cyl_type = self.cylinder_var.get()
                self.plot_cylinder(a, b, c, p, h, k, l, cyl_type, orientation, analysis_info)
        except Exception as e:
            messagebox.showerror("Plot Error", f"Error plotting surface: {str(e)}")
            return
        
        # Set labels and title with better styling
        self.ax.set_xlabel('X', fontsize=11, fontweight='bold')
        self.ax.set_ylabel('Y', fontsize=11, fontweight='bold')
        self.ax.set_zlabel('Z', fontsize=11, fontweight='bold')
        self.ax.set_title(f"{self.surface_types[surface_type]}", 
                         fontsize=13, fontweight='bold', pad=15)
        
        # Set background color for better contrast
        self.ax.set_facecolor('#f0f0f0')
        self.fig.patch.set_facecolor('white')
        
        # Grid styling
        self.ax.grid(True, linestyle='--', alpha=0.3, linewidth=0.5)
        
        # Draw coordinate axes
        self.draw_axes(ranges)
        
        # Mark center with better visibility
        self.ax.scatter([h], [k], [l], color='red', s=150, marker='o', 
                       edgecolors='darkred', linewidths=2, label='Center', 
                       alpha=0.9, zorder=100)
        self.ax.legend(loc='upper right', fontsize=9)
        
        # Set equal aspect ratio if possible
        try:
            self.ax.set_box_aspect([1,1,1])
        except:
            pass
        
        self.canvas.draw()
    
    def plot_ellipsoid(self, a, b, c, h, k, l, analysis_info):
        res = self.quality_level
        u = np.linspace(0, 2 * np.pi, res)
        v = np.linspace(0, np.pi, res)
        
        X = a * np.outer(np.cos(u), np.sin(v)) + h
        Y = b * np.outer(np.sin(u), np.sin(v)) + k
        Z = c * np.outer(np.ones(np.size(u)), np.cos(v)) + l
        
        # Use rcount and ccount for better performance
        self.ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, 
                            rcount=res//2, ccount=res//2, 
                            linewidth=0, antialiased=True, shade=True)
        
        equation = f"Equation: (x-{h})²/{a}² + (y-{k})²/{b}² + (z-{l})²/{c}² = 1\n"
        description = "Description: Closed surface, symmetric in all coordinate directions\n"
        description += f"Intercepts: x-axis: ±{a}, y-axis: ±{b}, z-axis: ±{c}"
        
        self.analysis_text.insert(tk.END, analysis_info + equation + description)
        
        # Plot traces
        self.plot_traces_ellipsoid(a, b, c, h, k, l)
    
    def plot_elliptic_cone(self, a, b, c, h, k, l, orientation, analysis_info):
        res = self.quality_level
        u = np.linspace(0, 2 * np.pi, res)
        v = np.linspace(-2, 2, res)
        U, V = np.meshgrid(u, v)
        
        if orientation == "z-axis":
            X = a * V * np.cos(U) + h
            Y = b * V * np.sin(U) + k
            Z = c * V + l
            equation = f"Equation: (x-{h})²/{a}² + (y-{k})²/{b}² - (z-{l})²/{c}² = 0"
        elif orientation == "y-axis":
            X = a * V * np.cos(U) + h
            Z = c * V * np.sin(U) + l
            Y = b * V + k
            equation = f"Equation: (x-{h})²/{a}² + (z-{l})²/{c}² - (y-{k})²/{b}² = 0"
        else:  # x-axis
            Y = b * V * np.cos(U) + k
            Z = c * V * np.sin(U) + l
            X = a * V + h
            equation = f"Equation: (y-{k})²/{b}² + (z-{l})²/{c}² - (x-{h})²/{a}² = 0"
        
        self.ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.8, 
                            rcount=res//2, ccount=res//2,
                            linewidth=0, antialiased=True, shade=True)
        
        description = f"\nDescription: Double cone, vertex at ({h}, {k}, {l}), opens along {orientation}"
        self.analysis_text.insert(tk.END, analysis_info + equation + description)
    
    def plot_hyperboloid_one_sheet(self, a, b, c, h, k, l, orientation, analysis_info):
        res = self.quality_level
        u = np.linspace(0, 2 * np.pi, res)
        v = np.linspace(-2, 2, res)
        U, V = np.meshgrid(u, v)
        
        if orientation == "z-axis":
            X = a * np.cosh(V) * np.cos(U) + h
            Y = b * np.cosh(V) * np.sin(U) + k
            Z = c * np.sinh(V) + l
            equation = f"Equation: (x-{h})²/{a}² + (y-{k})²/{b}² - (z-{l})²/{c}² = 1"
        elif orientation == "y-axis":
            X = a * np.cosh(V) * np.cos(U) + h
            Z = c * np.cosh(V) * np.sin(U) + l
            Y = b * np.sinh(V) + k
            equation = f"Equation: (x-{h})²/{a}² + (z-{l})²/{c}² - (y-{k})²/{b}² = 1"
        else:  # x-axis
            Y = b * np.cosh(V) * np.cos(U) + k
            Z = c * np.cosh(V) * np.sin(U) + l
            X = a * np.sinh(V) + h
            equation = f"Equation: (y-{k})²/{b}² + (z-{l})²/{c}² - (x-{h})²/{a}² = 1"
        
        self.ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.8,
                            rcount=res//2, ccount=res//2,
                            linewidth=0, antialiased=True, shade=True)
        
        description = f"\nDescription: Single-sheeted hyperboloid, connected surface, opens along {orientation}"
        self.analysis_text.insert(tk.END, analysis_info + equation + description)
    
    def plot_hyperboloid_two_sheets(self, a, b, c, h, k, l, orientation, analysis_info):
        res = self.quality_level
        u = np.linspace(0, 2 * np.pi, res)
        v = np.linspace(0.1, 2, res//2)
        U, V = np.meshgrid(u, v)
        
        if orientation == "z-axis":
            X = a * np.sinh(V) * np.cos(U) + h
            Y = b * np.sinh(V) * np.sin(U) + k
            Z1 = c * np.cosh(V) + l
            Z2 = -c * np.cosh(V) + l
            equation = f"Equation: -(x-{h})²/{a}² - (y-{k})²/{b}² + (z-{l})²/{c}² = 1"
        elif orientation == "y-axis":
            X = a * np.sinh(V) * np.cos(U) + h
            Z = c * np.sinh(V) * np.sin(U) + l
            Y1 = b * np.cosh(V) + k
            Y2 = -b * np.cosh(V) + k
            equation = f"Equation: -(x-{h})²/{a}² - (z-{l})²/{c}² + (y-{k})²/{b}² = 1"
        else:  # x-axis
            Y = b * np.sinh(V) * np.cos(U) + k
            Z = c * np.sinh(V) * np.sin(U) + l
            X1 = a * np.cosh(V) + h
            X2 = -a * np.cosh(V) + h
            equation = f"Equation: -(y-{k})²/{b}² - (z-{l})²/{c}² + (x-{h})²/{a}² = 1"
        
        # Plot both sheets
        res = self.quality_level
        if orientation == "z-axis":
            self.ax.plot_surface(X, Y, Z1, cmap='autumn', alpha=0.8,
                                rcount=res//2, ccount=res//2,
                                linewidth=0, antialiased=True, shade=True)
            self.ax.plot_surface(X, Y, Z2, cmap='winter', alpha=0.8,
                                rcount=res//2, ccount=res//2,
                                linewidth=0, antialiased=True, shade=True)
        elif orientation == "y-axis":
            self.ax.plot_surface(X, Y1, Z, cmap='autumn', alpha=0.8,
                                rcount=res//2, ccount=res//2,
                                linewidth=0, antialiased=True, shade=True)
            self.ax.plot_surface(X, Y2, Z, cmap='winter', alpha=0.8,
                                rcount=res//2, ccount=res//2,
                                linewidth=0, antialiased=True, shade=True)
        else:
            self.ax.plot_surface(X1, Y, Z, cmap='autumn', alpha=0.8,
                                rcount=res//2, ccount=res//2,
                                linewidth=0, antialiased=True, shade=True)
            self.ax.plot_surface(X2, Y, Z, cmap='winter', alpha=0.8,
                                rcount=res//2, ccount=res//2,
                                linewidth=0, antialiased=True, shade=True)
        
        description = f"\nDescription: Two-sheeted hyperboloid, disconnected surface, opens along {orientation}"
        self.analysis_text.insert(tk.END, analysis_info + equation + description)
    
    def plot_elliptic_paraboloid(self, a, b, c, h, k, l, orientation, analysis_info):
        res = self.quality_level
        u = np.linspace(-2, 2, res)
        v = np.linspace(-2, 2, res)
        U, V = np.meshgrid(u, v)
        
        if orientation == "z-axis":
            X = a * U + h
            Y = b * V + k
            Z = (U**2 + V**2) + l
            equation = f"Equation: (x-{h})²/{a}² + (y-{k})²/{b}² = z-{l}"
        elif orientation == "y-axis":
            X = a * U + h
            Z = c * V + l
            Y = (U**2 + V**2) + k
            equation = f"Equation: (x-{h})²/{a}² + (z-{l})²/{c}² = y-{k}"
        else:  # x-axis
            Y = b * U + k
            Z = c * V + l
            X = (U**2 + V**2) + h
            equation = f"Equation: (y-{k})²/{b}² + (z-{l})²/{c}² = x-{h}"
        
        self.ax.plot_surface(X, Y, Z, cmap='Spectral', alpha=0.8,
                            rcount=res//2, ccount=res//2,
                            linewidth=0, antialiased=True, shade=True)
        
        description = f"\nDescription: Elliptic paraboloid, opens along {orientation}, bowl-shaped"
        self.analysis_text.insert(tk.END, analysis_info + equation + description)
    
    def plot_hyperbolic_paraboloid(self, a, b, c, h, k, l, orientation, analysis_info):
        res = self.quality_level
        u = np.linspace(-2, 2, res)
        v = np.linspace(-2, 2, res)
        U, V = np.meshgrid(u, v)
        
        if orientation == "z-axis":
            X = a * U + h
            Y = b * V + k
            Z = (V**2 - U**2) + l
            equation = f"Equation: (y-{k})²/{b}² - (x-{h})²/{a}² = z-{l}"
        elif orientation == "y-axis":
            X = a * U + h
            Z = c * V + l
            Y = (V**2 - U**2) + k
            equation = f"Equation: (z-{l})²/{c}² - (x-{h})²/{a}² = y-{k}"
        else:  # x-axis
            Y = b * U + k
            Z = c * V + l
            X = (V**2 - U**2) + h
            equation = f"Equation: (z-{l})²/{c}² - (y-{k})²/{b}² = x-{h}"
        
        self.ax.plot_surface(X, Y, Z, cmap='RdYlBu', alpha=0.8,
                            rcount=res//2, ccount=res//2,
                            linewidth=0, antialiased=True, shade=True)
        
        description = f"\nDescription: Hyperbolic paraboloid (saddle surface), opens along {orientation}"
        self.analysis_text.insert(tk.END, analysis_info + equation + description)
    
    def plot_cylinder(self, a, b, c, p, h, k, l, cyl_type, orientation, analysis_info):
        res = self.quality_level
        theta = np.linspace(0, 2 * np.pi, res)
        z = np.linspace(-5, 5, res)
        
        if cyl_type == "Elliptic":
            Theta, Z = np.meshgrid(theta, z)
            X = a * np.cos(Theta) + h
            Y = b * np.sin(Theta) + k
            Z_plot = Z + l
            equation = f"Equation: (x-{h})²/{a}² + (y-{k})²/{b}² = 1"
            description = "\nDescription: Elliptic cylinder, infinite along z-axis"
            
        elif cyl_type == "Hyperbolic":
            t = np.linspace(-2, 2, res)
            z = np.linspace(-5, 5, res)
            T, Z = np.meshgrid(t, z)
            
            X1 = a * np.cosh(T) + h
            Y1 = b * np.sinh(T) + k
            X2 = -a * np.cosh(T) + h
            Y2 = -b * np.sinh(T) + k
            Z_plot = Z + l
            
            self.ax.plot_surface(X1, Y1, Z_plot, cmap='copper', alpha=0.8,
                                rcount=res//2, ccount=res//2,
                                linewidth=0, antialiased=True, shade=True)
            self.ax.plot_surface(X2, Y2, Z_plot, cmap='copper', alpha=0.8,
                                rcount=res//2, ccount=res//2,
                                linewidth=0, antialiased=True, shade=True)
            
            equation = f"Equation: (x-{h})²/{a}² - (y-{k})²/{b}² = 1"
            description = "\nDescription: Hyperbolic cylinder, two separate sheets, infinite along z-axis"
            self.analysis_text.insert(tk.END, analysis_info + equation + description)
            return
            
        else:  # Parabolic
            y_vals = np.linspace(-3, 3, res)
            z = np.linspace(-5, 5, res)
            Y, Z = np.meshgrid(y_vals, z)
            X = (Y - k)**2 / (4 * p) + h
            Z_plot = Z + l
            equation = f"Equation: (y-{k})² = 4·{p}·(x-{h})"
            description = "\nDescription: Parabolic cylinder, infinite along z-axis"
        
        self.ax.plot_surface(X, Y, Z_plot, cmap='ocean', alpha=0.8,
                            rcount=res//2, ccount=res//2,
                            linewidth=0, antialiased=True, shade=True)
        self.analysis_text.insert(tk.END, analysis_info + equation + description)
    
    def plot_traces_ellipsoid(self, a, b, c, h, k, l):
        # XY-plane trace (z = l)
        theta = np.linspace(0, 2 * np.pi, 80)
        x_trace = a * np.cos(theta) + h
        y_trace = b * np.sin(theta) + k
        z_trace = np.full_like(x_trace, l)
        self.ax.plot(x_trace, y_trace, z_trace, 'r-', linewidth=2.5, label='XY-plane trace', alpha=0.9)
        
        # XZ-plane trace (y = k)
        x_trace = a * np.cos(theta) + h
        y_trace = np.full_like(x_trace, k)
        z_trace = c * np.sin(theta) + l
        self.ax.plot(x_trace, y_trace, z_trace, 'b-', linewidth=2.5, label='XZ-plane trace', alpha=0.9)
        
        # YZ-plane trace (x = h)
        x_trace = np.full_like(theta, h)
        y_trace = b * np.cos(theta) + k
        z_trace = c * np.sin(theta) + l
        self.ax.plot(x_trace, y_trace, z_trace, 'g-', linewidth=2.5, label='YZ-plane trace', alpha=0.9)
    
    def draw_axes(self, ranges):
        # Draw coordinate axes
        axis_length = max(abs(ranges['xmax']), abs(ranges['xmin']),
                         abs(ranges['ymax']), abs(ranges['ymin']),
                         abs(ranges['zmax']), abs(ranges['zmin']))
        
        self.ax.plot([0, axis_length], [0, 0], [0, 0], 'k--', alpha=0.3, linewidth=0.5)
        self.ax.plot([0, -axis_length], [0, 0], [0, 0], 'k--', alpha=0.3, linewidth=0.5)
        self.ax.plot([0, 0], [0, axis_length], [0, 0], 'k--', alpha=0.3, linewidth=0.5)
        self.ax.plot([0, 0], [0, -axis_length], [0, 0], 'k--', alpha=0.3, linewidth=0.5)
        self.ax.plot([0, 0], [0, 0], [0, axis_length], 'k--', alpha=0.3, linewidth=0.5)
        self.ax.plot([0, 0], [0, 0], [0, -axis_length], 'k--', alpha=0.3, linewidth=0.5)


def main():
    root = tk.Tk()
    app = QuadricSurfaceVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
