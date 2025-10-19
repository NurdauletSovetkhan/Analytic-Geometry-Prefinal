"""
Equation Generation Utilities
Generates mathematical equations for different quadric surfaces.
"""

from models.quadric_surfaces import SurfaceType


class EquationGenerator:
    """Generates canonical equations for quadric surfaces"""
    
    @staticmethod
    def generate(surface_type: SurfaceType, axis: str, a: float, b: float, 
                 c: float, h: float, k: float, l: float) -> str:
        """Generate the canonical equation with substituted parameters"""
        
        if surface_type == SurfaceType.ELLIPSOID:
            return f"Equation: (x-{h:.2f})²/{a:.2f}² + (y-{k:.2f})²/{b:.2f}² + (z-{l:.2f})²/{c:.2f}² = 1"
        
        elif surface_type == SurfaceType.ELLIPTIC_CONE:
            if axis == 'Z':
                return f"Equation: (x-{h:.2f})²/{a:.2f}² + (y-{k:.2f})²/{b:.2f}² = (z-{l:.2f})²/{c:.2f}²"
            elif axis == 'Y':
                return f"Equation: (x-{h:.2f})²/{a:.2f}² + (z-{l:.2f})²/{c:.2f}² = (y-{k:.2f})²/{b:.2f}²"
            else:
                return f"Equation: (y-{k:.2f})²/{b:.2f}² + (z-{l:.2f})²/{c:.2f}² = (x-{h:.2f})²/{a:.2f}²"
        
        elif surface_type == SurfaceType.HYPERBOLOID_ONE_SHEET:
            if axis == 'Z':
                return f"Equation: (x-{h:.2f})²/{a:.2f}² + (y-{k:.2f})²/{b:.2f}² - (z-{l:.2f})²/{c:.2f}² = 1"
            elif axis == 'Y':
                return f"Equation: (x-{h:.2f})²/{a:.2f}² + (z-{l:.2f})²/{c:.2f}² - (y-{k:.2f})²/{b:.2f}² = 1"
            else:
                return f"Equation: (y-{k:.2f})²/{b:.2f}² + (z-{l:.2f})²/{c:.2f}² - (x-{h:.2f})²/{a:.2f}² = 1"
        
        elif surface_type == SurfaceType.HYPERBOLOID_TWO_SHEETS:
            if axis == 'Z':
                return f"Equation: (z-{l:.2f})²/{c:.2f}² - (x-{h:.2f})²/{a:.2f}² - (y-{k:.2f})²/{b:.2f}² = 1"
            elif axis == 'Y':
                return f"Equation: (y-{k:.2f})²/{b:.2f}² - (x-{h:.2f})²/{a:.2f}² - (z-{l:.2f})²/{c:.2f}² = 1"
            else:
                return f"Equation: (x-{h:.2f})²/{a:.2f}² - (y-{k:.2f})²/{b:.2f}² - (z-{l:.2f})²/{c:.2f}² = 1"
        
        elif surface_type == SurfaceType.ELLIPTIC_PARABOLOID:
            if axis == 'Z':
                return f"Equation: z = (x-{h:.2f})²/{a:.2f}² + (y-{k:.2f})²/{b:.2f}² + {l:.2f}"
            elif axis == 'Y':
                return f"Equation: y = (x-{h:.2f})²/{a:.2f}² + (z-{l:.2f})²/{c:.2f}² + {k:.2f}"
            else:
                return f"Equation: x = (y-{k:.2f})²/{b:.2f}² + (z-{l:.2f})²/{c:.2f}² + {h:.2f}"
        
        elif surface_type == SurfaceType.HYPERBOLIC_PARABOLOID:
            if axis == 'Z':
                return f"Equation: z = (y-{k:.2f})²/{b:.2f}² - (x-{h:.2f})²/{a:.2f}² + {l:.2f}"
            elif axis == 'Y':
                return f"Equation: y = (z-{l:.2f})²/{c:.2f}² - (x-{h:.2f})²/{a:.2f}² + {k:.2f}"
            else:
                return f"Equation: x = (y-{k:.2f})²/{b:.2f}² - (z-{l:.2f})²/{c:.2f}² + {h:.2f}"
        
        elif surface_type == SurfaceType.CYLINDER:
            if axis == 'Z':
                return f"Equation: (x-{h:.2f})²/{a:.2f}² + (y-{k:.2f})²/{b:.2f}² = 1"
            elif axis == 'Y':
                return f"Equation: (x-{h:.2f})²/{a:.2f}² + (z-{l:.2f})²/{c:.2f}² = 1"
            else:
                return f"Equation: (y-{k:.2f})²/{b:.2f}² + (z-{l:.2f})²/{c:.2f}² = 1"
        
        return "Equation: N/A"
