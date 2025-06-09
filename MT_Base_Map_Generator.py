import tkinter as tk
from tkinter import ttk, messagebox
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from shapely.geometry import Point
import os

class MontanaBaseMapGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Montana Base Map Generator")
        self.root.geometry("1200x800")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create and pack the map frame
        self.map_frame = ttk.Frame(self.main_frame)
        self.map_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create buttons frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Create a custom style for larger buttons
        style = ttk.Style()
        style.configure('Large.TButton', font=('Arial', 14, 'bold'), padding=(20, 10))
        
        # Add Generate Map button with large style
        self.generate_btn = ttk.Button(
            self.button_frame, 
            text="Generate Base Map", 
            command=self.generate_map,
            style='Large.TButton'
        )
        self.generate_btn.pack(side=tk.LEFT, padx=20, pady=10, ipadx=30, ipady=15)
        
        # Add Clear button with large style
        self.clear_btn = ttk.Button(
            self.button_frame, 
            text="Clear", 
            command=self.clear_map,
            style='Large.TButton'
        )
        self.clear_btn.pack(side=tk.LEFT, padx=20, pady=10, ipadx=30, ipady=15)
        
        # Initialize the figure and canvas
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.map_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Initialize with a blank white canvas
        self.initialize_blank_canvas()
        
        # Load Montana boundary
        self.load_montana_boundary()

    def initialize_blank_canvas(self):
        """Initialize a blank white canvas"""
        self.ax.clear()
        self.ax.set_facecolor('white')
        self.fig.patch.set_facecolor('white')
        self.ax.axis('off')
        self.canvas.draw()

    def clear_map(self):
        """Clear the map and return to blank white canvas"""
        self.initialize_blank_canvas()

    def load_montana_boundary(self):
        try:
            # Load Montana counties shapefile
            counties_path = "MontanaCounties_shp/County.shp"
            self.counties_gdf = gpd.read_file(counties_path)
            
            # Create state boundary by dissolving all counties
            self.montana_gdf = self.counties_gdf.dissolve(by=None, aggfunc='first')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Montana boundary: {str(e)}")
            self.counties_gdf = None
            self.montana_gdf = None

    def generate_map(self):
        if self.counties_gdf is None or self.montana_gdf is None:
            messagebox.showerror("Error", "Montana boundary data not loaded!")
            return
        
        # Clear the current plot
        self.ax.clear()
        
        # Plot all counties with white fill and black boundaries
        self.counties_gdf.plot(ax=self.ax,
                             color='white',      # White fill for counties
                             edgecolor='black',  # Black boundary lines
                             linewidth=1.0)      # Thin, crisp lines
        
        # Set white background
        self.ax.set_facecolor('white')
        self.fig.patch.set_facecolor('white')
        
        # Remove axes
        self.ax.axis('off')
        
        # Adjust the plot to show only Montana with some padding
        bounds = self.montana_gdf.total_bounds
        padding = 0.2  # Add 20% padding around the map
        x_padding = (bounds[2] - bounds[0]) * padding
        y_padding = (bounds[3] - bounds[1]) * padding
        
        self.ax.set_xlim(bounds[0] - x_padding, bounds[2] + x_padding)
        self.ax.set_ylim(bounds[1] - y_padding, bounds[3] + y_padding)
        
        # Set aspect ratio to equal for proper geographic display
        self.ax.set_aspect('equal')
        
        # Update the canvas
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = MontanaBaseMapGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 