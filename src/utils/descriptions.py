"""
Description Generation Utilities
Provides qualitative descriptions for different quadric surfaces.
"""

from models.quadric_surfaces import SurfaceType


class DescriptionGenerator:
    """Generates qualitative descriptions for quadric surfaces"""
    
    @staticmethod
    def generate(surface_type: SurfaceType, axis: str) -> str:
        """Get qualitative description of the surface"""
        
        descriptions = {
            SurfaceType.ELLIPSOID: 
                "Qualitative Description:\n"
                "- Closed, bounded surface\n"
                "- Symmetrical about all three axes\n"
                "- All cross-sections are ellipses\n"
                "- No ruled lines",
            
            SurfaceType.ELLIPTIC_CONE: 
                f"Qualitative Description:\n"
                f"- Unbounded surface extending to infinity\n"
                f"- Opens along {axis}-axis\n"
                f"- Vertex at the center point\n"
                f"- Cross-sections perpendicular to {axis} are ellipses\n"
                f"- Ruled surface (contains straight lines)",
            
            SurfaceType.HYPERBOLOID_ONE_SHEET: 
                f"Qualitative Description:\n"
                f"- Unbounded, single-sheeted surface\n"
                f"- Opens along {axis}-axis (waist perpendicular to {axis})\n"
                f"- Cross-sections perpendicular to {axis} are ellipses\n"
                f"- Cross-sections parallel to {axis} are hyperbolas\n"
                f"- Ruled surface (doubly ruled)",
            
            SurfaceType.HYPERBOLOID_TWO_SHEETS: 
                f"Qualitative Description:\n"
                f"- Two separate sheets (disconnected)\n"
                f"- Sheets open along {axis}-axis\n"
                f"- Gap between sheets at center\n"
                f"- All cross-sections perpendicular to {axis} are ellipses\n"
                f"- Cross-sections parallel to {axis} are hyperbolas\n"
                f"- Not a ruled surface",
            
            SurfaceType.ELLIPTIC_PARABOLOID: 
                f"Qualitative Description:\n"
                f"- Unbounded, bowl-shaped surface\n"
                f"- Opens along {axis}-axis\n"
                f"- Vertex at the center point\n"
                f"- All cross-sections perpendicular to {axis} are ellipses\n"
                f"- All cross-sections parallel to {axis} are parabolas\n"
                f"- Not a ruled surface",
            
            SurfaceType.HYPERBOLIC_PARABOLOID: 
                f"Qualitative Description:\n"
                f"- Saddle-shaped surface (unbounded)\n"
                f"- Principal axis along {axis}-axis\n"
                f"- Cross-sections are hyperbolas and parabolas\n"
                f"- Contains saddle point at center\n"
                f"- Ruled surface (doubly ruled)\n"
                f"- Used in architecture (hyperbolic paraboloid shells)",
            
            SurfaceType.CYLINDER: 
                f"Qualitative Description:\n"
                f"- Unbounded surface extending infinitely along {axis}-axis\n"
                f"- Cross-sections perpendicular to {axis} are ellipses\n"
                f"- Cross-sections parallel to {axis} are parallel lines\n"
                f"- Ruled surface (contains infinite parallel lines)\n"
                f"- Constant cross-section along {axis}"
        }
        
        return descriptions.get(surface_type, "Description: N/A")
