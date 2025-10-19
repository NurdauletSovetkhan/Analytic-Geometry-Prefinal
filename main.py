"""
Quadric Surface Visualizer - Entry Point
Main entry point for the Quadric Surface Visualizer application.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from ui.main_window import QuadricApp


def main():
    """Main entry point for the application"""
    app = QuadricApp()
    app.mainloop()


if __name__ == "__main__":
    main()
