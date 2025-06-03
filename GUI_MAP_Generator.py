import tkinter as tk
from tkinter import ttk, StringVar, filedialog, messagebox, Canvas
import os
from pathlib import Path
import datetime
import sys

class SplashScreen:
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.overrideredirect(True)
        self.root.attributes('-alpha', 0.9)
        self.root.attributes('-topmost', True)
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Window dimensions
        width = 400
        height = 200
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create frame
        frame = ttk.Frame(self.root, relief='raised', borderwidth=2)
        frame.pack(fill='both', expand=True)
        
        # Add title
        title = ttk.Label(
            frame, 
            text="Montana Bee County Map Generator",
            font=('Helvetica', 16, 'bold'),
            foreground='dark green'
        )
        title.pack(pady=20)
        
        # Add loading text
        self.status = ttk.Label(
            frame,
            text="Initializing...",
            font=('Helvetica', 10)
        )
        self.status.pack(pady=10)
        
        # Add progress bar
        self.progress = ttk.Progressbar(
            frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=20)
        self.progress.start(10)
        
        self.root.update()
    
    def update_status(self, message):
        self.status.config(text=message)
        self.root.update()
    
    def destroy(self):
        self.root.destroy()

class ToastNotification:
    def __init__(self, parent):
        self.parent = parent
        
    def show_toast(self, message, duration=3000, error=False):
        # Create toast window
        toast = tk.Toplevel(self.parent)
        toast.withdraw()  # Hide initially for position calculation
        
        # Remove window decorations
        toast.overrideredirect(True)
        
        # Create frame with border
        frame = ttk.Frame(toast, style='Toast.TFrame')
        frame.pack(fill='both', expand=True)
        
        # Add message with icon
        msg_frame = ttk.Frame(frame)
        msg_frame.pack(pady=10, padx=20)
        
        # Icon and color based on type
        if error:
            icon_text = "✕"
            icon_color = 'red'
            msg_color = 'red'
        else:
            icon_text = "✓"
            icon_color = 'green'
            msg_color = 'black'
        
        # Icon label
        icon_label = ttk.Label(msg_frame, text=icon_text, font=('Helvetica', 14, 'bold'), foreground=icon_color)
        icon_label.pack(side='left', padx=(0, 10))
        
        # Message with color
        msg_label = ttk.Label(msg_frame, text=message, font=('Helvetica', 10), foreground=msg_color)
        msg_label.pack(side='left')
        
        # Position toast at bottom right of main window
        toast.update_idletasks()  # Update to get actual size
        main_x = self.parent.winfo_x()
        main_y = self.parent.winfo_y()
        main_width = self.parent.winfo_width()
        main_height = self.parent.winfo_height()
        
        toast_width = toast.winfo_width()
        toast_height = toast.winfo_height()
        
        x = main_x + main_width - toast_width - 20
        y = main_y + main_height - toast_height - 20
        
        toast.geometry(f"+{x}+{y}")
        toast.deiconify()  # Show the toast
        
        # Destroy after duration
        toast.after(duration, toast.destroy)

class SelectionScreen:
    def __init__(self, parent, main_app, from_analysis=False):
        self.root = tk.Toplevel(parent)
        self.root.title("Analysis Selection")
        self.main_app = main_app
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate window size (80% of screen)
        self.default_width = int(screen_width * 0.8)
        self.default_height = int(screen_height * 0.8)
        
        # Calculate center position
        self.x_position = (screen_width - self.default_width) // 2
        self.y_position = (screen_height - self.default_height) // 2
        
        # Set minimum size before setting geometry
        self.root.minsize(600, 400)
        
        if from_analysis:
            # Set to full screen when coming from analysis pages
            self.root.geometry(f"{screen_width}x{screen_height}+0+0")
            self.root.state('zoomed')
        else:
            # Center the window using geometry manager
            self.root.geometry(f"{self.default_width}x{self.default_height}+{self.x_position}+{self.y_position}")
        
        # Update window to ensure proper sizing
        self.root.update_idletasks()
        
        # Bind window state change
        self.root.bind("<Configure>", self.on_window_resize)
        
        # Configure styles
        style = ttk.Style()
        style.configure('Title.TLabel',
                       font=('Helvetica', 32, 'bold'),
                       foreground='dark green')
        
        style.configure('Subtitle.TLabel',
                       font=('Helvetica', 24),
                       foreground='dark green')
        
        style.configure('Selection.TButton',
                       font=('Helvetica', 14, 'bold'),
                       padding=20)
        
        style.configure('Description.TLabel',
                       font=('Helvetica', 12),
                       foreground='gray')
        
        # Create main container with padding
        main_container = ttk.Frame(self.root, padding="40")
        main_container.pack(fill='both', expand=True)
        
        # Create a content frame to center everything vertically
        content_frame = ttk.Frame(main_container)
        content_frame.pack(expand=True)
        
        # Add logo or icon (if available)
        try:
            logo_path = "bee_logo.png"  # You can add a logo file later
            if os.path.exists(logo_path):
                logo = tk.PhotoImage(file=logo_path)
                logo_label = ttk.Label(content_frame, image=logo)
                logo_label.image = logo  # Keep a reference
                logo_label.pack(pady=(0, 30))
        except:
            pass
        
        # Title with shadow effect
        title_frame = ttk.Frame(content_frame)
        title_frame.pack(pady=(0, 40))
        
        title_label = ttk.Label(
            title_frame,
            text="Montana Bee County Map Generator",
            style='Title.TLabel'
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = ttk.Label(
            content_frame,
            text="Select Analysis Type",
            style='Subtitle.TLabel'
        )
        subtitle_label.pack(pady=(0, 60))
        
        # Button container for consistent width
        button_container = ttk.Frame(content_frame)
        button_container.pack(expand=True)
        
        # Single Year Analysis Section
        single_year_frame = ttk.Frame(button_container)
        single_year_frame.pack(pady=(0, 30))
        
        single_year_btn = ttk.Button(
            single_year_frame,
            text="Single Year Analysis",
            style='Selection.TButton',
            command=self.start_single_year_analysis,
            width=30
        )
        single_year_btn.pack()
        
        single_year_desc = ttk.Label(
            single_year_frame,
            text="Analyze bee distribution before and after a specific year",
            style='Description.TLabel'
        )
        single_year_desc.pack(pady=(10, 0))
        
        # Dual Year Analysis Section
        dual_year_frame = ttk.Frame(button_container)
        dual_year_frame.pack()
        
        dual_year_btn = ttk.Button(
            dual_year_frame,
            text="Dual Year Analysis",
            style='Selection.TButton',
            command=self.start_dual_year_analysis,
            width=30
        )
        dual_year_btn.pack()
        
        dual_year_desc = ttk.Label(
            dual_year_frame,
            text="Analyze bee distribution across three time periods using two year boundaries",
            style='Description.TLabel'
        )
        dual_year_desc.pack(pady=(10, 0))
        
        # Configure hover effects
        style.map('Selection.TButton',
                 background=[('active', '#e1e1e1')],
                 foreground=[('active', 'dark green')])
        
        # Add version or copyright info at bottom
        footer_frame = ttk.Frame(main_container)
        footer_frame.pack(side='bottom', fill='x')
        
        current_year = datetime.datetime.now().year
        copyright_label = ttk.Label(
            footer_frame,
            text=f"© {current_year} Montana Bee Project",
            font=('Helvetica', 8),
            foreground='gray'
        )
        copyright_label.pack(side='right')
    
    def start_single_year_analysis(self):
        self.root.destroy()
        SingleYearAnalysis(self.root.master, self.main_app)
    
    def start_dual_year_analysis(self):
        self.root.destroy()
        DualYearAnalysis(self.root.master, self.main_app)
    
    def on_window_resize(self, event=None):
        if self.root.state() == 'normal':
            self.root.geometry(f"{self.default_width}x{self.default_height}+{self.x_position}+{self.y_position}")

class MainApplication:
    def __init__(self):
        # Create and hide the root window
        self.root = tk.Tk()
        self.root.withdraw()
        
        # Initialize variables
        self.gdf = None
        self.pd = None
        self.gpd = None
        self.plt = None
        self.FigureCanvasTkAgg = None
        
        # Show splash screen
        self.splash = SplashScreen(self.root)
        
        # Start loading sequence
        self.root.after(100, self.load_step_1)
        
        # Start the event loop
        self.root.mainloop()
    
    def load_step_1(self):
        """Load pandas"""
        try:
            self.splash.update_status("From Billings to Bozeman...")
            import pandas as pd
            self.pd = pd
            self.root.after(100, self.load_step_2)
        except Exception as e:
            self.show_error(f"Error loading pandas: {str(e)}")
    
    def load_step_2(self):
        """Load geopandas"""
        try:
            self.splash.update_status("Spanning the Big Sky Country...")
            import geopandas as gpd
            self.gpd = gpd
            self.root.after(100, self.load_step_3)
        except Exception as e:
            self.show_error(f"Error loading geopandas: {str(e)}")
    
    def load_step_3(self):
        """Load matplotlib"""
        try:
            self.splash.update_status("Mapping Montana's vast landscapes...")
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            self.plt = plt
            self.FigureCanvasTkAgg = FigureCanvasTkAgg
            self.root.after(100, self.load_step_4)
        except Exception as e:
            self.show_error(f"Error loading matplotlib: {str(e)}")
    
    def load_step_4(self):
        """Load shapefile"""
        try:
            self.splash.update_status("Connecting all 56 counties...")
            self.load_shapefile()
            self.root.after(100, self.show_selection_screen)
        except Exception as e:
            self.show_error(f"Error loading shapefile: {str(e)}")
    
    def show_selection_screen(self):
        """Show the selection screen after splash"""
        self.splash.destroy()
        SelectionScreen(self.root, self)
    
    def show_error(self, message):
        """Show error message and exit"""
        if hasattr(self, 'splash'):
            self.splash.destroy()
        messagebox.showerror("Error", message)
        self.root.quit()
        sys.exit(1)
    
    def load_shapefile(self):
        try:
            # Get the application's base directory
            if getattr(sys, 'frozen', False):
                base_dir = sys._MEIPASS
            else:
                base_dir = os.path.dirname(os.path.abspath(__file__))
            
            shapefile_path = os.path.join(base_dir, "MontanaCounties_shp", "County.shp")
            
            if not os.path.exists(shapefile_path):
                raise FileNotFoundError(
                    f"Shapefile not found at:\n{shapefile_path}\n\n"
                    "Please ensure the MontanaCounties_shp folder is in the correct location."
                )
                
            self.gdf = self.gpd.read_file(shapefile_path)
            self.gdf.columns = self.gdf.columns.str.strip()
            self.gdf["County"] = self.gdf["NAME"].str.strip().str.lower()
            self.gdf["Color"] = "white"
            
        except Exception as e:
            raise Exception(f"Error loading shapefile:\n{str(e)}\n\nPlease ensure the shapefile is not corrupted and try again.")
    
    def load_excel(self):
        path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if not path:
            return
        
        # Show loading dialog
        loading_window = tk.Tk()
        loading_window.title("Loading")
        screen_width = loading_window.winfo_screenwidth()
        screen_height = loading_window.winfo_screenheight()
        window_width = 300
        window_height = 100
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        loading_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        loading_window.overrideredirect(True)
        
        frame = ttk.Frame(loading_window, padding="20", relief="raised")
        frame.pack(fill='both', expand=True)
        
        loading_label = ttk.Label(frame, text="Loading file...\nPlease wait", font=('Helvetica', 10))
        loading_label.pack(pady=10)
        
        progress = ttk.Progressbar(frame, mode='indeterminate')
        progress.pack(fill='x', pady=5)
        progress.start(10)
        
        loading_window.update()
        
        try:
            # Load the Excel file
            self.df = self.pd.read_excel(path, sheet_name=0)
            self.df.columns = self.df.columns.str.strip()
            
            # Get just the filename from the path
            filename = path.split('/')[-1]
            
            # Validate required columns
            required_columns = ["county", "family", "genus", "species", "year"]
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            
            if missing_columns:
                progress.stop()
                loading_window.destroy()
                self.selected_file_var.set("No file selected")
                messagebox.showerror("Error", 
                    f"Missing required columns: {', '.join(missing_columns)}\n\n"
                    "The following columns are required:\n"
                    "- county: for mapping locations\n"
                    "- family: for taxonomic classification\n"
                    "- genus: for taxonomic classification\n"
                    "- species: for taxonomic classification\n"
                    "- year: for temporal analysis\n\n"
                    "Please check your Excel file and try again."
                )
                return
            
            # Process the data
            for col in required_columns:
                self.df[col] = self.df[col].astype(str).str.strip().str.lower()
            self.df["year"] = self.df["year"].astype(str).str.extract(r'(\d{4})').astype(float)
            
            # Calculate statistics
            num_records = len(self.df)
            num_families = len(self.df["family"].unique())
            num_genera = len(self.df["genus"].unique())
            num_species = len(self.df["species"].unique())
            year_range = f"{int(self.df['year'].min())} - {int(self.df['year'].max())}"
            num_counties = len(self.df["county"].unique())
            
            # Update Family dropdown with capitalized values
            family_values = sorted(self.df["family"].dropna().unique())
            family_values = [f.title() for f in family_values]
            self.family_dropdown["values"] = family_values
            self.family_dropdown.set("Select Family")
            
            # Reset other dropdowns and fields
            self.genus_dropdown.set("Select Genus")
            self.genus_dropdown["values"] = []
            self.species_dropdown.set("Select Species")
            self.species_dropdown["values"] = []
            self.year_var.set("")
            
            # Update file info display
            self.selected_file_var.set(f"✓ {filename}\n{num_records:,} records loaded")
            
            # Stop progress bar and close loading window
            progress.stop()
            loading_window.destroy()
            
            # Show success message with detailed statistics
            messagebox.showinfo("Success", 
                f"File loaded successfully!\n\n"
                f"Dataset Summary:\n"
                f"• Total Records: {num_records:,}\n"
                f"• Unique Families: {num_families}\n"
                f"• Unique Genera: {num_genera}\n"
                f"• Unique Species: {num_species}\n"
                f"• Counties Covered: {num_counties}\n"
                f"• Year Range: {year_range}\n\n"
                "Please select a Family to continue."
            )
            
            print("✅ Excel file loaded successfully!")
            
        except Exception as e:
            progress.stop()
            loading_window.destroy()
            self.selected_file_var.set("No file selected")
            error_message = str(e)
            if "No sheet named" in error_message:
                error_message = "Invalid Excel file format. Please ensure your data is in the first sheet."
            elif "Invalid file" in error_message:
                error_message = "Invalid file format. Please ensure you're uploading a valid Excel (.xlsx) file."
            
            messagebox.showerror("Error", 
                f"Error loading file:\n{error_message}\n\n"
                "Please check your Excel file format and try again."
            )
            return
    
    def update_genus_dropdown(self, event=None):
        family = self.selected_family.get().strip().lower()
        filtered = self.df[self.df["family"] == family]
        # Capitalize genus names for display
        genus_values = sorted(filtered["genus"].dropna().unique())
        genus_values = [g.title() for g in genus_values]  # Capitalize genus names
        self.genus_dropdown["values"] = genus_values
        self.genus_dropdown.set("Select Genus")
    
    def update_species_dropdown(self, event=None):
        family = self.selected_family.get().strip().lower()
        genus = self.selected_genus.get().strip().lower()
        filtered = self.df[(self.df["family"] == family) & (self.df["genus"] == genus)]
        self.species_dropdown["values"] = sorted(filtered["species"].dropna().unique())
        self.species_dropdown.set("Select Species")
    
    def is_valid_color(self, color):
        """Validate if a color string is a valid matplotlib color"""
        try:
            # Convert color to RGB
            self.plt.matplotlib.colors.to_rgb(color)
            return True
        except ValueError:
            return False

    def validate_colors(self):
        """Validate all selected colors"""
        colors = {
            'Pre-Year': self.pre_color.get(),
            'Post-Year': self.post_color.get(),
            'All Records': self.all_color.get()
        }
        
        invalid_colors = []
        for name, color in colors.items():
            if not self.is_valid_color(color):
                invalid_colors.append(f"{name} color '{color}'")
        
        if invalid_colors:
            error_msg = "Invalid colors detected:\n" + "\n".join(invalid_colors)
            self.toast.show_toast(error_msg, duration=5000, error=True)
            return False
        return True

    def on_color_change(self, event=None):
        """Validate colors when they change"""
        self.validate_colors()

    def generate_map(self):
        if self.map_canvas:
            self.map_canvas.get_tk_widget().destroy()
        
        # Validate colors first
        if not self.validate_colors():
            self.download_button.config(state="disabled")
            return
        
        gdf_copy = self.gdf.copy()
        # Initialize all counties as white
        gdf_copy["Color"] = "white"
        
        fam = self.selected_family.get().strip().lower()
        gen = self.selected_genus.get().strip().lower()
        spec = self.selected_species.get().strip().lower()
        year = self.year_var.get().strip()
        
        if not fam or not gen or not spec:
            messagebox.showerror("Missing Input", "Please select Family, Genus, and Species.")
            self.download_button.config(state="disabled")
            return
        
        filtered = self.df[(self.df["family"] == fam) & (self.df["genus"] == gen) & (self.df["species"] == spec)]
        
        if isinstance(year, str) and year.isdigit():
            year = int(year)
            # First pass: Mark counties with post-dividing year records with post_color (only if they're white)
            for county in filtered[filtered["year"] > year]["county"].unique():
                if gdf_copy.loc[gdf_copy["County"] == county, "Color"].iloc[0] == "white":
                    gdf_copy.loc[gdf_copy["County"] == county, "Color"] = self.post_color.get()
            
            # Second pass: Mark counties with pre-dividing year records with pre_color (overriding any color)
            for county in filtered[filtered["year"] <= year]["county"].unique():
                gdf_copy.loc[gdf_copy["County"] == county, "Color"] = self.pre_color.get()
        else:
            # If no year specified, mark all counties with records using all_color
            for county in filtered["county"].unique():
                gdf_copy.loc[gdf_copy["County"] == county, "Color"] = self.all_color.get()
        
        # Create figure with larger size and better proportions
        fig, ax = self.plt.subplots(figsize=(12, 11))
        gdf_copy.boundary.plot(ax=ax, linewidth=1, edgecolor="black")
        gdf_copy.plot(ax=ax, color=gdf_copy["Color"], alpha=0.6)
        
        title = f"{fam.title()} > {gen.title()} > {spec.lower()}"
        if isinstance(year, int):
            subtitle = f"\nYear: {year}"
            ax.set_title(title + subtitle, fontsize=15, pad=20)
        else:
            ax.set_title(title, fontsize=15, pad=20)
        ax.axis("off")
        
        # Create a separate axis for the legend
        legend_ax = fig.add_axes([0.2, 0.02, 0.6, 0.12])
        legend_ax.axis('off')
        
        # Add a box around the legend
        legend_box = self.plt.Rectangle((0, 0), 1, 1, 
                                      facecolor='white', edgecolor='black',
                                      transform=legend_ax.transAxes)
        legend_ax.add_patch(legend_box)
        
        # # Create legend title
        # legend_ax.text(0.5, 0.85, "Color Legend:", ha='center', va='center', fontsize=12)
        
        if isinstance(year, int):
            # Add horizontal bars with their descriptions for year analysis
            bar_length = 0.15
            bar_height = 0.1
            
            # Pre-year color
            legend_ax.add_patch(
                self.plt.Rectangle((0.2, 0.5), bar_length, bar_height, 
                                 facecolor=self.pre_color.get(), 
                                 alpha=0.6,
                                 edgecolor='black')
            )
            legend_ax.text(0.4, 0.55, f"Records ≤ {year}", fontsize=10, va='center')
            
            # Post-year color
            legend_ax.add_patch(
                self.plt.Rectangle((0.2, 0.2), bar_length, bar_height, 
                                 facecolor=self.post_color.get(), 
                                 alpha=0.6,
                                 edgecolor='black')
            )
            legend_ax.text(0.4, 0.25, f"Records > {year}", fontsize=10, va='center')
        else:
            # Add single bar for all records
            bar_length = 0.15
            bar_height = 0.1
            legend_ax.add_patch(
                self.plt.Rectangle((0.2, 0.35), bar_length, bar_height, 
                                 facecolor=self.all_color.get(), 
                                 alpha=0.6,
                                 edgecolor='black')
            )
            legend_ax.text(0.4, 0.4, "All Records", fontsize=10, va='center')
        
        # Set the legend axis limits
        legend_ax.set_xlim(0, 1)
        legend_ax.set_ylim(0, 1)
        
        # Adjust main plot to make room for legend
        fig.subplots_adjust(bottom=0.2, top=0.9)
        
        self.map_canvas = self.FigureCanvasTkAgg(fig, master=self.right_panel)
        self.map_canvas.draw()
        self.map_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        self.current_fig = fig
        self.download_button.config(state="normal")
        print("✅ Map generated successfully!")
    
    def download_map(self):
        if self.current_fig:
            try:
                # Get Downloads folder path
                downloads_path = str(Path.home() / "Downloads")
                
                # Get taxonomic info and year
                fam = self.selected_family.get().strip().title()
                gen = self.selected_genus.get().strip().title()
                spec = self.selected_species.get().strip().lower()
                year = self.year_var.get().strip()
                
                # Create short timestamp (just MMDD_HHMM)
                timestamp = datetime.datetime.now().strftime("%m%d_%H%M")
                
                # Create filename with taxonomic info
                year_info = f"_{year}" if year else ""
                filename = f"{fam}-{gen}-{spec}{year_info}_{timestamp}.tiff"
                
                # Full path for the file
                file_path = os.path.join(downloads_path, filename)
                
                # Save the figure
                self.current_fig.savefig(file_path, format="tiff", dpi=300)
                
                # Show toast notification
                self.toast.show_toast(f"Map saved as {filename}")
                
                print(f"✅ TIFF map saved as '{file_path}'")
                
            except Exception as e:
                messagebox.showerror("Error", 
                    f"Error saving file:\n{str(e)}\n\n"
                    "Please try again."
                )
    
    def initialize_gui(self):
        # Show the main window
        self.root.deiconify()
        self.root.title("Montana Bee County Map Generator")
        
        # Create toast notification instance
        self.toast = ToastNotification(self.root)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'))  # Increased from 16 to 24
        style.configure('Back.TButton', 
                       font=('Helvetica', 10, 'bold'),
                       padding=8)
        
        # Get screen dimensions and set window to full screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.state('zoomed')
        
        # Set minimum window size
        self.root.minsize(800, 600)
        self.root.resizable(True, True)
        
        # Calculate default restored window size (80% of screen)
        self.default_width = int(screen_width * 0.8)
        self.default_height = int(screen_height * 0.8)
        self.x_position = (screen_width - self.default_width) // 2
        self.y_position = (screen_height - self.default_height) // 2
        
        # Bind window state change
        self.root.bind("<Configure>", self.on_window_resize)
        
        # Create main container with padding
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill='both', expand=True)
        
        # Title
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill='x', pady=(0, 20))
        title_label = ttk.Label(
            title_frame, 
            text="Montana Bee County Map Generator", 
            style='Title.TLabel',
            foreground='dark green'
        )
        title_label.pack()
        
        # Create left panel for controls with scrollbar
        left_panel_container = ttk.Frame(main_container)
        left_panel_container.pack(side='left', fill='y', padx=(0, 20))
        
        # Back button at the top of left panel container (outside scroll area)
        back_button = ttk.Button(
            left_panel_container,
            text="← Back to Selection",
            command=self.go_back,
            style='Back.TButton'
        )
        back_button.pack(fill='x', pady=(0, 10))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(left_panel_container)
        scrollbar.pack(side='right', fill='y')
        
        # Create canvas for scrollable content
        self.scroll_canvas = Canvas(left_panel_container, yscrollcommand=scrollbar.set, width=300)
        self.scroll_canvas.pack(side='left', fill='y')
        
        scrollbar.config(command=self.scroll_canvas.yview)
        
        # Create frame for controls inside canvas
        left_panel = ttk.Frame(self.scroll_canvas)
        self.scroll_canvas.create_window((0, 0), window=left_panel, anchor='nw', width=self.scroll_canvas.winfo_reqwidth())
        
        # Excel Load Section
        excel_frame = ttk.LabelFrame(left_panel, text="Data Input", padding="10")
        excel_frame.pack(fill='x', pady=(0, 20))
        
        # Create a frame for the button and file info
        file_info_frame = ttk.Frame(excel_frame)
        file_info_frame.pack(fill='x', expand=True)
        
        # Load button
        load_button = ttk.Button(
            file_info_frame, 
            text="Load Excel File", 
            command=self.load_excel, 
            style='TButton'
        )
        load_button.pack(fill='x', pady=(0, 5))
        
        # File info label with smaller font and ellipsis for long names
        file_label = ttk.Label(
            file_info_frame, 
            textvariable=self.selected_file_var,
            style='FileInfo.TLabel',
            wraplength=250
        )
        file_label.pack(fill='x')
        
        # Configure style for file info
        style.configure('FileInfo.TLabel', 
                       font=('Helvetica', 9),
                       foreground='dark green')
        
        # Color Selection Section
        color_frame = ttk.LabelFrame(left_panel, text="Color Settings", padding="10")
        color_frame.pack(fill='x', pady=(0, 20))
        
        # Common color options
        color_options = ["red", "blue", "grey", "black", "yellow", "purple", "orange", "pink", "brown"]
        
        # Pre Color
        ttk.Label(color_frame, text="Pre-Year Color:", style='TLabel').pack(fill='x')
        pre_color_combo = ttk.Combobox(
            color_frame, 
            textvariable=self.pre_color, 
            values=color_options,
            state="normal"
        )
        pre_color_combo.pack(fill='x', pady=(0, 10))
        pre_color_combo.bind('<<ComboboxSelected>>', self.on_color_change)
        pre_color_combo.bind('<Return>', self.on_color_change)
        pre_color_combo.bind('<FocusOut>', self.on_color_change)
        
        # Post Color
        ttk.Label(color_frame, text="Post-Year Color:", style='TLabel').pack(fill='x')
        post_color_combo = ttk.Combobox(
            color_frame, 
            textvariable=self.post_color, 
            values=color_options,
            state="normal"
        )
        post_color_combo.pack(fill='x', pady=(0, 10))
        post_color_combo.bind('<<ComboboxSelected>>', self.on_color_change)
        post_color_combo.bind('<Return>', self.on_color_change)
        post_color_combo.bind('<FocusOut>', self.on_color_change)
        
        # All Color
        ttk.Label(color_frame, text="All Records Color:", style='TLabel').pack(fill='x')
        all_color_combo = ttk.Combobox(
            color_frame, 
            textvariable=self.all_color, 
            values=color_options,
            state="normal"
        )
        all_color_combo.pack(fill='x', pady=(0, 10))
        all_color_combo.bind('<<ComboboxSelected>>', self.on_color_change)
        all_color_combo.bind('<Return>', self.on_color_change)
        all_color_combo.bind('<FocusOut>', self.on_color_change)
        
        # Add helper text for custom colors
        helper_label = ttk.Label(
            color_frame, 
            text="Tip: You can type any valid color name or hex code (e.g., #FF5733)",
            style='TLabel',
            wraplength=250
        )
        helper_label.pack(fill='x', pady=(5, 0))
        
        # Year Input Section
        year_frame = ttk.LabelFrame(left_panel, text="Year Filter", padding="10")
        year_frame.pack(fill='x', pady=(0, 20))
        ttk.Label(year_frame, text="Year (Optional):", style='TLabel').pack(fill='x')
        ttk.Entry(year_frame, textvariable=self.year_var).pack(fill='x')
        
        # Species Selection Section
        species_frame = ttk.LabelFrame(left_panel, text="Species Selection", padding="10")
        species_frame.pack(fill='x', pady=(0, 20))
        
        # Family
        ttk.Label(species_frame, text="Family:", style='TLabel').pack(fill='x')
        self.family_dropdown = ttk.Combobox(species_frame, textvariable=self.selected_family, state="readonly")
        self.family_dropdown.pack(fill='x', pady=(0, 10))
        
        # Genus
        ttk.Label(species_frame, text="Genus:", style='TLabel').pack(fill='x')
        self.genus_dropdown = ttk.Combobox(species_frame, textvariable=self.selected_genus, state="readonly")
        self.genus_dropdown.pack(fill='x', pady=(0, 10))
        
        # Species
        ttk.Label(species_frame, text="Species:", style='TLabel').pack(fill='x')
        self.species_dropdown = ttk.Combobox(species_frame, textvariable=self.selected_species, state="readonly")
        self.species_dropdown.pack(fill='x', pady=(0, 10))
        
        # Button Section with better styling
        button_frame = ttk.Frame(left_panel)
        button_frame.pack(fill='x', pady=(0, 20))
        
        # Style configuration for buttons
        style.configure('Action.TButton', 
                       font=('Helvetica', 10, 'bold'),
                       padding=10)
        
        generate_button = ttk.Button(
            button_frame, 
            text="Generate Map", 
            command=self.generate_map, 
            style='Action.TButton'
        )
        generate_button.pack(fill='x', pady=(0, 5))
        
        self.download_button = ttk.Button(
            button_frame, 
            text="Download Map", 
            command=self.download_map, 
            state="disabled", 
            style='Action.TButton'
        )
        self.download_button.pack(fill='x', pady=(0, 5))
        
        # Create right panel for map display
        self.right_panel = ttk.Frame(main_container)
        self.right_panel.pack(side='left', fill='both', expand=True)
        
        # Configure scrolling
        def on_configure(event):
            self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox('all'))
        
        left_panel.bind('<Configure>', on_configure)
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            self.scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        self.scroll_canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Bind dropdowns
        self.family_dropdown.bind("<<ComboboxSelected>>", self.update_genus_dropdown)
        self.genus_dropdown.bind("<<ComboboxSelected>>", self.update_species_dropdown)
    
    def go_back(self):
        """Return to the selection screen"""
        self.root.destroy()
        SelectionScreen(self.root.master, self.main_app, from_analysis=True)

class SingleYearAnalysis:
    def __init__(self, parent, main_app):
        self.root = tk.Toplevel(parent)
        self.root.title("Single Year Analysis - Montana Bee County Map Generator")
        
        # Store main_app reference
        self.main_app = main_app
        
        # Get dependencies from main_app
        self.pd = main_app.pd
        self.plt = main_app.plt
        self.FigureCanvasTkAgg = main_app.FigureCanvasTkAgg
        
        # Get screen dimensions and set window to full screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.state('zoomed')
        
        # Set minimum window size
        self.root.minsize(800, 600)
        self.root.resizable(True, True)
        
        # Calculate default restored window size (80% of screen)
        self.default_width = int(screen_width * 0.8)
        self.default_height = int(screen_height * 0.8)
        self.x_position = (screen_width - self.default_width) // 2
        self.y_position = (screen_height - self.default_height) // 2
        
        # Initialize variables
        self.map_canvas = None
        self.current_fig = None
        
        # Initialize StringVar variables
        self.pre_color = StringVar(self.root)
        self.post_color = StringVar(self.root)
        self.all_color = StringVar(self.root)
        self.year_var = StringVar(self.root)
        self.selected_family = StringVar(self.root)
        self.selected_genus = StringVar(self.root)
        self.selected_species = StringVar(self.root)
        self.selected_file_var = StringVar(self.root)
        
        # Set default values
        self.pre_color.set("grey")
        self.post_color.set("red")
        self.all_color.set("yellow")
        self.selected_file_var.set("No file selected")
        
        # Create toast notification instance
        self.toast = ToastNotification(self.root)
        
        # Initialize pandas DataFrame
        self.df = self.pd.DataFrame()
        
        # Get the shapefile data from parent
        self.gdf = main_app.gdf.copy()
        
        # Initialize GUI
        self.initialize_gui()
        
        # Bind window state change
        self.root.bind("<Configure>", self.on_window_resize)
    
    def on_window_resize(self, event=None):
        if self.root.state() == 'normal':  # Only handle when window is restored (not maximized)
            # Recalculate screen center
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Ensure we maintain 80% size
            self.default_width = int(screen_width * 0.8)
            self.default_height = int(screen_height * 0.8)
            
            # Recalculate center position
            x = (screen_width - self.default_width) // 2
            y = (screen_height - self.default_height) // 2
            
            # Update window geometry
            self.root.geometry(f"{self.default_width}x{self.default_height}+{x}+{y}")
            
            # Force geometry update
            self.root.update_idletasks()
    
    def initialize_gui(self):
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'))  # Increased from 16 to 24
        style.configure('Back.TButton', 
                       font=('Helvetica', 10, 'bold'),
                       padding=8)
        
        # Create main container with padding
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill='both', expand=True)
        
        # Title
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill='x', pady=(0, 20))
        title_label = ttk.Label(
            title_frame, 
            text="Montana Bee County Map Generator", 
            style='Title.TLabel',
            foreground='dark green'
        )
        title_label.pack()
        
        # Create left panel for controls with scrollbar
        left_panel_container = ttk.Frame(main_container)
        left_panel_container.pack(side='left', fill='y', padx=(0, 20))
        
        # Back button at the top of left panel container (outside scroll area)
        back_button = ttk.Button(
            left_panel_container,
            text="← Back to Selection",
            command=self.go_back,
            style='Back.TButton'
        )
        back_button.pack(fill='x', pady=(0, 10))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(left_panel_container)
        scrollbar.pack(side='right', fill='y')
        
        # Create canvas for scrollable content
        self.scroll_canvas = Canvas(left_panel_container, yscrollcommand=scrollbar.set, width=300)
        self.scroll_canvas.pack(side='left', fill='y')
        
        scrollbar.config(command=self.scroll_canvas.yview)
        
        # Create frame for controls inside canvas
        left_panel = ttk.Frame(self.scroll_canvas)
        self.scroll_canvas.create_window((0, 0), window=left_panel, anchor='nw', width=self.scroll_canvas.winfo_reqwidth())
        
        # Excel Load Section
        excel_frame = ttk.LabelFrame(left_panel, text="Data Input", padding="10")
        excel_frame.pack(fill='x', pady=(0, 20))
        
        # Create a frame for the button and file info
        file_info_frame = ttk.Frame(excel_frame)
        file_info_frame.pack(fill='x', expand=True)
        
        # Load button
        load_button = ttk.Button(
            file_info_frame, 
            text="Load Excel File", 
            command=self.load_excel, 
            style='TButton'
        )
        load_button.pack(fill='x', pady=(0, 5))
        
        # File info label with smaller font and ellipsis for long names
        file_label = ttk.Label(
            file_info_frame, 
            textvariable=self.selected_file_var,
            style='FileInfo.TLabel',
            wraplength=250
        )
        file_label.pack(fill='x')
        
        # Configure style for file info
        style.configure('FileInfo.TLabel', 
                       font=('Helvetica', 9),
                       foreground='dark green')
        
        # Color Selection Section
        color_frame = ttk.LabelFrame(left_panel, text="Color Settings", padding="10")
        color_frame.pack(fill='x', pady=(0, 20))
        
        # Common color options
        color_options = ["red", "blue", "grey", "black", "yellow", "purple", "orange", "pink", "brown"]
        
        # Pre Color
        ttk.Label(color_frame, text="Pre-Year Color:", style='TLabel').pack(fill='x')
        pre_color_combo = ttk.Combobox(
            color_frame, 
            textvariable=self.pre_color, 
            values=color_options,
            state="normal"
        )
        pre_color_combo.pack(fill='x', pady=(0, 10))
        pre_color_combo.bind('<<ComboboxSelected>>', self.on_color_change)
        pre_color_combo.bind('<Return>', self.on_color_change)
        pre_color_combo.bind('<FocusOut>', self.on_color_change)
        
        # Post Color
        ttk.Label(color_frame, text="Post-Year Color:", style='TLabel').pack(fill='x')
        post_color_combo = ttk.Combobox(
            color_frame, 
            textvariable=self.post_color, 
            values=color_options,
            state="normal"
        )
        post_color_combo.pack(fill='x', pady=(0, 10))
        post_color_combo.bind('<<ComboboxSelected>>', self.on_color_change)
        post_color_combo.bind('<Return>', self.on_color_change)
        post_color_combo.bind('<FocusOut>', self.on_color_change)
        
        # All Color
        ttk.Label(color_frame, text="All Records Color:", style='TLabel').pack(fill='x')
        all_color_combo = ttk.Combobox(
            color_frame, 
            textvariable=self.all_color, 
            values=color_options,
            state="normal"
        )
        all_color_combo.pack(fill='x', pady=(0, 10))
        all_color_combo.bind('<<ComboboxSelected>>', self.on_color_change)
        all_color_combo.bind('<Return>', self.on_color_change)
        all_color_combo.bind('<FocusOut>', self.on_color_change)
        
        # Add helper text for custom colors
        helper_label = ttk.Label(
            color_frame, 
            text="Tip: You can type any valid color name or hex code (e.g., #FF5733)",
            style='TLabel',
            wraplength=250
        )
        helper_label.pack(fill='x', pady=(5, 0))
        
        # Year Input Section
        year_frame = ttk.LabelFrame(left_panel, text="Year Filter", padding="10")
        year_frame.pack(fill='x', pady=(0, 20))
        ttk.Label(year_frame, text="Year (Optional):", style='TLabel').pack(fill='x')
        ttk.Entry(year_frame, textvariable=self.year_var).pack(fill='x')
        
        # Species Selection Section
        species_frame = ttk.LabelFrame(left_panel, text="Species Selection", padding="10")
        species_frame.pack(fill='x', pady=(0, 20))
        
        # Family
        ttk.Label(species_frame, text="Family:", style='TLabel').pack(fill='x')
        self.family_dropdown = ttk.Combobox(species_frame, textvariable=self.selected_family, state="readonly")
        self.family_dropdown.pack(fill='x', pady=(0, 10))
        
        # Genus
        ttk.Label(species_frame, text="Genus:", style='TLabel').pack(fill='x')
        self.genus_dropdown = ttk.Combobox(species_frame, textvariable=self.selected_genus, state="readonly")
        self.genus_dropdown.pack(fill='x', pady=(0, 10))
        
        # Species
        ttk.Label(species_frame, text="Species:", style='TLabel').pack(fill='x')
        self.species_dropdown = ttk.Combobox(species_frame, textvariable=self.selected_species, state="readonly")
        self.species_dropdown.pack(fill='x', pady=(0, 10))
        
        # Button Section with better styling
        button_frame = ttk.Frame(left_panel)
        button_frame.pack(fill='x', pady=(0, 20))
        
        # Style configuration for buttons
        style.configure('Action.TButton', 
                       font=('Helvetica', 10, 'bold'),
                       padding=10)
        
        generate_button = ttk.Button(
            button_frame, 
            text="Generate Map", 
            command=self.generate_map, 
            style='Action.TButton'
        )
        generate_button.pack(fill='x', pady=(0, 5))
        
        self.download_button = ttk.Button(
            button_frame, 
            text="Download Map", 
            command=self.download_map, 
            state="disabled", 
            style='Action.TButton'
        )
        self.download_button.pack(fill='x', pady=(0, 5))
        
        # Create right panel for map display
        self.right_panel = ttk.Frame(main_container)
        self.right_panel.pack(side='left', fill='both', expand=True)
        
        # Configure scrolling
        def on_configure(event):
            self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox('all'))
        
        left_panel.bind('<Configure>', on_configure)
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            self.scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        self.scroll_canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Bind dropdowns
        self.family_dropdown.bind("<<ComboboxSelected>>", self.update_genus_dropdown)
        self.genus_dropdown.bind("<<ComboboxSelected>>", self.update_species_dropdown)
    
    def go_back(self):
        """Return to the selection screen"""
        self.root.destroy()
        SelectionScreen(self.root.master, self.main_app, from_analysis=True)
    
    def load_excel(self):
        path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if not path:
            return
        
        # Show loading dialog
        loading_window = tk.Tk()
        loading_window.title("Loading")
        screen_width = loading_window.winfo_screenwidth()
        screen_height = loading_window.winfo_screenheight()
        window_width = 300
        window_height = 100
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        loading_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        loading_window.overrideredirect(True)
        
        frame = ttk.Frame(loading_window, padding="20", relief="raised")
        frame.pack(fill='both', expand=True)
        
        loading_label = ttk.Label(frame, text="Loading file...\nPlease wait", font=('Helvetica', 10))
        loading_label.pack(pady=10)
        
        progress = ttk.Progressbar(frame, mode='indeterminate')
        progress.pack(fill='x', pady=5)
        progress.start(10)
        
        loading_window.update()
        
        try:
            # Load the Excel file
            self.df = self.pd.read_excel(path, sheet_name=0)
            self.df.columns = self.df.columns.str.strip()
            
            # Get just the filename from the path
            filename = path.split('/')[-1]
            
            # Validate required columns
            required_columns = ["county", "family", "genus", "species", "year"]
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            
            if missing_columns:
                progress.stop()
                loading_window.destroy()
                self.selected_file_var.set("No file selected")
                messagebox.showerror("Error", 
                    f"Missing required columns: {', '.join(missing_columns)}\n\n"
                    "The following columns are required:\n"
                    "- county: for mapping locations\n"
                    "- family: for taxonomic classification\n"
                    "- genus: for taxonomic classification\n"
                    "- species: for taxonomic classification\n"
                    "- year: for temporal analysis\n\n"
                    "Please check your Excel file and try again."
                )
                return
            
            # Process the data
            for col in required_columns:
                self.df[col] = self.df[col].astype(str).str.strip().str.lower()
            self.df["year"] = self.df["year"].astype(str).str.extract(r'(\d{4})').astype(float)
            
            # Calculate statistics
            num_records = len(self.df)
            num_families = len(self.df["family"].unique())
            num_genera = len(self.df["genus"].unique())
            num_species = len(self.df["species"].unique())
            year_range = f"{int(self.df['year'].min())} - {int(self.df['year'].max())}"
            num_counties = len(self.df["county"].unique())
            
            # Update Family dropdown with capitalized values
            family_values = sorted(self.df["family"].dropna().unique())
            family_values = [f.title() for f in family_values]
            self.family_dropdown["values"] = family_values
            self.family_dropdown.set("Select Family")
            
            # Reset other dropdowns and fields
            self.genus_dropdown.set("Select Genus")
            self.genus_dropdown["values"] = []
            self.species_dropdown.set("Select Species")
            self.species_dropdown["values"] = []
            self.year_var.set("")
            
            # Update file info display
            self.selected_file_var.set(f"✓ {filename}\n{num_records:,} records loaded")
            
            # Stop progress bar and close loading window
            progress.stop()
            loading_window.destroy()
            
            # Show success message with detailed statistics
            messagebox.showinfo("Success", 
                f"File loaded successfully!\n\n"
                f"Dataset Summary:\n"
                f"• Total Records: {num_records:,}\n"
                f"• Unique Families: {num_families}\n"
                f"• Unique Genera: {num_genera}\n"
                f"• Unique Species: {num_species}\n"
                f"• Counties Covered: {num_counties}\n"
                f"• Year Range: {year_range}\n\n"
                "Please select a Family to continue."
            )
            
            print("✅ Excel file loaded successfully!")
            
        except Exception as e:
            progress.stop()
            loading_window.destroy()
            self.selected_file_var.set("No file selected")
            error_message = str(e)
            if "No sheet named" in error_message:
                error_message = "Invalid Excel file format. Please ensure your data is in the first sheet."
            elif "Invalid file" in error_message:
                error_message = "Invalid file format. Please ensure you're uploading a valid Excel (.xlsx) file."
            
            messagebox.showerror("Error", 
                f"Error loading file:\n{error_message}\n\n"
                "Please check your Excel file format and try again."
            )
            return
    
    def update_genus_dropdown(self, event=None):
        family = self.selected_family.get().strip().lower()
        filtered = self.df[self.df["family"] == family]
        # Capitalize genus names for display
        genus_values = sorted(filtered["genus"].dropna().unique())
        genus_values = [g.title() for g in genus_values]  # Capitalize genus names
        self.genus_dropdown["values"] = genus_values
        self.genus_dropdown.set("Select Genus")
    
    def update_species_dropdown(self, event=None):
        family = self.selected_family.get().strip().lower()
        genus = self.selected_genus.get().strip().lower()
        filtered = self.df[(self.df["family"] == family) & (self.df["genus"] == genus)]
        self.species_dropdown["values"] = sorted(filtered["species"].dropna().unique())
        self.species_dropdown.set("Select Species")
    
    def is_valid_color(self, color):
        """Validate if a color string is a valid matplotlib color"""
        try:
            # Convert color to RGB
            self.plt.matplotlib.colors.to_rgb(color)
            return True
        except ValueError:
            return False

    def validate_colors(self):
        """Validate all selected colors"""
        colors = {
            'Pre-Year': self.pre_color.get(),
            'Post-Year': self.post_color.get(),
            'All Records': self.all_color.get()
        }
        
        invalid_colors = []
        for name, color in colors.items():
            if not self.is_valid_color(color):
                invalid_colors.append(f"{name} color '{color}'")
        
        if invalid_colors:
            error_msg = "Invalid colors detected:\n" + "\n".join(invalid_colors)
            self.toast.show_toast(error_msg, duration=5000, error=True)
            return False
        return True

    def on_color_change(self, event=None):
        """Validate colors when they change"""
        self.validate_colors()

    def generate_map(self):
        if self.map_canvas:
            self.map_canvas.get_tk_widget().destroy()
        
        # Validate colors first
        if not self.validate_colors():
            self.download_button.config(state="disabled")
            return
        
        gdf_copy = self.gdf.copy()
        # Initialize all counties as white
        gdf_copy["Color"] = "white"
        
        fam = self.selected_family.get().strip().lower()
        gen = self.selected_genus.get().strip().lower()
        spec = self.selected_species.get().strip().lower()
        year = self.year_var.get().strip()
        
        if not fam or not gen or not spec:
            messagebox.showerror("Missing Input", "Please select Family, Genus, and Species.")
            self.download_button.config(state="disabled")
            return
        
        filtered = self.df[(self.df["family"] == fam) & (self.df["genus"] == gen) & (self.df["species"] == spec)]
        
        if isinstance(year, str) and year.isdigit():
            year = int(year)
            # First pass: Mark counties with post-dividing year records with post_color (only if they're white)
            for county in filtered[filtered["year"] > year]["county"].unique():
                if gdf_copy.loc[gdf_copy["County"] == county, "Color"].iloc[0] == "white":
                    gdf_copy.loc[gdf_copy["County"] == county, "Color"] = self.post_color.get()
            
            # Second pass: Mark counties with pre-dividing year records with pre_color (overriding any color)
            for county in filtered[filtered["year"] <= year]["county"].unique():
                gdf_copy.loc[gdf_copy["County"] == county, "Color"] = self.pre_color.get()
        else:
            # If no year specified, mark all counties with records using all_color
            for county in filtered["county"].unique():
                gdf_copy.loc[gdf_copy["County"] == county, "Color"] = self.all_color.get()
        
        # Create figure with larger size and better proportions
        fig, ax = self.plt.subplots(figsize=(12, 11))
        gdf_copy.boundary.plot(ax=ax, linewidth=1, edgecolor="black")
        gdf_copy.plot(ax=ax, color=gdf_copy["Color"], alpha=0.6)
        
        title = f"{fam.title()} > {gen.title()} > {spec.lower()}"
        if isinstance(year, int):
            subtitle = f"\nYear: {year}"
            ax.set_title(title + subtitle, fontsize=15, pad=20)
        else:
            ax.set_title(title, fontsize=15, pad=20)
        ax.axis("off")
        
        # Create a separate axis for the legend
        legend_ax = fig.add_axes([0.2, 0.02, 0.6, 0.12])
        legend_ax.axis('off')
        
        # Add a box around the legend
        legend_box = self.plt.Rectangle((0, 0), 1, 1, 
                                      facecolor='white', edgecolor='black',
                                      transform=legend_ax.transAxes)
        legend_ax.add_patch(legend_box)
        
        # # Create legend title
        # legend_ax.text(0.5, 0.85, "Color Legend:", ha='center', va='center', fontsize=12)
        
        if isinstance(year, int):
            # Add horizontal bars with their descriptions for year analysis
            bar_length = 0.15
            bar_height = 0.1
            
            # Pre-year color
            legend_ax.add_patch(
                self.plt.Rectangle((0.2, 0.5), bar_length, bar_height, 
                                 facecolor=self.pre_color.get(), 
                                 alpha=0.6,
                                 edgecolor='black')
            )
            legend_ax.text(0.4, 0.55, f"Records ≤ {year}", fontsize=10, va='center')
            
            # Post-year color
            legend_ax.add_patch(
                self.plt.Rectangle((0.2, 0.2), bar_length, bar_height, 
                                 facecolor=self.post_color.get(), 
                                 alpha=0.6,
                                 edgecolor='black')
            )
            legend_ax.text(0.4, 0.25, f"Records > {year}", fontsize=10, va='center')
        else:
            # Add single bar for all records
            bar_length = 0.15
            bar_height = 0.1
            legend_ax.add_patch(
                self.plt.Rectangle((0.2, 0.35), bar_length, bar_height, 
                                 facecolor=self.all_color.get(), 
                                 alpha=0.6,
                                 edgecolor='black')
            )
            legend_ax.text(0.4, 0.4, "All Records", fontsize=10, va='center')
        
        # Set the legend axis limits
        legend_ax.set_xlim(0, 1)
        legend_ax.set_ylim(0, 1)
        
        # Adjust main plot to make room for legend
        fig.subplots_adjust(bottom=0.2, top=0.9)
        
        self.map_canvas = self.FigureCanvasTkAgg(fig, master=self.right_panel)
        self.map_canvas.draw()
        self.map_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        self.current_fig = fig
        self.download_button.config(state="normal")
        print("✅ Map generated successfully!")
    
    def download_map(self):
        if self.current_fig:
            try:
                # Get Downloads folder path
                downloads_path = str(Path.home() / "Downloads")
                
                # Get taxonomic info and year
                fam = self.selected_family.get().strip().title()
                gen = self.selected_genus.get().strip().title()
                spec = self.selected_species.get().strip().lower()
                year = self.year_var.get().strip()
                
                # Create short timestamp (just MMDD_HHMM)
                timestamp = datetime.datetime.now().strftime("%m%d_%H%M")
                
                # Create filename with taxonomic info
                year_info = f"_{year}" if year else ""
                filename = f"{fam}-{gen}-{spec}{year_info}_{timestamp}.tiff"
                
                # Full path for the file
                file_path = os.path.join(downloads_path, filename)
                
                # Save the figure
                self.current_fig.savefig(file_path, format="tiff", dpi=300)
                
                # Show toast notification
                self.toast.show_toast(f"Map saved as {filename}")
                
                print(f"✅ TIFF map saved as '{file_path}'")
                
            except Exception as e:
                messagebox.showerror("Error", 
                    f"Error saving file:\n{str(e)}\n\n"
                    "Please try again."
                )
    
    def on_window_resize(self, event=None):
        if self.root.state() == 'normal':  # Only handle when window is restored (not maximized)
            # Recalculate screen center
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Ensure we maintain 80% size
            self.default_width = int(screen_width * 0.8)
            self.default_height = int(screen_height * 0.8)
            
            # Recalculate center position
            x = (screen_width - self.default_width) // 2
            y = (screen_height - self.default_height) // 2
            
            # Update window geometry
            self.root.geometry(f"{self.default_width}x{self.default_height}+{x}+{y}")
            
            # Force geometry update
            self.root.update_idletasks()

class DualYearAnalysis:
    def __init__(self, parent, main_app):
        self.root = tk.Toplevel(parent)
        self.root.title("Dual Year Analysis - Montana Bee County Map Generator")
        
        # Store main_app reference
        self.main_app = main_app
        
        # Get dependencies from main_app
        self.pd = main_app.pd
        self.plt = main_app.plt
        self.FigureCanvasTkAgg = main_app.FigureCanvasTkAgg
        
        # Get screen dimensions and set window to full screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.state('zoomed')
        
        # Set minimum window size
        self.root.minsize(800, 600)
        self.root.resizable(True, True)
        
        # Calculate default restored window size (80% of screen)
        self.default_width = int(screen_width * 0.8)
        self.default_height = int(screen_height * 0.8)
        self.x_position = (screen_width - self.default_width) // 2
        self.y_position = (screen_height - self.default_height) // 2
        
        # Initialize variables
        self.map_canvas = None
        self.current_fig = None
        
        # Initialize StringVar variables
        self.first_color = StringVar(self.root)
        self.second_color = StringVar(self.root)
        self.third_color = StringVar(self.root)
        self.first_year_var = StringVar(self.root)
        self.second_year_var = StringVar(self.root)
        self.selected_family = StringVar(self.root)
        self.selected_genus = StringVar(self.root)
        self.selected_species = StringVar(self.root)
        self.selected_file_var = StringVar(self.root)
        
        # Set default values
        self.first_color.set("grey")  # For records ≤ first year
        self.second_color.set("red")  # For records between years
        self.third_color.set("yellow")  # For records > second year
        self.selected_file_var.set("No file selected")
        
        # Create toast notification instance
        self.toast = ToastNotification(self.root)
        
        # Initialize pandas DataFrame
        self.df = self.pd.DataFrame()
        
        # Get the shapefile data from parent
        self.gdf = main_app.gdf.copy()
        
        # Initialize GUI
        self.initialize_gui()
        
        # Bind window state change
        self.root.bind("<Configure>", self.on_window_resize)
    
    def on_window_resize(self, event=None):
        if self.root.state() == 'normal':  # Only handle when window is restored (not maximized)
            # Recalculate screen center
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Ensure we maintain 80% size
            self.default_width = int(screen_width * 0.8)
            self.default_height = int(screen_height * 0.8)
            
            # Recalculate center position
            x = (screen_width - self.default_width) // 2
            y = (screen_height - self.default_height) // 2
            
            # Update window geometry
            self.root.geometry(f"{self.default_width}x{self.default_height}+{x}+{y}")
            
            # Force geometry update
            self.root.update_idletasks()
    
    def initialize_gui(self):
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'))  # Increased from 16 to 24
        style.configure('Back.TButton', 
                       font=('Helvetica', 10, 'bold'),
                       padding=8)
        
        # Create main container with padding
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill='both', expand=True)
        
        # Title
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill='x', pady=(0, 20))
        title_label = ttk.Label(
            title_frame, 
            text="Montana Bee County Map Generator - Dual Year Analysis", 
            style='Title.TLabel',
            foreground='dark green'
        )
        title_label.pack()
        
        # Create left panel for controls with scrollbar
        left_panel_container = ttk.Frame(main_container)
        left_panel_container.pack(side='left', fill='y', padx=(0, 20))
        
        # Back button at the top of left panel container (outside scroll area)
        back_button = ttk.Button(
            left_panel_container,
            text="← Back to Selection",
            command=self.go_back,
            style='Back.TButton'
        )
        back_button.pack(fill='x', pady=(0, 10))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(left_panel_container)
        scrollbar.pack(side='right', fill='y')
        
        # Create canvas for scrollable content
        self.scroll_canvas = Canvas(left_panel_container, yscrollcommand=scrollbar.set, width=300)
        self.scroll_canvas.pack(side='left', fill='y')
        
        scrollbar.config(command=self.scroll_canvas.yview)
        
        # Create frame for controls inside canvas
        left_panel = ttk.Frame(self.scroll_canvas)
        self.scroll_canvas.create_window((0, 0), window=left_panel, anchor='nw', width=self.scroll_canvas.winfo_reqwidth())
        
        # Excel Load Section
        excel_frame = ttk.LabelFrame(left_panel, text="Data Input", padding="10")
        excel_frame.pack(fill='x', pady=(0, 20))
        
        # Create a frame for the button and file info
        file_info_frame = ttk.Frame(excel_frame)
        file_info_frame.pack(fill='x', expand=True)
        
        # Load button
        load_button = ttk.Button(
            file_info_frame, 
            text="Load Excel File", 
            command=self.load_excel, 
            style='TButton'
        )
        load_button.pack(fill='x', pady=(0, 5))
        
        # File info label
        file_label = ttk.Label(
            file_info_frame, 
            textvariable=self.selected_file_var,
            style='FileInfo.TLabel',
            wraplength=250
        )
        file_label.pack(fill='x')
        
        # Configure style for file info
        style.configure('FileInfo.TLabel', 
                       font=('Helvetica', 9),
                       foreground='dark green')
        
        # Color Selection Section
        color_frame = ttk.LabelFrame(left_panel, text="Color Settings", padding="10")
        color_frame.pack(fill='x', pady=(0, 20))
        
        # Common color options
        color_options = ["red", "blue", "grey", "black", "yellow", "purple", "orange", "pink", "brown"]
        
        # First Color (Highest Priority)
        ttk.Label(color_frame, text="First Period Color (Highest Priority):", style='TLabel').pack(fill='x')
        first_color_combo = ttk.Combobox(
            color_frame, 
            textvariable=self.first_color, 
            values=color_options,
            state="normal"
        )
        first_color_combo.pack(fill='x', pady=(0, 10))
        first_color_combo.bind('<<ComboboxSelected>>', self.on_color_change)
        first_color_combo.bind('<Return>', self.on_color_change)
        first_color_combo.bind('<FocusOut>', self.on_color_change)
        
        # Second Color (Medium Priority)
        ttk.Label(color_frame, text="Second Period Color (Medium Priority):", style='TLabel').pack(fill='x')
        second_color_combo = ttk.Combobox(
            color_frame, 
            textvariable=self.second_color, 
            values=color_options,
            state="normal"
        )
        second_color_combo.pack(fill='x', pady=(0, 10))
        second_color_combo.bind('<<ComboboxSelected>>', self.on_color_change)
        second_color_combo.bind('<Return>', self.on_color_change)
        second_color_combo.bind('<FocusOut>', self.on_color_change)
        
        # Third Color (Lowest Priority)
        ttk.Label(color_frame, text="Third Period Color (Lowest Priority):", style='TLabel').pack(fill='x')
        third_color_combo = ttk.Combobox(
            color_frame, 
            textvariable=self.third_color, 
            values=color_options,
            state="normal"
        )
        third_color_combo.pack(fill='x', pady=(0, 10))
        third_color_combo.bind('<<ComboboxSelected>>', self.on_color_change)
        third_color_combo.bind('<Return>', self.on_color_change)
        third_color_combo.bind('<FocusOut>', self.on_color_change)
        
        # Add helper text for custom colors
        helper_label = ttk.Label(
            color_frame, 
            text="Tip: You can type any valid color name or hex code (e.g., #FF5733)",
            style='TLabel',
            wraplength=250
        )
        helper_label.pack(fill='x', pady=(5, 0))
        
        # Year Input Section
        year_frame = ttk.LabelFrame(left_panel, text="Year Filters", padding="10")
        year_frame.pack(fill='x', pady=(0, 20))
        
        # First Year (Required)
        ttk.Label(year_frame, text="First Year (Required):", style='TLabel').pack(fill='x')
        ttk.Entry(year_frame, textvariable=self.first_year_var).pack(fill='x', pady=(0, 10))
        
        # Second Year (Required)
        ttk.Label(year_frame, text="Second Year (Required):", style='TLabel').pack(fill='x')
        ttk.Entry(year_frame, textvariable=self.second_year_var).pack(fill='x')
        
        # Add helper text for years
        year_helper = ttk.Label(
            year_frame,
            text="Note: Records will be colored based on:\n" +
                 "• First color: Records ≤ First Year\n" +
                 "• Second color: Records between years\n" +
                 "• Third color: Records > Second Year",
            style='TLabel',
            wraplength=250
        )
        year_helper.pack(fill='x', pady=(10, 0))
        
        # Species Selection Section
        species_frame = ttk.LabelFrame(left_panel, text="Species Selection", padding="10")
        species_frame.pack(fill='x', pady=(0, 20))
        
        # Family
        ttk.Label(species_frame, text="Family:", style='TLabel').pack(fill='x')
        self.family_dropdown = ttk.Combobox(species_frame, textvariable=self.selected_family, state="readonly")
        self.family_dropdown.pack(fill='x', pady=(0, 10))
        
        # Genus
        ttk.Label(species_frame, text="Genus:", style='TLabel').pack(fill='x')
        self.genus_dropdown = ttk.Combobox(species_frame, textvariable=self.selected_genus, state="readonly")
        self.genus_dropdown.pack(fill='x', pady=(0, 10))
        
        # Species
        ttk.Label(species_frame, text="Species:", style='TLabel').pack(fill='x')
        self.species_dropdown = ttk.Combobox(species_frame, textvariable=self.selected_species, state="readonly")
        self.species_dropdown.pack(fill='x', pady=(0, 10))
        
        # Button Section
        button_frame = ttk.Frame(left_panel)
        button_frame.pack(fill='x', pady=(0, 20))
        
        # Style configuration for buttons
        style.configure('Action.TButton', 
                       font=('Helvetica', 10, 'bold'),
                       padding=10)
        
        generate_button = ttk.Button(
            button_frame, 
            text="Generate Map", 
            command=self.generate_map, 
            style='Action.TButton'
        )
        generate_button.pack(fill='x', pady=(0, 5))
        
        self.download_button = ttk.Button(
            button_frame, 
            text="Download Map", 
            command=self.download_map, 
            state="disabled", 
            style='Action.TButton'
        )
        self.download_button.pack(fill='x', pady=(0, 5))
        
        # Create right panel for map display
        self.right_panel = ttk.Frame(main_container)
        self.right_panel.pack(side='left', fill='both', expand=True)
        
        # Configure scrolling
        def on_configure(event):
            self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox('all'))
        
        left_panel.bind('<Configure>', on_configure)
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            self.scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        self.scroll_canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Bind dropdowns
        self.family_dropdown.bind("<<ComboboxSelected>>", self.update_genus_dropdown)
        self.genus_dropdown.bind("<<ComboboxSelected>>", self.update_species_dropdown)
    
    def go_back(self):
        """Return to the selection screen"""
        self.root.destroy()
        SelectionScreen(self.root.master, self.main_app, from_analysis=True)
    
    def load_excel(self):
        path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if not path:
            return
        
        # Show loading dialog
        loading_window = tk.Tk()
        loading_window.title("Loading")
        screen_width = loading_window.winfo_screenwidth()
        screen_height = loading_window.winfo_screenheight()
        window_width = 300
        window_height = 100
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        loading_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        loading_window.overrideredirect(True)
        
        frame = ttk.Frame(loading_window, padding="20", relief="raised")
        frame.pack(fill='both', expand=True)
        
        loading_label = ttk.Label(frame, text="Loading file...\nPlease wait", font=('Helvetica', 10))
        loading_label.pack(pady=10)
        
        progress = ttk.Progressbar(frame, mode='indeterminate')
        progress.pack(fill='x', pady=5)
        progress.start(10)
        
        loading_window.update()
        
        try:
            # Load the Excel file
            self.df = self.pd.read_excel(path, sheet_name=0)
            self.df.columns = self.df.columns.str.strip()
            
            # Get just the filename from the path
            filename = path.split('/')[-1]
            
            # Validate required columns
            required_columns = ["county", "family", "genus", "species", "year"]
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            
            if missing_columns:
                progress.stop()
                loading_window.destroy()
                self.selected_file_var.set("No file selected")
                messagebox.showerror("Error", 
                    f"Missing required columns: {', '.join(missing_columns)}\n\n"
                    "The following columns are required:\n"
                    "- county: for mapping locations\n"
                    "- family: for taxonomic classification\n"
                    "- genus: for taxonomic classification\n"
                    "- species: for taxonomic classification\n"
                    "- year: for temporal analysis\n\n"
                    "Please check your Excel file and try again."
                )
                return
            
            # Process the data
            for col in required_columns:
                self.df[col] = self.df[col].astype(str).str.strip().str.lower()
            self.df["year"] = self.df["year"].astype(str).str.extract(r'(\d{4})').astype(float)
            
            # Calculate statistics
            num_records = len(self.df)
            num_families = len(self.df["family"].unique())
            num_genera = len(self.df["genus"].unique())
            num_species = len(self.df["species"].unique())
            year_range = f"{int(self.df['year'].min())} - {int(self.df['year'].max())}"
            num_counties = len(self.df["county"].unique())
            
            # Update Family dropdown with capitalized values
            family_values = sorted(self.df["family"].dropna().unique())
            family_values = [f.title() for f in family_values]
            self.family_dropdown["values"] = family_values
            self.family_dropdown.set("Select Family")
            
            # Reset other dropdowns and fields
            self.genus_dropdown.set("Select Genus")
            self.genus_dropdown["values"] = []
            self.species_dropdown.set("Select Species")
            self.species_dropdown["values"] = []
            self.first_year_var.set("")
            self.second_year_var.set("")
            
            # Update file info display
            self.selected_file_var.set(f"✓ {filename}\n{num_records:,} records loaded")
            
            # Stop progress bar and close loading window
            progress.stop()
            loading_window.destroy()
            
            # Show success message with detailed statistics
            messagebox.showinfo("Success", 
                f"File loaded successfully!\n\n"
                f"Dataset Summary:\n"
                f"• Total Records: {num_records:,}\n"
                f"• Unique Families: {num_families}\n"
                f"• Unique Genera: {num_genera}\n"
                f"• Unique Species: {num_species}\n"
                f"• Counties Covered: {num_counties}\n"
                f"• Year Range: {year_range}\n\n"
                "Please select a Family to continue."
            )
            
            print("✅ Excel file loaded successfully!")
            
        except Exception as e:
            progress.stop()
            loading_window.destroy()
            self.selected_file_var.set("No file selected")
            error_message = str(e)
            if "No sheet named" in error_message:
                error_message = "Invalid Excel file format. Please ensure your data is in the first sheet."
            elif "Invalid file" in error_message:
                error_message = "Invalid file format. Please ensure you're uploading a valid Excel (.xlsx) file."
            
            messagebox.showerror("Error", 
                f"Error loading file:\n{error_message}\n\n"
                "Please check your Excel file format and try again."
            )
            return
    
    def update_genus_dropdown(self, event=None):
        family = self.selected_family.get().strip().lower()
        filtered = self.df[self.df["family"] == family]
        # Capitalize genus names for display
        genus_values = sorted(filtered["genus"].dropna().unique())
        genus_values = [g.title() for g in genus_values]
        self.genus_dropdown["values"] = genus_values
        self.genus_dropdown.set("Select Genus")
    
    def update_species_dropdown(self, event=None):
        family = self.selected_family.get().strip().lower()
        genus = self.selected_genus.get().strip().lower()
        filtered = self.df[(self.df["family"] == family) & (self.df["genus"] == genus)]
        self.species_dropdown["values"] = sorted(filtered["species"].dropna().unique())
        self.species_dropdown.set("Select Species")
    
    def is_valid_color(self, color):
        """Validate if a color string is a valid matplotlib color"""
        try:
            # Convert color to RGB
            self.plt.matplotlib.colors.to_rgb(color)
            return True
        except ValueError:
            return False

    def validate_colors(self):
        """Validate all selected colors"""
        colors = {
            'First Period': self.first_color.get(),
            'Second Period': self.second_color.get(),
            'Third Period': self.third_color.get()
        }
        
        invalid_colors = []
        for name, color in colors.items():
            if not self.is_valid_color(color):
                invalid_colors.append(f"{name} color '{color}'")
        
        if invalid_colors:
            error_msg = "Invalid colors detected:\n" + "\n".join(invalid_colors)
            self.toast.show_toast(error_msg, duration=5000, error=True)
            return False
        return True

    def validate_years(self):
        """Validate that both years are provided and first year is less than second year"""
        try:
            first_year = int(self.first_year_var.get().strip())
            second_year = int(self.second_year_var.get().strip())
            
            if first_year >= second_year:
                messagebox.showerror("Invalid Years", 
                    "First year must be less than second year.\n\n"
                    f"You entered:\n"
                    f"First Year: {first_year}\n"
                    f"Second Year: {second_year}"
                )
                return False
            return True
        except ValueError:
            messagebox.showerror("Invalid Years",
                "Both years are required and must be valid numbers.\n\n"
                "Please enter valid years (e.g., 1990, 2000)"
            )
            return False

    def on_color_change(self, event=None):
        """Validate colors when they change"""
        self.validate_colors()

    def generate_map(self):
        if self.map_canvas:
            self.map_canvas.get_tk_widget().destroy()
        
        # Validate colors first
        if not self.validate_colors():
            self.download_button.config(state="disabled")
            return
        
        # Validate years
        if not self.validate_years():
            self.download_button.config(state="disabled")
            return
        
        gdf_copy = self.gdf.copy()
        # Initialize all counties as white
        gdf_copy["Color"] = "white"
        
        fam = self.selected_family.get().strip().lower()
        gen = self.selected_genus.get().strip().lower()
        spec = self.selected_species.get().strip().lower()
        first_year = int(self.first_year_var.get().strip())
        second_year = int(self.second_year_var.get().strip())
        
        if not fam or not gen or not spec:
            messagebox.showerror("Missing Input", "Please select Family, Genus, and Species.")
            self.download_button.config(state="disabled")
            return
        
        filtered = self.df[(self.df["family"] == fam) & (self.df["genus"] == gen) & (self.df["species"] == spec)]
        
        # Apply colors with priority:
        # 1. First color (highest priority)
        # 2. Second color (medium priority)
        # 3. Third color (lowest priority)
        
        # Third pass (lowest priority): Mark counties with records after second year
        for county in filtered[filtered["year"] > second_year]["county"].unique():
            if gdf_copy.loc[gdf_copy["County"] == county, "Color"].iloc[0] == "white":
                gdf_copy.loc[gdf_copy["County"] == county, "Color"] = self.third_color.get()
        
        # Second pass (medium priority): Mark counties with records between years
        for county in filtered[(filtered["year"] > first_year) & (filtered["year"] <= second_year)]["county"].unique():
            if gdf_copy.loc[gdf_copy["County"] == county, "Color"].iloc[0] == "white":
                gdf_copy.loc[gdf_copy["County"] == county, "Color"] = self.second_color.get()
        
        # First pass (highest priority): Mark counties with records before or equal to first year
        for county in filtered[filtered["year"] <= first_year]["county"].unique():
            gdf_copy.loc[gdf_copy["County"] == county, "Color"] = self.first_color.get()
        
        # Create figure with larger size and better proportions
        fig, ax = self.plt.subplots(figsize=(12, 11))  # Increased from (10, 10) to (12, 11)
        gdf_copy.boundary.plot(ax=ax, linewidth=1, edgecolor="black")
        gdf_copy.plot(ax=ax, color=gdf_copy["Color"], alpha=0.6)
        
        title = f"{fam.title()} > {gen.title()} > {spec.lower()}"
        subtitle = f"\nYears: {first_year} - {second_year}"
        ax.set_title(title + subtitle, fontsize=15, pad=20)  # Added pad to adjust title spacing
        ax.axis("off")
        
        # Create a separate axis for the legend with adjusted position
        legend_ax = fig.add_axes([0.2, 0.02, 0.6, 0.12])  # Adjusted height from 0.15 to 0.12
        legend_ax.axis('off')
        
        # Add a box around the legend
        legend_box = self.plt.Rectangle((0, 0), 1, 1, 
                                      facecolor='white', edgecolor='black',
                                      transform=legend_ax.transAxes)
        legend_ax.add_patch(legend_box)
        
        # # Create legend title
        # legend_ax.text(0.5, 0.85, "Color Legend:", ha='center', va='center', fontsize=12)
        
        # Add horizontal bars with their descriptions
        bar_length = 0.15
        bar_height = 0.1
        
        # First color (highest priority)
        legend_ax.add_patch(
            self.plt.Rectangle((0.2, 0.6), bar_length, bar_height, 
                             facecolor=self.first_color.get(), 
                             alpha=0.6,
                             edgecolor='black')
        )
        legend_ax.text(0.4, 0.65, f"Records ≤ {first_year}", fontsize=10, va='center')
        
        # Second color (medium priority)
        legend_ax.add_patch(
            self.plt.Rectangle((0.2, 0.4), bar_length, bar_height, 
                             facecolor=self.second_color.get(), 
                             alpha=0.6,
                             edgecolor='black')
        )
        legend_ax.text(0.4, 0.45, f"Records between {first_year} and {second_year}", fontsize=10, va='center')
        
        # Third color (lowest priority)
        legend_ax.add_patch(
            self.plt.Rectangle((0.2, 0.2), bar_length, bar_height, 
                             facecolor=self.third_color.get(), 
                             alpha=0.6,
                             edgecolor='black')
        )
        legend_ax.text(0.4, 0.25, f"Records > {second_year}", fontsize=10, va='center')
        
        # Set the legend axis limits
        legend_ax.set_xlim(0, 1)
        legend_ax.set_ylim(0, 1)
        
        # Adjust main plot to make room for legend - reduced bottom margin
        fig.subplots_adjust(bottom=0.2, top=0.9)  # Adjusted from bottom=0.3 to 0.2
        
        self.map_canvas = self.FigureCanvasTkAgg(fig, master=self.right_panel)
        self.map_canvas.draw()
        self.map_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        self.current_fig = fig
        self.download_button.config(state="normal")
        print("✅ Map generated successfully!")
    
    def download_map(self):
        if self.current_fig:
            try:
                # Get Downloads folder path
                downloads_path = str(Path.home() / "Downloads")
                
                # Get taxonomic info and years
                fam = self.selected_family.get().strip().title()
                gen = self.selected_genus.get().strip().title()
                spec = self.selected_species.get().strip().lower()
                first_year = self.first_year_var.get().strip()
                second_year = self.second_year_var.get().strip()
                
                # Create short timestamp (just MMDD_HHMM)
                timestamp = datetime.datetime.now().strftime("%m%d_%H%M")
                
                # Create filename with taxonomic info
                filename = f"{fam}-{gen}-{spec}_{first_year}-{second_year}_{timestamp}.tiff"
                
                # Full path for the file
                file_path = os.path.join(downloads_path, filename)
                
                # Save the figure
                self.current_fig.savefig(file_path, format="tiff", dpi=300)
                
                # Show toast notification
                self.toast.show_toast(f"Map saved as {filename}")
                
                print(f"✅ TIFF map saved as '{file_path}'")
                
            except Exception as e:
                messagebox.showerror("Error", 
                    f"Error saving file:\n{str(e)}\n\n"
                    "Please try again."
                )
    
    def on_window_resize(self, event=None):
        if self.root.state() == 'normal':  # Only handle when window is restored (not maximized)
            # Recalculate screen center
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Ensure we maintain 80% size
            self.default_width = int(screen_width * 0.8)
            self.default_height = int(screen_height * 0.8)
            
            # Recalculate center position
            x = (screen_width - self.default_width) // 2
            y = (screen_height - self.default_height) // 2
            
            # Update window geometry
            self.root.geometry(f"{self.default_width}x{self.default_height}+{x}+{y}")
            
            # Force geometry update
            self.root.update_idletasks()

if __name__ == "__main__":
    app = MainApplication()
