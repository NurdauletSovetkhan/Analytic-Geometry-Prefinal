"""
Script to build executable for Quadric Surfaces Visualizer
Run this script to create a standalone .exe file
"""

import subprocess
import sys
import os
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
        return True
    except ImportError:
        print("✗ PyInstaller is not installed")
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    print("\n📦 Installing PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install PyInstaller")
        return False

def build_exe():
    """Build the executable"""
    print("\n🔨 Building executable...")
    print("=" * 60)
    
    # Get the current directory
    current_dir = Path(__file__).parent
    script_path = current_dir / "quadric_surfaces.py"
    
    if not script_path.exists():
        print(f"✗ Error: {script_path} not found!")
        return False
    
    # PyInstaller command
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",           # Create a single executable
        "--windowed",          # No console window
        "--name=QuadricSurfaces",  # Name of the executable
        "--icon=NONE",         # No icon (you can add one later)
        "--clean",             # Clean cache
        str(script_path)
    ]
    
    print(f"Running: {' '.join(cmd)}")
    print("=" * 60)
    
    try:
        subprocess.check_call(cmd, cwd=str(current_dir))
        print("\n" + "=" * 60)
        print("✓ Build successful!")
        print("=" * 60)
        
        # Find the executable
        dist_dir = current_dir / "dist"
        exe_path = dist_dir / "QuadricSurfaces.exe"
        
        if exe_path.exists():
            print(f"\n📦 Executable created at:")
            print(f"   {exe_path}")
            print(f"\n📊 File size: {exe_path.stat().st_size / (1024*1024):.2f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False

def cleanup():
    """Ask user if they want to clean up build files"""
    print("\n" + "=" * 60)
    response = input("🗑️  Clean up build files (build/, *.spec)? (y/n): ").strip().lower()
    
    if response == 'y':
        import shutil
        current_dir = Path(__file__).parent
        
        # Remove build directory
        build_dir = current_dir / "build"
        if build_dir.exists():
            shutil.rmtree(build_dir)
            print("✓ Removed build/ directory")
        
        # Remove .spec file
        spec_file = current_dir / "QuadricSurfaces.spec"
        if spec_file.exists():
            spec_file.unlink()
            print("✓ Removed .spec file")
        
        print("✓ Cleanup complete")
    else:
        print("ℹ️  Build files kept (you can delete them manually later)")

def main():
    print("=" * 60)
    print("  Quadric Surfaces Visualizer - Executable Builder")
    print("=" * 60)
    
    # Check Python version
    print(f"\n🐍 Python version: {sys.version}")
    print(f"📁 Working directory: {Path(__file__).parent}")
    
    # Check if PyInstaller is installed
    if not check_pyinstaller():
        response = input("\nInstall PyInstaller now? (y/n): ").strip().lower()
        if response == 'y':
            if not install_pyinstaller():
                print("\n✗ Cannot proceed without PyInstaller")
                return 1
        else:
            print("\n✗ PyInstaller is required to build executable")
            return 1
    
    # Build executable
    print("\n" + "=" * 60)
    response = input("Start building executable? (y/n): ").strip().lower()
    
    if response != 'y':
        print("Build cancelled")
        return 0
    
    if build_exe():
        cleanup()
        print("\n" + "=" * 60)
        print("✅ All done! You can now run:")
        print("   .\\dist\\QuadricSurfaces.exe")
        print("=" * 60)
        return 0
    else:
        print("\n✗ Build failed")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        input("\nPress Enter to exit...")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)
