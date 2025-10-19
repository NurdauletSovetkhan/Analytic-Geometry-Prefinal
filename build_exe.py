"""
Build script to create standalone .exe using PyInstaller
Run this script to generate a standalone executable file.

Usage:
    python build_exe.py
"""

import os
import sys
import subprocess

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
        return True
    except ImportError:
        print("✗ PyInstaller is not installed")
        print("\nInstalling PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")
        return True

def build_exe():
    """Build the executable using PyInstaller"""
    print("\n" + "="*60)
    print("Building Quadric Surface Visualizer executable...")
    print("="*60 + "\n")
    
    # PyInstaller command - use python -m to ensure it works
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=QuadricVisualizer",
        "--onefile",                    # Create a single exe file
        "--windowed",                   # No console window
        "--icon=NONE",                  # No icon (you can add one later)
        "--add-data=src;src",          # Include src directory
        "--hidden-import=customtkinter",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        "--hidden-import=PIL",
        "--hidden-import=packaging",
        "--collect-all=customtkinter",
        "main.py"
    ]
    
    print("Running PyInstaller...")
    print()
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*60)
        print("✓ Build completed successfully!")
        print("="*60)
        print("\nThe executable file is located at:")
        print("  dist\\QuadricVisualizer.exe")
        print("\nYou can now:")
        print("  1. Double-click QuadricVisualizer.exe to run the application")
        print("  2. Move it to any location on your computer")
        print("  3. Create a desktop shortcut for easy access")
        print("\nNote: The first launch may take a few seconds as the")
        print("      application unpacks itself.")
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with error: {e}")
        return False
    
    return True

def main():
    print("Quadric Surface Visualizer - EXE Builder")
    print("="*60)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("✗ Error: main.py not found!")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check and install PyInstaller
    if not check_pyinstaller():
        print("✗ Failed to install PyInstaller")
        sys.exit(1)
    
    # Build the executable
    if build_exe():
        print("\n✓ All done!")
    else:
        print("\n✗ Build process failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
