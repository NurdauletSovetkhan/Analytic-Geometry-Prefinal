"""
Quadric Surface Models and Calculations
Contains the mathematical definitions and computation logic for all quadric surfaces.
"""

from enum import Enum
import numpy as np
from dataclasses import dataclass
from typing import Tuple, Optional


class SurfaceType(Enum):
    """Enumeration of all supported quadric surface types"""
    ELLIPSOID = "Ellipsoid"
    ELLIPTIC_CONE = "Elliptic Cone"
    HYPERBOLOID_ONE_SHEET = "Hyperboloid of One Sheet"
    HYPERBOLOID_TWO_SHEETS = "Hyperboloid of Two Sheets"
    ELLIPTIC_PARABOLOID = "Elliptic Paraboloid"
    HYPERBOLIC_PARABOLOID = "Hyperbolic Paraboloid"
    CYLINDER = "Cylinder"


@dataclass
class SurfaceParameters:
    """Data class for surface parameters"""
    a: float
    b: float
    c: float
    h: float = 0.0
    k: float = 0.0
    l: float = 0.0
    
    def validate(self) -> Tuple[bool, Optional[str]]:
        """Validate parameters"""
        if self.a <= 0 or self.b <= 0 or self.c <= 0:
            return False, "Parameters a, b, c must be positive (> 0)"
        return True, None


class QuadricSurface:
    """Base class for quadric surface calculations and generation"""
    
    def __init__(self, surface_type: SurfaceType, params: SurfaceParameters, 
                 orientation: str = 'Z', grid_size: int = 100):
        self.surface_type = surface_type
        self.params = params
        self.orientation = orientation
        self.grid_size = grid_size
    
    def generate_surface(self, range_min: float = -10, range_max: float = 10):
        """Generate surface coordinates based on type"""
        method_map = {
            SurfaceType.ELLIPSOID: self._generate_ellipsoid,
            SurfaceType.ELLIPTIC_CONE: self._generate_elliptic_cone,
            SurfaceType.HYPERBOLOID_ONE_SHEET: self._generate_hyperboloid_one,
            SurfaceType.HYPERBOLOID_TWO_SHEETS: self._generate_hyperboloid_two,
            SurfaceType.ELLIPTIC_PARABOLOID: self._generate_elliptic_paraboloid,
            SurfaceType.HYPERBOLIC_PARABOLOID: self._generate_hyperbolic_paraboloid,
            SurfaceType.CYLINDER: self._generate_cylinder,
        }
        
        generator = method_map.get(self.surface_type)
        if generator:
            return generator(range_min, range_max)
        return None, None, None
    
    def _generate_ellipsoid(self, range_min: float, range_max: float):
        """Generate ellipsoid coordinates"""
        phi = np.linspace(0, 2 * np.pi, self.grid_size)
        theta = np.linspace(0, np.pi, self.grid_size)
        PHI, THETA = np.meshgrid(phi, theta)
        
        X = self.params.a * np.sin(THETA) * np.cos(PHI) + self.params.h
        Y = self.params.b * np.sin(THETA) * np.sin(PHI) + self.params.k
        Z = self.params.c * np.cos(THETA) + self.params.l
        
        return X, Y, Z
    
    def _generate_elliptic_cone(self, range_min: float, range_max: float):
        """Generate elliptic cone coordinates"""
        u = np.linspace(range_min, range_max, self.grid_size)
        v = np.linspace(range_min, range_max, self.grid_size)
        U, V = np.meshgrid(u, v)
        
        if self.orientation == 'Z':
            X = U
            Y = V
            with np.errstate(invalid='ignore'):
                Z_pos = self.params.c * np.sqrt(
                    (X - self.params.h)**2 / self.params.a**2 + 
                    (Y - self.params.k)**2 / self.params.b**2
                ) + self.params.l
                Z_neg = -self.params.c * np.sqrt(
                    (X - self.params.h)**2 / self.params.a**2 + 
                    (Y - self.params.k)**2 / self.params.b**2
                ) + self.params.l
            return X, Y, (Z_pos, Z_neg)
        
        elif self.orientation == 'Y':
            X = U
            Z = V
            with np.errstate(invalid='ignore'):
                Y_pos = self.params.b * np.sqrt(
                    (X - self.params.h)**2 / self.params.a**2 + 
                    (Z - self.params.l)**2 / self.params.c**2
                ) + self.params.k
                Y_neg = -self.params.b * np.sqrt(
                    (X - self.params.h)**2 / self.params.a**2 + 
                    (Z - self.params.l)**2 / self.params.c**2
                ) + self.params.k
            return X, (Y_pos, Y_neg), Z
        
        else:  # X axis
            Y = U
            Z = V
            with np.errstate(invalid='ignore'):
                X_pos = self.params.a * np.sqrt(
                    (Y - self.params.k)**2 / self.params.b**2 + 
                    (Z - self.params.l)**2 / self.params.c**2
                ) + self.params.h
                X_neg = -self.params.a * np.sqrt(
                    (Y - self.params.k)**2 / self.params.b**2 + 
                    (Z - self.params.l)**2 / self.params.c**2
                ) + self.params.h
            return (X_pos, X_neg), Y, Z
    
    def _generate_hyperboloid_one(self, range_min: float, range_max: float):
        """Generate hyperboloid of one sheet coordinates"""
        u = np.linspace(range_min, range_max, self.grid_size)
        v = np.linspace(range_min, range_max, self.grid_size)
        U, V = np.meshgrid(u, v)
        
        if self.orientation == 'Z':
            X = U
            Y = V
            with np.errstate(invalid='ignore'):
                Z_pos = self.params.c * np.sqrt(
                    (X - self.params.h)**2 / self.params.a**2 + 
                    (Y - self.params.k)**2 / self.params.b**2 - 1
                ) + self.params.l
                Z_neg = -self.params.c * np.sqrt(
                    (X - self.params.h)**2 / self.params.a**2 + 
                    (Y - self.params.k)**2 / self.params.b**2 - 1
                ) + self.params.l
            return X, Y, (Z_pos, Z_neg)
        
        elif self.orientation == 'Y':
            X = U
            Z = V
            with np.errstate(invalid='ignore'):
                Y_pos = self.params.b * np.sqrt(
                    (X - self.params.h)**2 / self.params.a**2 + 
                    (Z - self.params.l)**2 / self.params.c**2 - 1
                ) + self.params.k
                Y_neg = -self.params.b * np.sqrt(
                    (X - self.params.h)**2 / self.params.a**2 + 
                    (Z - self.params.l)**2 / self.params.c**2 - 1
                ) + self.params.k
            return X, (Y_pos, Y_neg), Z
        
        else:  # X axis
            Y = U
            Z = V
            with np.errstate(invalid='ignore'):
                X_pos = self.params.a * np.sqrt(
                    (Y - self.params.k)**2 / self.params.b**2 + 
                    (Z - self.params.l)**2 / self.params.c**2 - 1
                ) + self.params.h
                X_neg = -self.params.a * np.sqrt(
                    (Y - self.params.k)**2 / self.params.b**2 + 
                    (Z - self.params.l)**2 / self.params.c**2 - 1
                ) + self.params.h
            return (X_pos, X_neg), Y, Z
    
    def _generate_hyperboloid_two(self, range_min: float, range_max: float):
        """Generate hyperboloid of two sheets coordinates"""
        u = np.linspace(range_min, range_max, self.grid_size)
        v = np.linspace(range_min, range_max, self.grid_size)
        U, V = np.meshgrid(u, v)
        
        if self.orientation == 'Z':
            X = U
            Y = V
            with np.errstate(invalid='ignore'):
                Z_pos = self.params.c * np.sqrt(
                    1 + (X - self.params.h)**2 / self.params.a**2 + 
                    (Y - self.params.k)**2 / self.params.b**2
                ) + self.params.l
                Z_neg = -self.params.c * np.sqrt(
                    1 + (X - self.params.h)**2 / self.params.a**2 + 
                    (Y - self.params.k)**2 / self.params.b**2
                ) + self.params.l
            return X, Y, (Z_pos, Z_neg)
        
        elif self.orientation == 'Y':
            X = U
            Z = V
            with np.errstate(invalid='ignore'):
                Y_pos = self.params.b * np.sqrt(
                    1 + (X - self.params.h)**2 / self.params.a**2 + 
                    (Z - self.params.l)**2 / self.params.c**2
                ) + self.params.k
                Y_neg = -self.params.b * np.sqrt(
                    1 + (X - self.params.h)**2 / self.params.a**2 + 
                    (Z - self.params.l)**2 / self.params.c**2
                ) + self.params.k
            return X, (Y_pos, Y_neg), Z
        
        else:  # X axis
            Y = U
            Z = V
            with np.errstate(invalid='ignore'):
                X_pos = self.params.a * np.sqrt(
                    1 + (Y - self.params.k)**2 / self.params.b**2 + 
                    (Z - self.params.l)**2 / self.params.c**2
                ) + self.params.h
                X_neg = -self.params.a * np.sqrt(
                    1 + (Y - self.params.k)**2 / self.params.b**2 + 
                    (Z - self.params.l)**2 / self.params.c**2
                ) + self.params.h
            return (X_pos, X_neg), Y, Z
    
    def _generate_elliptic_paraboloid(self, range_min: float, range_max: float):
        """Generate elliptic paraboloid coordinates"""
        u = np.linspace(range_min, range_max, self.grid_size)
        v = np.linspace(range_min, range_max, self.grid_size)
        U, V = np.meshgrid(u, v)
        
        if self.orientation == 'Z':
            X = U
            Y = V
            Z = ((X - self.params.h)**2 / self.params.a**2 + 
                 (Y - self.params.k)**2 / self.params.b**2) * self.params.c + self.params.l
            return X, Y, Z
        
        elif self.orientation == 'Y':
            X = U
            Z = V
            Y = ((X - self.params.h)**2 / self.params.a**2 + 
                 (Z - self.params.l)**2 / self.params.c**2) * self.params.b + self.params.k
            return X, Y, Z
        
        else:  # X axis
            Y = U
            Z = V
            X = ((Y - self.params.k)**2 / self.params.b**2 + 
                 (Z - self.params.l)**2 / self.params.c**2) * self.params.a + self.params.h
            return X, Y, Z
    
    def _generate_hyperbolic_paraboloid(self, range_min: float, range_max: float):
        """Generate hyperbolic paraboloid coordinates"""
        u = np.linspace(range_min, range_max, self.grid_size)
        v = np.linspace(range_min, range_max, self.grid_size)
        U, V = np.meshgrid(u, v)
        
        if self.orientation == 'Z':
            X = U
            Y = V
            Z = ((Y - self.params.k)**2 / self.params.b**2 - 
                 (X - self.params.h)**2 / self.params.a**2) * self.params.c + self.params.l
            return X, Y, Z
        
        elif self.orientation == 'Y':
            X = U
            Z = V
            Y = ((Z - self.params.l)**2 / self.params.c**2 - 
                 (X - self.params.h)**2 / self.params.a**2) * self.params.b + self.params.k
            return X, Y, Z
        
        else:  # X axis
            Y = U
            Z = V
            X = ((Y - self.params.k)**2 / self.params.b**2 - 
                 (Z - self.params.l)**2 / self.params.c**2) * self.params.a + self.params.h
            return X, Y, Z
    
    def _generate_cylinder(self, range_min: float, range_max: float):
        """Generate cylinder coordinates"""
        if self.orientation == 'Z':
            theta = np.linspace(0, 2 * np.pi, self.grid_size)
            z = np.linspace(-10, 10, self.grid_size)
            THETA, Z = np.meshgrid(theta, z)
            
            X = self.params.a * np.cos(THETA) + self.params.h
            Y = self.params.b * np.sin(THETA) + self.params.k
            Z = Z + self.params.l
            return X, Y, Z
        
        elif self.orientation == 'Y':
            theta = np.linspace(0, 2 * np.pi, self.grid_size)
            y = np.linspace(-10, 10, self.grid_size)
            THETA, Y = np.meshgrid(theta, y)
            
            X = self.params.a * np.cos(THETA) + self.params.h
            Z = self.params.c * np.sin(THETA) + self.params.l
            Y = Y + self.params.k
            return X, Y, Z
        
        else:  # X missing
            theta = np.linspace(0, 2 * np.pi, self.grid_size)
            x = np.linspace(-10, 10, self.grid_size)
            THETA, X = np.meshgrid(theta, x)
            
            Y = self.params.b * np.cos(THETA) + self.params.k
            Z = self.params.c * np.sin(THETA) + self.params.l
            X = X + self.params.h
            return X, Y, Z
