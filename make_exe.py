"""
Quick build script - Just run this to create exe
"""
import subprocess
import sys

print("Building QuadricSurfaces.exe...")
print("-" * 50)

try:
    subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed", 
        "--name=QuadricSurfaces",
        "--clean",
        "quadric_surfaces.py"
    ], check=True)
    
    print("-" * 50)
    print("SUCCESS! Executable created at: dist\\QuadricSurfaces.exe")
    print("-" * 50)
    
except Exception as e:
    print(f"ERROR: {e}")
    
input("\nPress Enter to close...")
