"""
Analysis Generator Module
Generates detailed mathematical analysis including computation steps.
"""

from models.quadric_surfaces import SurfaceType, SurfaceParameters


class AnalysisGenerator:
    """Generates comprehensive analysis with computation details"""
    
    @staticmethod
    def generate_full_analysis(surface_type: SurfaceType, orientation: str, 
                               params: SurfaceParameters) -> str:
        """Generate complete analysis including computation steps"""
        
        analysis_parts = []
        
        # 1. Surface type and configuration
        analysis_parts.append("═" * 60)
        analysis_parts.append("QUADRIC SURFACE ANALYSIS")
        analysis_parts.append("═" * 60)
        analysis_parts.append("")
        
        # 2. Surface identification
        analysis_parts.append("1. SURFACE IDENTIFICATION")
        analysis_parts.append("─" * 60)
        if surface_type == SurfaceType.ELLIPSOID:
            analysis_parts.append(f"Type: {surface_type.value}")
            analysis_parts.append("Configuration: Symmetric about all three axes")
        elif surface_type == SurfaceType.CYLINDER:
            analysis_parts.append(f"Type: {surface_type.value}")
            analysis_parts.append(f"Configuration: Extends infinitely along {orientation}-axis")
        else:
            analysis_parts.append(f"Type: {surface_type.value}")
            analysis_parts.append(f"Configuration: Axis of symmetry along {orientation}-axis")
        analysis_parts.append("")
        
        # 3. Given parameters
        analysis_parts.append("2. GIVEN PARAMETERS")
        analysis_parts.append("─" * 60)
        analysis_parts.append(f"Semi-axes: a = {params.a:.3f}, b = {params.b:.3f}, c = {params.c:.3f}")
        analysis_parts.append(f"Center: C({params.h:.3f}, {params.k:.3f}, {params.l:.3f})")
        analysis_parts.append("")
        
        # 4. Canonical equation
        analysis_parts.append("3. CANONICAL EQUATION")
        analysis_parts.append("─" * 60)
        canonical_eq = AnalysisGenerator._get_canonical_equation(surface_type, orientation)
        analysis_parts.append(f"Standard form: {canonical_eq}")
        analysis_parts.append("")
        
        # 5. Substituted equation
        analysis_parts.append("4. EQUATION WITH SUBSTITUTED VALUES")
        analysis_parts.append("─" * 60)
        substituted_eq = AnalysisGenerator._get_substituted_equation(
            surface_type, orientation, params
        )
        analysis_parts.append(substituted_eq)
        analysis_parts.append("")
        
        # 6. Computation method
        analysis_parts.append("5. COMPUTATION METHOD")
        analysis_parts.append("─" * 60)
        computation_method = AnalysisGenerator._get_computation_method(
            surface_type, orientation, params
        )
        analysis_parts.extend(computation_method)
        analysis_parts.append("")
        
        # 7. Key properties
        analysis_parts.append("6. KEY PROPERTIES")
        analysis_parts.append("─" * 60)
        properties = AnalysisGenerator._get_properties(surface_type, orientation, params)
        analysis_parts.extend(properties)
        analysis_parts.append("")
        
        # 8. Cross-sections
        analysis_parts.append("7. CROSS-SECTIONS")
        analysis_parts.append("─" * 60)
        cross_sections = AnalysisGenerator._get_cross_sections(surface_type, orientation)
        analysis_parts.extend(cross_sections)
        
        return "\n".join(analysis_parts)
    
    @staticmethod
    def _get_canonical_equation(surface_type: SurfaceType, orientation: str) -> str:
        """Get canonical form of the equation"""
        if surface_type == SurfaceType.ELLIPSOID:
            return "(x-h)²/a² + (y-k)²/b² + (z-l)²/c² = 1"
        
        elif surface_type == SurfaceType.ELLIPTIC_CONE:
            if orientation == 'Z':
                return "(x-h)²/a² + (y-k)²/b² = (z-l)²/c²"
            elif orientation == 'Y':
                return "(x-h)²/a² + (z-l)²/c² = (y-k)²/b²"
            else:
                return "(y-k)²/b² + (z-l)²/c² = (x-h)²/a²"
        
        elif surface_type == SurfaceType.HYPERBOLOID_ONE_SHEET:
            if orientation == 'Z':
                return "(x-h)²/a² + (y-k)²/b² - (z-l)²/c² = 1"
            elif orientation == 'Y':
                return "(x-h)²/a² + (z-l)²/c² - (y-k)²/b² = 1"
            else:
                return "(y-k)²/b² + (z-l)²/c² - (x-h)²/a² = 1"
        
        elif surface_type == SurfaceType.HYPERBOLOID_TWO_SHEETS:
            if orientation == 'Z':
                return "(z-l)²/c² - (x-h)²/a² - (y-k)²/b² = 1"
            elif orientation == 'Y':
                return "(y-k)²/b² - (x-h)²/a² - (z-l)²/c² = 1"
            else:
                return "(x-h)²/a² - (y-k)²/b² - (z-l)²/c² = 1"
        
        elif surface_type == SurfaceType.ELLIPTIC_PARABOLOID:
            if orientation == 'Z':
                return "z - l = c[(x-h)²/a² + (y-k)²/b²]"
            elif orientation == 'Y':
                return "y - k = b[(x-h)²/a² + (z-l)²/c²]"
            else:
                return "x - h = a[(y-k)²/b² + (z-l)²/c²]"
        
        elif surface_type == SurfaceType.HYPERBOLIC_PARABOLOID:
            if orientation == 'Z':
                return "z - l = c[(y-k)²/b² - (x-h)²/a²]"
            elif orientation == 'Y':
                return "y - k = b[(z-l)²/c² - (x-h)²/a²]"
            else:
                return "x - h = a[(y-k)²/b² - (z-l)²/c²]"
        
        elif surface_type == SurfaceType.CYLINDER:
            if orientation == 'Z':
                return "(x-h)²/a² + (y-k)²/b² = 1, z extends infinitely"
            elif orientation == 'Y':
                return "(x-h)²/a² + (z-l)²/c² = 1, y extends infinitely"
            else:
                return "(y-k)²/b² + (z-l)²/c² = 1, x extends infinitely"
        
        return "N/A"
    
    @staticmethod
    def _get_substituted_equation(surface_type: SurfaceType, orientation: str,
                                  params: SurfaceParameters) -> str:
        """Get equation with values substituted"""
        a, b, c = params.a, params.b, params.c
        h, k, l = params.h, params.k, params.l
        
        if surface_type == SurfaceType.ELLIPSOID:
            return f"(x-{h:.2f})²/{a:.2f}² + (y-{k:.2f})²/{b:.2f}² + (z-{l:.2f})²/{c:.2f}² = 1"
        
        elif surface_type == SurfaceType.ELLIPTIC_CONE:
            if orientation == 'Z':
                return f"(x-{h:.2f})²/{a:.2f}² + (y-{k:.2f})²/{b:.2f}² = (z-{l:.2f})²/{c:.2f}²"
            elif orientation == 'Y':
                return f"(x-{h:.2f})²/{a:.2f}² + (z-{l:.2f})²/{c:.2f}² = (y-{k:.2f})²/{b:.2f}²"
            else:
                return f"(y-{k:.2f})²/{b:.2f}² + (z-{l:.2f})²/{c:.2f}² = (x-{h:.2f})²/{a:.2f}²"
        
        elif surface_type == SurfaceType.HYPERBOLOID_ONE_SHEET:
            if orientation == 'Z':
                return f"(x-{h:.2f})²/{a:.2f}² + (y-{k:.2f})²/{b:.2f}² - (z-{l:.2f})²/{c:.2f}² = 1"
            elif orientation == 'Y':
                return f"(x-{h:.2f})²/{a:.2f}² + (z-{l:.2f})²/{c:.2f}² - (y-{k:.2f})²/{b:.2f}² = 1"
            else:
                return f"(y-{k:.2f})²/{b:.2f}² + (z-{l:.2f})²/{c:.2f}² - (x-{h:.2f})²/{a:.2f}² = 1"
        
        elif surface_type == SurfaceType.HYPERBOLOID_TWO_SHEETS:
            if orientation == 'Z':
                return f"(z-{l:.2f})²/{c:.2f}² - (x-{h:.2f})²/{a:.2f}² - (y-{k:.2f})²/{b:.2f}² = 1"
            elif orientation == 'Y':
                return f"(y-{k:.2f})²/{b:.2f}² - (x-{h:.2f})²/{a:.2f}² - (z-{l:.2f})²/{c:.2f}² = 1"
            else:
                return f"(x-{h:.2f})²/{a:.2f}² - (y-{k:.2f})²/{b:.2f}² - (z-{l:.2f})²/{c:.2f}² = 1"
        
        elif surface_type == SurfaceType.ELLIPTIC_PARABOLOID:
            if orientation == 'Z':
                return f"z = {c:.2f}[(x-{h:.2f})²/{a:.2f}² + (y-{k:.2f})²/{b:.2f}²] + {l:.2f}"
            elif orientation == 'Y':
                return f"y = {b:.2f}[(x-{h:.2f})²/{a:.2f}² + (z-{l:.2f})²/{c:.2f}²] + {k:.2f}"
            else:
                return f"x = {a:.2f}[(y-{k:.2f})²/{b:.2f}² + (z-{l:.2f})²/{c:.2f}²] + {h:.2f}"
        
        elif surface_type == SurfaceType.HYPERBOLIC_PARABOLOID:
            if orientation == 'Z':
                return f"z = {c:.2f}[(y-{k:.2f})²/{b:.2f}² - (x-{h:.2f})²/{a:.2f}²] + {l:.2f}"
            elif orientation == 'Y':
                return f"y = {b:.2f}[(z-{l:.2f})²/{c:.2f}² - (x-{h:.2f})²/{a:.2f}²] + {k:.2f}"
            else:
                return f"x = {a:.2f}[(y-{k:.2f})²/{b:.2f}² - (z-{l:.2f})²/{c:.2f}²] + {h:.2f}"
        
        elif surface_type == SurfaceType.CYLINDER:
            if orientation == 'Z':
                return f"(x-{h:.2f})²/{a:.2f}² + (y-{k:.2f})²/{b:.2f}² = 1"
            elif orientation == 'Y':
                return f"(x-{h:.2f})²/{a:.2f}² + (z-{l:.2f})²/{c:.2f}² = 1"
            else:
                return f"(y-{k:.2f})²/{b:.2f}² + (z-{l:.2f})²/{c:.2f}² = 1"
        
        return "N/A"
    
    @staticmethod
    def _get_computation_method(surface_type: SurfaceType, orientation: str,
                               params: SurfaceParameters) -> list:
        """Describe how the surface is computed"""
        steps = []
        
        if surface_type == SurfaceType.ELLIPSOID:
            steps.append("Method: Parametric representation using spherical coordinates")
            steps.append("Steps:")
            steps.append("  1. Set φ ∈ [0, 2π] (azimuthal angle)")
            steps.append("  2. Set θ ∈ [0, π] (polar angle)")
            steps.append(f"  3. Compute: x = {params.a:.3f}·sin(θ)·cos(φ) + {params.h:.3f}")
            steps.append(f"  4. Compute: y = {params.b:.3f}·sin(θ)·sin(φ) + {params.k:.3f}")
            steps.append(f"  5. Compute: z = {params.c:.3f}·cos(θ) + {params.l:.3f}")
            steps.append("  6. Plot surface using meshgrid(φ, θ)")
        
        elif surface_type == SurfaceType.ELLIPTIC_CONE:
            if orientation == 'Z':
                steps.append("Method: Solve for z from the cone equation")
                steps.append("Steps:")
                steps.append("  1. Create meshgrid for x and y")
                steps.append(f"  2. Calculate: r² = (x-{params.h:.3f})²/{params.a:.3f}² + (y-{params.k:.3f})²/{params.b:.3f}²")
                steps.append(f"  3. Compute: z₊ = {params.c:.3f}·√(r²) + {params.l:.3f}")
                steps.append(f"  4. Compute: z₋ = -{params.c:.3f}·√(r²) + {params.l:.3f}")
                steps.append("  5. Plot both sheets (positive and negative)")
            elif orientation == 'Y':
                steps.append("Method: Solve for y from the cone equation")
                steps.append("Steps:")
                steps.append("  1. Create meshgrid for x and z")
                steps.append(f"  2. Calculate: r² = (x-{params.h:.3f})²/{params.a:.3f}² + (z-{params.l:.3f})²/{params.c:.3f}²")
                steps.append(f"  3. Compute: y₊ = {params.b:.3f}·√(r²) + {params.k:.3f}")
                steps.append(f"  4. Compute: y₋ = -{params.b:.3f}·√(r²) + {params.k:.3f}")
                steps.append("  5. Plot both sheets")
            else:
                steps.append("Method: Solve for x from the cone equation")
                steps.append("Steps:")
                steps.append("  1. Create meshgrid for y and z")
                steps.append(f"  2. Calculate: r² = (y-{params.k:.3f})²/{params.b:.3f}² + (z-{params.l:.3f})²/{params.c:.3f}²")
                steps.append(f"  3. Compute: x₊ = {params.a:.3f}·√(r²) + {params.h:.3f}")
                steps.append(f"  4. Compute: x₋ = -{params.a:.3f}·√(r²) + {params.h:.3f}")
                steps.append("  5. Plot both sheets")
        
        elif surface_type == SurfaceType.HYPERBOLOID_ONE_SHEET:
            if orientation == 'Z':
                steps.append("Method: Solve for z from hyperboloid equation")
                steps.append("Steps:")
                steps.append("  1. Create meshgrid for x and y")
                steps.append(f"  2. Calculate: r² = (x-{params.h:.3f})²/{params.a:.3f}² + (y-{params.k:.3f})²/{params.b:.3f}² - 1")
                steps.append(f"  3. Compute: z₊ = {params.c:.3f}·√(r²) + {params.l:.3f}  (valid when r² ≥ 0)")
                steps.append(f"  4. Compute: z₋ = -{params.c:.3f}·√(r²) + {params.l:.3f}")
                steps.append("  5. Plot both sheets (connected surface)")
            elif orientation == 'Y':
                steps.append("Method: Solve for y from hyperboloid equation")
                steps.append("Steps:")
                steps.append("  1. Create meshgrid for x and z")
                steps.append(f"  2. Calculate: r² = (x-{params.h:.3f})²/{params.a:.3f}² + (z-{params.l:.3f})²/{params.c:.3f}² - 1")
                steps.append(f"  3. Compute: y₊ = {params.b:.3f}·√(r²) + {params.k:.3f}")
                steps.append(f"  4. Compute: y₋ = -{params.b:.3f}·√(r²) + {params.k:.3f}")
                steps.append("  5. Plot both sheets")
            else:
                steps.append("Method: Solve for x from hyperboloid equation")
                steps.append("Steps:")
                steps.append("  1. Create meshgrid for y and z")
                steps.append(f"  2. Calculate: r² = (y-{params.k:.3f})²/{params.b:.3f}² + (z-{params.l:.3f})²/{params.c:.3f}² - 1")
                steps.append(f"  3. Compute: x₊ = {params.a:.3f}·√(r²) + {params.h:.3f}")
                steps.append(f"  4. Compute: x₋ = -{params.a:.3f}·√(r²) + {params.h:.3f}")
                steps.append("  5. Plot both sheets")
        
        elif surface_type == SurfaceType.HYPERBOLOID_TWO_SHEETS:
            if orientation == 'Z':
                steps.append("Method: Solve for z from two-sheet hyperboloid")
                steps.append("Steps:")
                steps.append("  1. Create meshgrid for x and y")
                steps.append(f"  2. Calculate: r² = 1 + (x-{params.h:.3f})²/{params.a:.3f}² + (y-{params.k:.3f})²/{params.b:.3f}²")
                steps.append(f"  3. Compute: z₊ = {params.c:.3f}·√(r²) + {params.l:.3f}  (upper sheet)")
                steps.append(f"  4. Compute: z₋ = -{params.c:.3f}·√(r²) + {params.l:.3f}  (lower sheet)")
                steps.append("  5. Plot both disconnected sheets")
            elif orientation == 'Y':
                steps.append("Method: Solve for y from two-sheet hyperboloid")
                steps.append("Steps:")
                steps.append("  1. Create meshgrid for x and z")
                steps.append(f"  2. Calculate: r² = 1 + (x-{params.h:.3f})²/{params.a:.3f}² + (z-{params.l:.3f})²/{params.c:.3f}²")
                steps.append(f"  3. Compute: y₊ = {params.b:.3f}·√(r²) + {params.k:.3f}")
                steps.append(f"  4. Compute: y₋ = -{params.b:.3f}·√(r²) + {params.k:.3f}")
                steps.append("  5. Plot both sheets")
            else:
                steps.append("Method: Solve for x from two-sheet hyperboloid")
                steps.append("Steps:")
                steps.append("  1. Create meshgrid for y and z")
                steps.append(f"  2. Calculate: r² = 1 + (y-{params.k:.3f})²/{params.b:.3f}² + (z-{params.l:.3f})²/{params.c:.3f}²")
                steps.append(f"  3. Compute: x₊ = {params.a:.3f}·√(r²) + {params.h:.3f}")
                steps.append(f"  4. Compute: x₋ = -{params.a:.3f}·√(r²) + {params.h:.3f}")
                steps.append("  5. Plot both sheets")
        
        elif surface_type == SurfaceType.ELLIPTIC_PARABOLOID:
            if orientation == 'Z':
                steps.append("Method: Direct computation from paraboloid equation")
                steps.append("Steps:")
                steps.append("  1. Create meshgrid for x and y")
                steps.append(f"  2. Calculate: u = (x-{params.h:.3f})²/{params.a:.3f}²")
                steps.append(f"  3. Calculate: v = (y-{params.k:.3f})²/{params.b:.3f}²")
                steps.append(f"  4. Compute: z = {params.c:.3f}·(u + v) + {params.l:.3f}")
                steps.append("  5. Plot surface (opens upward/downward along z)")
            elif orientation == 'Y':
                steps.append("Method: Direct computation from paraboloid equation")
                steps.append("Steps:")
                steps.append("  1. Create meshgrid for x and z")
                steps.append(f"  2. Calculate: u = (x-{params.h:.3f})²/{params.a:.3f}²")
                steps.append(f"  3. Calculate: v = (z-{params.l:.3f})²/{params.c:.3f}²")
                steps.append(f"  4. Compute: y = {params.b:.3f}·(u + v) + {params.k:.3f}")
                steps.append("  5. Plot surface")
            else:
                steps.append("Method: Direct computation from paraboloid equation")
                steps.append("Steps:")
                steps.append("  1. Create meshgrid for y and z")
                steps.append(f"  2. Calculate: u = (y-{params.k:.3f})²/{params.b:.3f}²")
                steps.append(f"  3. Calculate: v = (z-{params.l:.3f})²/{params.c:.3f}²")
                steps.append(f"  4. Compute: x = {params.a:.3f}·(u + v) + {params.h:.3f}")
                steps.append("  5. Plot surface")
        
        elif surface_type == SurfaceType.HYPERBOLIC_PARABOLOID:
            if orientation == 'Z':
                steps.append("Method: Direct computation (saddle surface)")
                steps.append("Steps:")
                steps.append("  1. Create meshgrid for x and y")
                steps.append(f"  2. Calculate: u = (y-{params.k:.3f})²/{params.b:.3f}²")
                steps.append(f"  3. Calculate: v = (x-{params.h:.3f})²/{params.a:.3f}²")
                steps.append(f"  4. Compute: z = {params.c:.3f}·(u - v) + {params.l:.3f}")
                steps.append("  5. Plot saddle-shaped surface")
            elif orientation == 'Y':
                steps.append("Method: Direct computation (saddle surface)")
                steps.append("Steps:")
                steps.append("  1. Create meshgrid for x and z")
                steps.append(f"  2. Calculate: u = (z-{params.l:.3f})²/{params.c:.3f}²")
                steps.append(f"  3. Calculate: v = (x-{params.h:.3f})²/{params.a:.3f}²")
                steps.append(f"  4. Compute: y = {params.b:.3f}·(u - v) + {params.k:.3f}")
                steps.append("  5. Plot surface")
            else:
                steps.append("Method: Direct computation (saddle surface)")
                steps.append("Steps:")
                steps.append("  1. Create meshgrid for y and z")
                steps.append(f"  2. Calculate: u = (y-{params.k:.3f})²/{params.b:.3f}²")
                steps.append(f"  3. Calculate: v = (z-{params.l:.3f})²/{params.c:.3f}²")
                steps.append(f"  4. Compute: x = {params.a:.3f}·(u - v) + {params.h:.3f}")
                steps.append("  5. Plot surface")
        
        elif surface_type == SurfaceType.CYLINDER:
            if orientation == 'Z':
                steps.append("Method: Parametric cylindrical representation")
                steps.append("Steps:")
                steps.append("  1. Set θ ∈ [0, 2π] (angular parameter)")
                steps.append("  2. Set z ∈ [-∞, +∞] (linear extension)")
                steps.append(f"  3. Compute: x = {params.a:.3f}·cos(θ) + {params.h:.3f}")
                steps.append(f"  4. Compute: y = {params.b:.3f}·sin(θ) + {params.k:.3f}")
                steps.append(f"  5. z varies freely (extends infinitely)")
                steps.append("  6. Plot cylindrical surface")
            elif orientation == 'Y':
                steps.append("Method: Parametric cylindrical representation")
                steps.append("Steps:")
                steps.append("  1. Set θ ∈ [0, 2π]")
                steps.append("  2. Set y ∈ [-∞, +∞]")
                steps.append(f"  3. Compute: x = {params.a:.3f}·cos(θ) + {params.h:.3f}")
                steps.append(f"  4. Compute: z = {params.c:.3f}·sin(θ) + {params.l:.3f}")
                steps.append(f"  5. y varies freely")
                steps.append("  6. Plot surface")
            else:
                steps.append("Method: Parametric cylindrical representation")
                steps.append("Steps:")
                steps.append("  1. Set θ ∈ [0, 2π]")
                steps.append("  2. Set x ∈ [-∞, +∞]")
                steps.append(f"  3. Compute: y = {params.b:.3f}·cos(θ) + {params.k:.3f}")
                steps.append(f"  4. Compute: z = {params.c:.3f}·sin(θ) + {params.l:.3f}")
                steps.append(f"  5. x varies freely")
                steps.append("  6. Plot surface")
        
        return steps
    
    @staticmethod
    def _get_properties(surface_type: SurfaceType, orientation: str,
                       params: SurfaceParameters) -> list:
        """Get key mathematical properties"""
        props = []
        
        if surface_type == SurfaceType.ELLIPSOID:
            props.append("• Type: Closed, bounded surface")
            props.append("• Symmetry: Symmetric about all three coordinate planes")
            props.append(f"• Volume: V = (4/3)π·a·b·c = {(4/3) * 3.14159 * params.a * params.b * params.c:.3f}")
            props.append("• All cross-sections are ellipses")
            props.append("• No ruled lines (not a ruled surface)")
        
        elif surface_type == SurfaceType.ELLIPTIC_CONE:
            props.append("• Type: Unbounded surface (extends to infinity)")
            props.append(f"• Vertex: ({params.h:.3f}, {params.k:.3f}, {params.l:.3f})")
            props.append(f"• Axis: {orientation}-axis")
            props.append("• Ruled surface (contains straight lines)")
            props.append(f"• Cross-sections perpendicular to {orientation}: ellipses")
        
        elif surface_type == SurfaceType.HYPERBOLOID_ONE_SHEET:
            props.append("• Type: Unbounded, connected (single sheet)")
            props.append(f"• Waist: perpendicular to {orientation}-axis at center")
            props.append("• Doubly ruled surface")
            props.append(f"• Cross-sections perpendicular to {orientation}: ellipses")
            props.append(f"• Cross-sections parallel to {orientation}: hyperbolas")
        
        elif surface_type == SurfaceType.HYPERBOLOID_TWO_SHEETS:
            props.append("• Type: Unbounded, disconnected (two sheets)")
            props.append(f"• Gap between sheets along {orientation}-axis")
            props.append("• Not a ruled surface")
            props.append(f"• Minimum distance between sheets: {2 * params.c:.3f}")
            props.append(f"• Opens along {orientation}-axis")
        
        elif surface_type == SurfaceType.ELLIPTIC_PARABOLOID:
            props.append("• Type: Unbounded, bowl-shaped")
            props.append(f"• Vertex: ({params.h:.3f}, {params.k:.3f}, {params.l:.3f})")
            props.append(f"• Opens along {orientation}-axis")
            props.append("• Not a ruled surface")
            props.append(f"• All cross-sections perpendicular to {orientation}: ellipses")
            props.append(f"• All cross-sections parallel to {orientation}: parabolas")
        
        elif surface_type == SurfaceType.HYPERBOLIC_PARABOLOID:
            props.append("• Type: Saddle-shaped surface (unbounded)")
            props.append(f"• Saddle point: ({params.h:.3f}, {params.k:.3f}, {params.l:.3f})")
            props.append(f"• Principal axis: {orientation}-axis")
            props.append("• Doubly ruled surface")
            props.append("• Contains hyperbolic and parabolic cross-sections")
            props.append("• Used in architecture (cooling towers, roof structures)")
        
        elif surface_type == SurfaceType.CYLINDER:
            props.append("• Type: Unbounded (extends infinitely)")
            props.append(f"• Extension: along {orientation}-axis")
            props.append("• Ruled surface (parallel lines)")
            props.append(f"• Cross-section perpendicular to {orientation}: ellipse")
            props.append("• Constant cross-section along length")
        
        return props
    
    @staticmethod
    def _get_cross_sections(surface_type: SurfaceType, orientation: str) -> list:
        """Describe cross-sections of the surface"""
        sections = []
        
        if surface_type == SurfaceType.ELLIPSOID:
            sections.append("• XY-plane (z = l): Ellipse")
            sections.append("• XZ-plane (y = k): Ellipse")
            sections.append("• YZ-plane (x = h): Ellipse")
            sections.append("• All cross-sections parallel to coord planes: Ellipses")
        
        elif surface_type == SurfaceType.ELLIPTIC_CONE:
            sections.append(f"• Perpendicular to {orientation}-axis: Ellipses (growing from vertex)")
            sections.append(f"• Parallel to {orientation}-axis: Hyperbolas or lines")
            sections.append(f"• At center ({orientation} = 0): Single point (vertex)")
        
        elif surface_type == SurfaceType.HYPERBOLOID_ONE_SHEET:
            sections.append(f"• Perpendicular to {orientation}-axis: Ellipses")
            sections.append(f"• At center: Smallest ellipse (waist)")
            sections.append(f"• Parallel to {orientation}-axis: Hyperbolas")
        
        elif surface_type == SurfaceType.HYPERBOLOID_TWO_SHEETS:
            sections.append(f"• Perpendicular to {orientation}-axis: Ellipses (two separate)")
            sections.append(f"• Near center: No intersection (gap)")
            sections.append(f"• Parallel to {orientation}-axis: Hyperbolas")
        
        elif surface_type == SurfaceType.ELLIPTIC_PARABOLOID:
            sections.append(f"• Perpendicular to {orientation}-axis: Ellipses")
            sections.append(f"• At vertex: Single point")
            sections.append(f"• Parallel to {orientation}-axis: Parabolas")
        
        elif surface_type == SurfaceType.HYPERBOLIC_PARABOLOID:
            sections.append(f"• Along {orientation}-axis: Parabola (opens one way)")
            sections.append("• Perpendicular to principal axis: Hyperbolas")
            sections.append("• At saddle point: Two intersecting lines")
        
        elif surface_type == SurfaceType.CYLINDER:
            sections.append(f"• Perpendicular to {orientation}-axis: Ellipse (constant)")
            sections.append(f"• Parallel to {orientation}-axis: Parallel lines")
            sections.append("• Surface is translation of ellipse")
        
        return sections
