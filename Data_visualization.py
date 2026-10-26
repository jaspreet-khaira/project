import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BG = "#F4F6FF"
WHITE = "#FFFFFF"
PURPLE = "#5945F5"
PURPLE_DARK = "#4334D9"
PURPLE_LIGHT = "#EEEBFF"
TEXT = "#172554"
MUTED = "#64748B"
BORDER = "#E0E7FF"
GREEN = "#16A34A"
PINK = "#F5D0FE"
BLUE_LIGHT = "#E0ECFF"

class DataVisualizationDashboard:

    def __init__(self, root):
        self.root = root

        self.root.title("Data Visualization Dashboard")
        self.root.geometry("1050x720")
        self.root.minsize(900, 620)
        self.root.configure(bg=BG)

        self.df = None
        self.file_name = ""
        self.figure = None
        self.canvas = None

        self.setup_styles()
        self.create_header()
        self.create_controls()
        self.create_content()
        self.create_status_bar()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Modern.TCombobox",
            padding=7,
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT,
            bordercolor=BORDER,
            arrowsize=13
        )

        style.map(
            "Modern.TCombobox",
            fieldbackground=[("readonly", WHITE)],
            foreground=[("readonly", TEXT)]
        )

        style.configure(
            "Modern.Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=29,
            borderwidth=0,
            font=("Segoe UI", 9)
        )

        style.configure(
            "Modern.Treeview.Heading",
            background="#EAEAFF",
            foreground=TEXT,
            font=("Segoe UI", 9, "bold"),
            padding=8,
            relief="flat"
        )

        style.map(
            "Modern.Treeview",
            background=[("selected", "#DCD6FF")],
            foreground=[("selected", TEXT)]
        )

    def make_button(
        self, parent, text, command,
        color=PURPLE, foreground=WHITE
    ):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=foreground,
            activebackground=PURPLE_DARK,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=8
        )

    def create_header(self):

        title_bar = tk.Frame(
            self.root,
            bg=PURPLE,
            height=43
        )
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)

        tk.Label(
            title_bar,
            text="◈  Data Visualization Dashboard",
            bg=PURPLE,
            fg=WHITE,
            font=("Segoe UI", 11)
        ).pack(side="left", padx=18)

        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=22, pady=(17, 13))

        icon = tk.Label(
            header,
            text="▥",
            bg=PURPLE_LIGHT,
            fg=PURPLE,
            font=("Segoe UI", 28, "bold"),
            width=3,
            height=1
        )
        icon.pack(side="left", padx=(0, 14))

        title_area = tk.Frame(header, bg=BG)
        title_area.pack(side="left", fill="x", expand=True)

        tk.Label(
            title_area,
            text="Data Visualization Dashboard",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 21, "bold")
        ).pack(anchor="w")

        tk.Label(
            title_area,
            text="Upload your dataset and create beautiful visualizations",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(3, 0))

    def create_controls(self):

        panel = tk.Frame(
            self.root,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        panel.pack(fill="x", padx=22, pady=(0, 14))

        panel.grid_columnconfigure(1, weight=1)
        panel.grid_columnconfigure(2, weight=1)
        panel.grid_columnconfigure(3, weight=1)

        upload = self.make_button(
            panel,
            "📁 Upload CSV",
            self.upload_csv
        )
        upload.grid(
            row=0, column=0, rowspan=2,
            padx=12, pady=18, sticky="nsew"
        )

        self.x_column = self.create_dropdown(
            panel, "X-Axis Column", 1
        )

        self.y_column = self.create_dropdown(
            panel, "Y-Axis Column", 2
        )

        self.chart_type = self.create_dropdown(
            panel, "Chart Type", 3
        )

        self.chart_type["values"] = [
            "Bar Chart",
            "Line Chart",
            "Scatter Plot",
            "Histogram",
            "Pie Chart"
        ]
        self.chart_type.set("Bar Chart")

        actions = tk.Frame(panel, bg=WHITE)
        actions.grid(
            row=0, column=4, rowspan=2,
            padx=12, pady=12, sticky="nsew"
        )

        self.make_button(
            actions,
            "▥  Generate Chart",
            self.generate_chart
        ).pack(fill="x", pady=(0, 8))

        bottom_buttons = tk.Frame(actions, bg=WHITE)
        bottom_buttons.pack(fill="x")

        self.make_button(
            bottom_buttons,
            "↓ Save",
            self.save_chart,
            color=PURPLE_LIGHT,
            foreground=PURPLE
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        self.make_button(
            bottom_buttons,
            "▤ Stats",
            self.show_statistics,
            color=BLUE_LIGHT,
            foreground=PURPLE_DARK
        ).pack(side="left", expand=True, fill="x", padx=(4, 0))

    def create_dropdown(self, parent, label, column):

        frame = tk.Frame(parent, bg=WHITE)
        frame.grid(
            row=0, column=column, rowspan=2,
            padx=7, pady=18, sticky="nsew"
        )

        tk.Label(
            frame,
            text=label,
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(0, 8))

        combo = ttk.Combobox(
            frame,
            state="readonly",
            style="Modern.TCombobox",
            width=15
        )
        combo.pack(fill="x")

        return combo

    def create_content(self):

        content = tk.Frame(self.root, bg=BG)
        content.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=(0, 12)
        )

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        # LEFT: DATASET TABLE

        left = tk.Frame(
            content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        left.grid(
            row=0, column=0,
            sticky="nsew",
            padx=(0, 7)
        )

        left_header = tk.Frame(left, bg=WHITE)
        left_header.pack(
            fill="x",
            padx=14,
            pady=14
        )

        tk.Label(
            left_header,
            text="▦  Dataset Preview",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 12, "bold")
        ).pack(side="left")

        self.rows_label = tk.Label(
            left_header,
            text="0 rows",
            bg=PURPLE_LIGHT,
            fg=PURPLE_DARK,
            font=("Segoe UI", 9, "bold"),
            padx=9,
            pady=4
        )
        self.rows_label.pack(side="right")

        table_container = tk.Frame(left, bg=WHITE)
        table_container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 12)
        )

        self.table = ttk.Treeview(
            table_container,
            show="headings",
            style="Modern.Treeview",
            height=8
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll_y = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.table.yview
        )
        scroll_y.pack(side="right", fill="y")

        self.table.configure(
            yscrollcommand=scroll_y.set
        )

        scroll_x = ttk.Scrollbar(
            left,
            orient="horizontal",
            command=self.table.xview
        )
        scroll_x.pack(fill="x", padx=10, pady=(0, 10))

        self.table.configure(
            xscrollcommand=scroll_x.set
        )

        self.table.tag_configure(
            "even",
            background="#F8FAFF"
        )
        self.table.tag_configure(
            "odd",
            background=WHITE
        )

        right = tk.Frame(
            content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        right.grid(
            row=0, column=1,
            sticky="nsew",
            padx=(7, 0)
        )

        graph_header = tk.Frame(right, bg=WHITE)
        graph_header.pack(
            fill="x",
            padx=14,
            pady=14
        )

        tk.Label(
            graph_header,
            text="⌁  Generated Visualization",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 12, "bold")
        ).pack(side="left")

        self.graph_status = tk.Label(
            graph_header,
            text="● Ready",
            bg=WHITE,
            fg=GREEN,
            font=("Segoe UI", 9)
        )
        self.graph_status.pack(side="right")

        self.graph_frame = tk.Frame(right, bg=WHITE)
        self.graph_frame.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(0, 10)
        )

        self.placeholder = tk.Frame(
            self.graph_frame,
            bg=WHITE
        )
        self.placeholder.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        tk.Label(
            self.placeholder,
            text="▥",
            bg=WHITE,
            fg="#C4B5FD",
            font=("Segoe UI", 42, "bold")
        ).pack()

        tk.Label(
            self.placeholder,
            text="Your chart will appear here",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 12, "bold")
        ).pack(pady=5)

        tk.Label(
            self.placeholder,
            text="Upload CSV → Select columns → Generate",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack()

    def create_status_bar(self):

        bar = tk.Frame(
            self.root,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        bar.pack(fill="x", padx=22, pady=(0, 12))

        self.status_label = tk.Label(
            bar,
            text="●  Ready — Upload a CSV file to get started",
            bg=WHITE,
            fg=GREEN,
            font=("Segoe UI", 9),
            padx=12,
            pady=10
        )
        self.status_label.pack(side="left")

        self.file_label = tk.Label(
            bar,
            text="No file selected",
            bg=WHITE,
            fg=PURPLE_DARK,
            font=("Segoe UI", 9, "bold"),
            padx=12
        )
        self.file_label.pack(side="right")

    def upload_csv(self):

        path = filedialog.askopenfilename(
            title="Select CSV Dataset",
            filetypes=[("CSV Files", "*.csv")]
        )

        if not path:
            return

        try:
            df = pd.read_csv(path)

            if df.empty:
                messagebox.showerror(
                    "Invalid CSV",
                    "The selected file contains no data."
                )
                return

            if not df.columns.is_unique:
                messagebox.showerror(
                    "Invalid CSV",
                    "Column names must be unique."
                )
                return

            self.df = df
            self.file_name = os.path.basename(path)

            columns = list(df.columns)

            self.x_column["values"] = columns
            self.y_column["values"] = columns

            self.x_column.set(columns[0])

            numeric = list(
                df.select_dtypes(include=np.number).columns
            )

            self.y_column.set(
                numeric[0] if numeric else columns[0]
            )

            self.update_table()

            self.rows_label.config(
                text=f"{len(df):,} rows"
            )

            self.file_label.config(
                text=f"▤  {self.file_name}"
            )

            self.status_label.config(
                text="●  Dataset loaded successfully!",
                fg=GREEN
            )

            self.graph_status.config(
                text="● Dataset loaded",
                fg=GREEN
            )

        except Exception as error:
            messagebox.showerror(
                "CSV Error",
                str(error)
            )
    def update_table(self):

        self.table.delete(
            *self.table.get_children()
        )

        columns = list(self.df.columns)

        self.table["columns"] = columns

        for column in columns:
            self.table.heading(
                column,
                text=str(column)
            )

            self.table.column(
                column,
                width=100,
                minwidth=70,
                anchor="w"
            )

        for i, (_, row) in enumerate(
            self.df.head(100).iterrows()
        ):

            values = [
                "" if pd.isna(value) else str(value)
                for value in row
            ]

            self.table.insert(
                "",
                "end",
                values=values,
                tags=("even" if i % 2 == 0 else "odd",)
            )
    def generate_chart(self):

        if self.df is None:
            messagebox.showwarning(
                "Upload Required",
                "Please upload a CSV file first."
            )
            return

        x = self.x_column.get()
        y = self.y_column.get()
        chart = self.chart_type.get()

        try:
            with plt.rc_context({
                "font.family": "DejaVu Sans",
                "font.size": 9,
                "axes.titlesize": 12,
                "axes.titleweight": "bold",
                "axes.labelsize": 9,
                "axes.edgecolor": "#CBD5E1",
                "axes.labelcolor": TEXT,
                "xtick.color": MUTED,
                "ytick.color": MUTED
            }):

                fig, ax = plt.subplots(
                    figsize=(5.0, 3.7),
                    dpi=85
                )

                fig.patch.set_facecolor(WHITE)
                ax.set_facecolor(WHITE)

                if chart == "Histogram":

                    values = pd.to_numeric(
                        self.df[x],
                        errors="coerce"
                    ).dropna()

                    if values.empty:
                        raise ValueError(
                            "Choose a numeric column for the histogram."
                        )

                    ax.hist(
                        values,
                        bins=8,
                        color=PURPLE,
                        edgecolor=WHITE,
                        linewidth=1.5
                    )

                    ax.set_xlabel(x)
                    ax.set_ylabel("Frequency")
                    ax.set_title(
                        f"Distribution of {x}",
                        loc="left",
                        pad=12
                    )

                elif chart == "Bar Chart":

                    values = pd.to_numeric(
                        self.df[y],
                        errors="coerce"
                    )

                    data = pd.DataFrame({
                        "category": self.df[x],
                        "value": values
                    }).dropna()

                    data = data.groupby(
                        "category",
                        as_index=False
                    )["value"].mean()

                    data = data.sort_values(
                        "value",
                        ascending=False
                    ).head(12)

                    if data.empty:
                        raise ValueError(
                            "No valid numeric values available."
                        )

                    palette = [
                        "#4F8DFD",
                        "#38B779",
                        "#FFB02E",
                        "#F05B7E",
                        "#8B5CF6",
                        "#06B6D4",
                        "#F97316",
                        "#14B8A6",
                        "#818CF8",
                        "#EC4899",
                        "#84CC16",
                        "#A78BFA"
                    ]

                    bars = ax.bar(
                        data["category"].astype(str),
                        data["value"],
                        color=palette[:len(data)],
                        width=0.72
                    )

                    ax.set_xlabel(x)
                    ax.set_ylabel(y)
                    ax.set_title(
                        f"{y} by {x}",
                        loc="left",
                        pad=12
                    )

                    ax.tick_params(
                        axis="x",
                        rotation=30,
                        labelsize=8
                    )

                    ax.bar_label(
                        bars,
                        fmt="%.0f",
                        padding=2,
                        fontsize=7
                    )

                elif chart == "Line Chart":

                    values = pd.to_numeric(
                        self.df[y],
                        errors="coerce"
                    )

                    data = pd.DataFrame({
                        "category": self.df[x],
                        "value": values
                    }).dropna()

                    if data.empty:
                        raise ValueError(
                            "No valid data available."
                        )

                    ax.plot(
                        data["category"].astype(str),
                        data["value"],
                        color=PURPLE,
                        marker="o",
                        linewidth=2.5,
                        markersize=5
                    )

                    ax.set_xlabel(x)
                    ax.set_ylabel(y)
                    ax.set_title(
                        f"{y} Trend",
                        loc="left",
                        pad=12
                    )

                    ax.tick_params(
                        axis="x",
                        rotation=30,
                        labelsize=8
                    )

                elif chart == "Scatter Plot":

                    xv = pd.to_numeric(
                        self.df[x],
                        errors="coerce"
                    )

                    yv = pd.to_numeric(
                        self.df[y],
                        errors="coerce"
                    )

                    data = pd.DataFrame({
                        "x": xv,
                        "y": yv
                    }).dropna()

                    if data.empty:
                        raise ValueError(
                            "Scatter plots require two numeric columns."
                        )

                    ax.scatter(
                        data["x"],
                        data["y"],
                        color=PURPLE,
                        s=45,
                        alpha=0.8
                    )

                    ax.set_xlabel(x)
                    ax.set_ylabel(y)
                    ax.set_title(
                        f"{y} vs {x}",
                        loc="left",
                        pad=12
                    )

                elif chart == "Pie Chart":

                    values = pd.to_numeric(
                        self.df[y],
                        errors="coerce"
                    )

                    data = pd.DataFrame({
                        "category": self.df[x],
                        "value": values
                    }).dropna()

                    data = data.groupby(
                        "category",
                        as_index=False
                    )["value"].sum()

                    data = data[data["value"] > 0]

                    if data.empty:
                        raise ValueError(
                            "No positive values available for the pie chart."
                        )

                    if len(data) > 10:
                        raise ValueError(
                            "Choose a column with 10 or fewer categories."
                        )

                    ax.pie(
                        data["value"],
                        labels=data["category"].astype(str),
                        autopct="%1.0f%%",
                        startangle=90,
                        textprops={"fontsize": 8},
                        wedgeprops={
                            "edgecolor": WHITE,
                            "linewidth": 2
                        }
                    )

                    ax.set_title(
                        f"{y} Distribution",
                        loc="left",
                        pad=12
                    )

                if chart != "Pie Chart":
                    ax.grid(
                        axis="y",
                        linestyle="--",
                        alpha=0.25
                    )
                    ax.set_axisbelow(True)

                fig.tight_layout(pad=1.8)

            self.display_chart(fig)

            self.graph_status.config(
                text=f"● {chart}",
                fg=GREEN
            )

            self.status_label.config(
                text=f"●  {chart} generated successfully!",
                fg=GREEN
            )

        except Exception as error:
            messagebox.showerror(
                "Chart Error",
                str(error)
            )

    def display_chart(self, fig):

        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        if self.figure is not None:
            plt.close(self.figure)

        if hasattr(self, "placeholder"):
            self.placeholder.destroy()

        self.figure = fig

        self.canvas = FigureCanvasTkAgg(
            fig,
            master=self.graph_frame
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    def save_chart(self):

        if self.figure is None:
            messagebox.showwarning(
                "No Chart",
                "Generate a chart before saving."
            )
            return

        path = filedialog.asksaveasfilename(
            title="Save Visualization",
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("PDF Document", "*.pdf")
            ]
        )

        if path:
            try:
                self.figure.savefig(
                    path,
                    dpi=250,
                    bbox_inches="tight",
                    facecolor=WHITE
                )

                self.status_label.config(
                    text="●  Chart exported successfully!",
                    fg=GREEN
                )

                messagebox.showinfo(
                    "Export Complete",
                    f"Chart saved successfully:\n{path}"
                )

            except Exception as error:
                messagebox.showerror(
                    "Save Error",
                    str(error)
                )

    def show_statistics(self):

        if self.df is None:
            messagebox.showwarning(
                "No Dataset",
                "Upload a CSV file first."
            )
            return

        window = tk.Toplevel(self.root)
        window.title("Dataset Statistics")
        window.geometry("600x400")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="Dataset Statistics",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", padx=18, pady=18)

        numeric = self.df.select_dtypes(
            include=np.number
        )

        if numeric.empty:
            result = "No numeric columns were found."
        else:
            result = numeric.describe().round(2).to_string()

        text_box = tk.Text(
            window,
            font=("Consolas", 10),
            bg=WHITE,
            fg=TEXT,
            relief="flat",
            padx=12,
            pady=12
        )

        text_box.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 18)
        )

        text_box.insert("1.0", result)
        text_box.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizationDashboard(root)
    root.mainloop()
