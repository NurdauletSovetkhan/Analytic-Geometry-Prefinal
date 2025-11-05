# Examples and Usage Guide

## Quick Start Examples

### Example 1: Ellipsoid (Sphere)
1. Select "Ellipsoid"
2. Set parameters: a=2, b=2, c=2
3. Center: (0, 0, 0)
4. Click "Plot"
**Result**: Perfect sphere with radius 2

### Example 2: Ellipsoid (Stretched)
1. Select "Ellipsoid"
2. Set parameters: a=3, b=2, c=1
3. Center: (0, 0, 0)
4. Click "Plot"
**Result**: Ellipsoid stretched along x-axis

### Example 3: Elliptic Cone
1. Select "Elliptic Cone"
2. Orientation: "Along z-axis"
3. Set parameters: a=1, b=1, c=1
4. Center: (0, 0, 0)
5. Click "Plot"
**Result**: Double cone with circular cross-section

### Example 4: Hyperboloid of One Sheet
1. Select "Hyperboloid of One Sheet"
2. Orientation: "Along z-axis"
3. Set parameters: a=2, b=2, c=1
4. Center: (0, 0, 0)
5. Click "Plot"
**Result**: Hourglass-shaped surface (cooling tower shape)

### Example 5: Hyperboloid of Two Sheets
1. Select "Hyperboloid of Two Sheets"
2. Orientation: "Along z-axis"
3. Set parameters: a=1, b=1, c=2
4. Center: (0, 0, 0)
5. Range: z in [-10, 10]
6. Click "Plot"
**Result**: Two separate bowl-shaped surfaces

### Example 6: Elliptic Paraboloid
1. Select "Elliptic Paraboloid"
2. Orientation: "Along z-axis"
3. Set parameters: a=1, b=1, c=1
4. Center: (0, 0, 0)
5. Click "Plot"
**Result**: Upward-opening paraboloid (satellite dish shape)

### Example 7: Hyperbolic Paraboloid (Saddle)
1. Select "Hyperbolic Paraboloid"
2. Orientation: "Along z-axis"
3. Set parameters: a=1, b=1, c=1
4. Center: (0, 0, 0)
5. Click "Plot"
**Result**: Classic saddle surface (Pringles chip shape)

### Example 8: Elliptic Cylinder
1. Select "Cylinders"
2. Cylinder Type: "Elliptic"
3. Set parameters: a=2, b=1
4. Center: (0, 0, 0)
5. Click "Plot"
**Result**: Elliptical tube extending along z-axis

### Example 9: Hyperbolic Cylinder
1. Select "Cylinders"
2. Cylinder Type: "Hyperbolic"
3. Set parameters: a=2, b=1
4. Center: (0, 0, 0)
5. Click "Plot"
**Result**: Two separate curved sheets

### Example 10: Parabolic Cylinder
1. Select "Cylinders"
2. Cylinder Type: "Parabolic"
3. Set parameters: p=1
4. Center: (0, 0, 0)
5. Click "Plot"
**Result**: U-shaped tube extending along z-axis

## Testing Different Orientations

### Cone along different axes:
**Z-axis**: Standard vertical cone
**Y-axis**: Cone opening horizontally (front-back)
**X-axis**: Cone opening horizontally (left-right)

### Paraboloid orientations:
**Z-axis**: Opens upward/downward
**Y-axis**: Opens forward/backward
**X-axis**: Opens left/right

## Using the Randomize Feature

1. Click "Randomize" button
2. Random values for a, b, c will be generated (between 1 and 10)
3. Click "Plot" to visualize with new parameters
4. Observe how different parameter values affect the shape

## Tips for Best Visualization

1. **Adjust Range**: If surface is too small/large, adjust xmin/xmax, ymin/ymax, zmin/zmax
2. **Center Position**: Move center to see surface from different perspectives
3. **Mouse Controls**:
   - Left click + drag: Rotate view
   - Scroll wheel: Zoom in/out
   - Right click + drag: Pan view

4. **For Cylinders**: Increase z-range to see more of the infinite extent

5. **For Two-Sheet Hyperboloid**: Ensure z-range is large enough to see both sheets

## Common Parameter Combinations

### Circular Cross-Sections:
- For ellipsoid: a = b = c (sphere)
- For cone: a = b (circular cone)
- For paraboloid: a = b (circular paraboloid)

### Highly Eccentric Shapes:
- Try a=5, b=1, c=0.5 for ellipsoid
- Creates very stretched/flattened surfaces

### Symmetric Saddle:
- For hyperbolic paraboloid: a=1, b=1
- Creates perfectly balanced saddle

## Understanding the Traces

**Red line**: Intersection with XY-plane (z = constant)
**Blue line**: Intersection with XZ-plane (y = constant)
**Green line**: Intersection with YZ-plane (x = constant)

These traces help understand the shape by showing how it cuts through coordinate planes.

## Assignment Requirements Checklist

✓ Menu-driven interface with buttons
✓ All 7 surface types supported
✓ Orientation selection (except ellipsoid)
✓ Parameter input (a, b, c > 0)
✓ Center coordinates (h, k, l)
✓ Range selection (xmin/max, ymin/max, zmin/max)
✓ Matplotlib 3D plotting
✓ Mouse-controlled rotation and zoom
✓ Randomize, Plot, Clear buttons
✓ Analysis Results panel showing:
  - Surface type and orientation
  - Equation in canonical form
  - Parameters and center
  - Qualitative description
✓ Coordinate axes displayed
✓ Center marked on plot
✓ Traces on coordinate planes (for ellipsoid)
✓ Input validation
✓ Works as Python script
✓ Can be compiled to .exe using build_exe.bat

## Troubleshooting

**Problem**: Surface not visible
**Solution**: Increase the range values or adjust center position

**Problem**: Surface looks flat
**Solution**: Check that a, b, c are not too similar; try more varied values

**Problem**: Program crashes on Plot
**Solution**: Verify all inputs are positive numbers

**Problem**: Two-sheet hyperboloid shows only one sheet
**Solution**: Increase z-range to show both sheets

**Problem**: Cylinder too short
**Solution**: Increase z-range (e.g., zmin=-20, zmax=20)
