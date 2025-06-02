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
        
    def show_toast(self, message, duration=3000):
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
        
        # Success icon (checkmark)
        icon_label = ttk.Label(msg_frame, text="✓", font=('Helvetica', 14, 'bold'), foreground='green')
        icon_label.pack(side='left', padx=(0, 10))
        
        # Message
        msg_label = ttk.Label(msg_frame, text=message, font=('Helvetica', 10))
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

class MainApplication:
    def __init__(self):
        # Create and hide the root window
        self.root = tk.Tk()
        self.root.withdraw()
        
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
            self.df = self.pd.DataFrame()
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
            self.root.after(100, self.finish_loading)
        except Exception as e:
            self.show_error(f"Error loading shapefile: {str(e)}")
    
    def finish_loading(self):
        """Complete the loading process"""
        try:
            self.splash.update_status("Ready to explore Montana's beauty...")
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
            self.all_color.set("green")
            self.selected_file_var.set("No file selected")
            
            # Initialize GUI
            self.splash.destroy()
            self.initialize_gui()
            
        except Exception as e:
            self.show_error(f"Error initializing application: {str(e)}")
    
    def show_error(self, message):
        """Show error message and exit"""
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
    
    def generate_map(self):
        if self.map_canvas:
            self.map_canvas.get_tk_widget().destroy()
        
        gdf_copy = self.gdf.copy()
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
        
        if year.isdigit():
            year = int(year)
            for county in filtered["county"].unique():
                county_data = filtered[filtered["county"] == county]
                post_count = (county_data["year"] >= year).sum()
                pre_count = (county_data["year"] < year).sum()
                if post_count + pre_count > 0:
                    color = self.post_color.get() if post_count >= pre_count else self.pre_color.get()
                    gdf_copy.loc[gdf_copy["County"] == county, "Color"] = color
        else:
            for county in filtered["county"].unique():
                gdf_copy.loc[gdf_copy["County"] == county, "Color"] = self.all_color.get()
        
        fig, ax = self.plt.subplots(figsize=(10, 10))
        gdf_copy.boundary.plot(ax=ax, linewidth=1, edgecolor="black")
        gdf_copy.plot(ax=ax, color=gdf_copy["Color"], alpha=0.6)
        
        ax.set_title(f"{fam.title()} > {gen.title()} > {spec.lower()}", fontsize=15)
        ax.axis("off")
        
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
                
                # Create filename with timestamp
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"montana_bee_map_{timestamp}.tiff"
                
                # Full path for the file
                file_path = os.path.join(downloads_path, filename)
                
                # Save the figure
                self.current_fig.savefig(file_path, format="tiff", dpi=300)
                
                # Show toast notification
                self.toast.show_toast(f"Map saved successfully to Downloads folder")
                
                print(f"✅ TIFF map saved as '{file_path}'")
                
            except Exception as e:
                messagebox.showerror("Error", 
                    f"Error saving file:\n{str(e)}\n\n"
                    "Please try again."
                )
    
    def on_window_resize(self, event=None):
        if self.root.state() == 'normal':
            self.root.geometry(f"{self.default_width}x{self.default_height}+{self.x_position}+{self.y_position}")
    
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
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
        
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
        title_label = ttk.Label(title_frame, text="Montana Bee County Map Generator", style='Title.TLabel')
        title_label.pack()
        
        # Create left panel for controls with scrollbar
        left_panel_container = ttk.Frame(main_container)
        left_panel_container.pack(side='left', fill='y', padx=(0, 20))
        
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
        color_options = ["red", "green", "blue", "grey", "black", "yellow", "purple", "orange", "pink", "brown"]
        
        # Pre Color
        ttk.Label(color_frame, text="Pre-Year Color:", style='TLabel').pack(fill='x')
        pre_color_combo = ttk.Combobox(
            color_frame, 
            textvariable=self.pre_color, 
            values=color_options,
            state="normal"
        )
        pre_color_combo.pack(fill='x', pady=(0, 10))
        
        # Post Color
        ttk.Label(color_frame, text="Post-Year Color:", style='TLabel').pack(fill='x')
        post_color_combo = ttk.Combobox(
            color_frame, 
            textvariable=self.post_color, 
            values=color_options,
            state="normal"
        )
        post_color_combo.pack(fill='x', pady=(0, 10))
        
        # All Color
        ttk.Label(color_frame, text="All Records Color:", style='TLabel').pack(fill='x')
        all_color_combo = ttk.Combobox(
            color_frame, 
            textvariable=self.all_color, 
            values=color_options,
            state="normal"
        )
        all_color_combo.pack(fill='x', pady=(0, 10))
        
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
        self.download_button.pack(fill='x')
        
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
        
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApplication()
