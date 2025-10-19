"""
Plot Panel Module
Handles 3D visualization and analysis display for quadric surfaces.
"""

import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from models.quadric_surfaces import QuadricSurface, SurfaceType, SurfaceParameters
from utils.analysis import AnalysisGenerator


class PlotPanel(ctk.CTkFrame):
    """Right panel containing 3D plot and analysis results"""
    
    def __init__(self, master):
        super().__init__(master)
        
        # Configure grid
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create plot frame
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Matplotlib Figure
        self.fig = Figure(figsize=(10, 8), dpi=100, facecolor='#2b2b2b')
        self.ax = self.fig.add_subplot(111, projection='3d', facecolor='#2b2b2b')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Analysis Results Panel
        analysis_frame = ctk.CTkFrame(self)
        analysis_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        analysis_title = ctk.CTkLabel(
            analysis_frame,
            text="Analysis Results",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        analysis_title.pack(pady=(10, 5), padx=10, anchor="w")
        
        self.analysis_text = ctk.CTkTextbox(
            analysis_frame,
            wrap="word",
            font=ctk.CTkFont(family="Consolas", size=11),
            height=200
        )
        self.analysis_text.pack(pady=(0, 10), padx=10, fill="both", expand=True)
    
    def clear_plot(self):
        """Clear the plot and analysis text"""
        self.ax.clear()
        self.canvas.draw()
        self.analysis_text.delete("1.0", "end")
    
    def plot_surface(self, surface_type: SurfaceType, params: SurfaceParameters,
                    orientation: str, range_min: float, range_max: float):
        """Main plotting function"""
        try:
            # Clear previous plot
            self.ax.clear()
            
            # Set up the plot
            self.ax.set_xlabel('X', fontsize=12, color='white')
            self.ax.set_ylabel('Y', fontsize=12, color='white')
            self.ax.set_zlabel('Z', fontsize=12, color='white')
            self.ax.tick_params(colors='white')
            
            # Create surface
            surface = QuadricSurface(surface_type, params, orientation)
            X, Y, Z = surface.generate_surface(range_min, range_max)
            
            # Plot surface
            self._plot_surface_data(X, Y, Z, surface_type)
            
            # Set title
            title = self._get_surface_title(surface_type, orientation, params)
            self.ax.set_title(title, fontsize=14, color='white', pad=20)
            
            # Plot center point
            self.ax.scatter([params.h], [params.k], [params.l], 
                          color='red', s=100, marker='o',
                          label=f'Center ({params.h:.1f}, {params.k:.1f}, {params.l:.1f})')
            
            # Plot traces
            self._plot_traces(params, surface_type, orientation, range_min, range_max)
            
            # Set equal aspect ratio
            max_range = max(abs(range_min), abs(range_max))
            self.ax.set_xlim([params.h - max_range, params.h + max_range])
            self.ax.set_ylim([params.k - max_range, params.k + max_range])
            self.ax.set_zlim([params.l - max_range, params.l + max_range])
            
            # Add legend
            self.ax.legend(loc='upper right', fontsize=9, facecolor='#2b2b2b',
                         edgecolor='white', labelcolor='white')
            
            # Update canvas
            self.canvas.draw()
            
            # Update analysis panel
            self._update_analysis(surface_type, orientation, params)
            
        except Exception as e:
            self._show_error(f"Error plotting surface: {str(e)}")
    
    def _plot_surface_data(self, X, Y, Z, surface_type: SurfaceType):
        """Plot the surface data with appropriate colormap"""
        # Choose colormap
        if surface_type == SurfaceType.HYPERBOLOID_TWO_SHEETS:
            cmap = 'plasma'
        elif surface_type == SurfaceType.ELLIPTIC_PARABOLOID:
            cmap = 'coolwarm'
        elif surface_type == SurfaceType.HYPERBOLIC_PARABOLOID:
            cmap = 'RdYlBu'
        else:
            cmap = 'viridis'
        
        # Handle surfaces with two sheets
        if isinstance(Z, tuple):
            Z_pos, Z_neg = Z
            mask = np.isfinite(Z_pos)
            self.ax.plot_surface(X, Y, Z_pos, where=mask, cmap=cmap, alpha=0.7, edgecolor='none')
            self.ax.plot_surface(X, Y, Z_neg, where=mask, cmap=cmap, alpha=0.7, edgecolor='none')
        elif isinstance(Y, tuple):
            Y_pos, Y_neg = Y
            mask = np.isfinite(Y_pos)
            self.ax.plot_surface(X, Y_pos, Z, where=mask, cmap=cmap, alpha=0.7, edgecolor='none')
            self.ax.plot_surface(X, Y_neg, Z, where=mask, cmap=cmap, alpha=0.7, edgecolor='none')
        elif isinstance(X, tuple):
            X_pos, X_neg = X
            mask = np.isfinite(X_pos)
            self.ax.plot_surface(X_pos, Y, Z, where=mask, cmap=cmap, alpha=0.7, edgecolor='none')
            self.ax.plot_surface(X_neg, Y, Z, where=mask, cmap=cmap, alpha=0.7, edgecolor='none')
        else:
            self.ax.plot_surface(X, Y, Z, cmap=cmap, alpha=0.7, edgecolor='none')
    
    def _get_surface_title(self, surface_type: SurfaceType, orientation: str, 
                          params: SurfaceParameters) -> str:
        """Generate title for the plot"""
        if surface_type == SurfaceType.ELLIPSOID:
            return f'Ellipsoid (a={params.a:.2f}, b={params.b:.2f}, c={params.c:.2f})'
        elif surface_type == SurfaceType.CYLINDER:
            return f'Elliptic Cylinder (Extends along {orientation})'
        elif surface_type == SurfaceType.HYPERBOLIC_PARABOLOID:
            return f'Hyperbolic Paraboloid - Saddle (Principal axis: {orientation})'
        elif surface_type == SurfaceType.ELLIPTIC_PARABOLOID:
            return f'Elliptic Paraboloid (Opens along {orientation})'
        else:
            return f'{surface_type.value} (Axis: {orientation})'
    
    def _plot_traces(self, params: SurfaceParameters, surface_type: SurfaceType,
                    orientation: str, range_min: float, range_max: float):
        """Plot cross-section traces on coordinate planes"""
        try:
            if surface_type == SurfaceType.ELLIPSOID:
                # XY plane trace (z = l)
                theta = np.linspace(0, 2*np.pi, 100)
                x_xy = params.a * np.cos(theta) + params.h
                y_xy = params.b * np.sin(theta) + params.k
                z_xy = np.full_like(x_xy, params.l)
                self.ax.plot3D(x_xy, y_xy, z_xy, 'r-', linewidth=2, label='XY trace (z=l)')
                
                # XZ plane trace (y = k)
                x_xz = params.a * np.cos(theta) + params.h
                z_xz = params.c * np.sin(theta) + params.l
                y_xz = np.full_like(x_xz, params.k)
                self.ax.plot3D(x_xz, y_xz, z_xz, 'b-', linewidth=2, label='XZ trace (y=k)')
                
                # YZ plane trace (x = h)
                y_yz = params.b * np.cos(theta) + params.k
                z_yz = params.c * np.sin(theta) + params.l
                x_yz = np.full_like(y_yz, params.h)
                self.ax.plot3D(x_yz, y_yz, z_yz, 'g-', linewidth=2, label='YZ trace (x=h)')
        except Exception:
            pass  # Skip traces if they can't be computed
    
    def _update_analysis(self, surface_type: SurfaceType, orientation: str, 
                        params: SurfaceParameters):
        """Update the analysis results panel"""
        self.analysis_text.delete("1.0", "end")
        
        # Generate comprehensive analysis
        full_analysis = AnalysisGenerator.generate_full_analysis(
            surface_type, orientation, params
        )
        
        self.analysis_text.insert("1.0", full_analysis)
    
    def _show_error(self, message: str):
        """Display error message"""
        error_window = ctk.CTkToplevel(self)
        error_window.title("Plot Error")
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
