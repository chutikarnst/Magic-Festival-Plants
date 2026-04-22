import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

def open_data_dashboard():
    try:
        df = pd.read_csv('game_data.csv')
    except FileNotFoundError:
        temp_root = tk.Tk()
        temp_root.withdraw()
        messagebox.showwarning("No Data", "Please play at least 1 game hour to generate data.")
        temp_root.destroy()
        return

    root = tk.Tk()
    root.title("4.3 Data Analysis Report - Magic Festival")
    root.geometry("1000x800")
    
    content_frame = ttk.Frame(root)
    content_frame.pack(fill="both", expand=True, pady=10)

    def clear_content():
        for widget in content_frame.winfo_children():
            widget.destroy()

    def show_overall_stats():
        clear_content()
        lbl = ttk.Label(content_frame, text="4.1 & 4.2 Overall Score Statistics", font=("Arial", 16, "bold"))
        lbl.pack(pady=10)

        stats = df[['Fr_Score', 'V_Score', 'Fl_Score']].agg(['mean', 'std'])
        tree = ttk.Treeview(content_frame, columns=("Type", "Avg", "Std", "Total"), show='headings', height=5)
        tree.heading("Type", text="Plant Type")
        tree.heading("Avg", text="Average Score")
        tree.heading("Std", text="Standard Deviation")
        tree.heading("Total", text="Total Collected")

        data = [
            ("Fruit", stats['Fr_Score']['mean'], stats['Fr_Score']['std'], df['Fruit'].sum()),
            ("Vegetable", stats['V_Score']['mean'], stats['V_Score']['std'], df['Vegetable'].sum()),
            ("Flower", stats['Fl_Score']['mean'], stats['Fl_Score']['std'], df['Flower'].sum())
        ]
        for item in data: tree.insert("", "end", values=item)
        tree.pack(padx=20, pady=10, fill="x")

    def show_visuals(mode):
        clear_content()
        fig = plt.Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)

        if mode == "diversity":
            pivot = df.groupby('Game_ID')[['Fruit', 'Vegetable', 'Flower']].sum()
            row_sums = pivot.sum(axis=1)
            perc = pivot.div(row_sums.replace(0, 1), axis=0) * 100
            perc.plot(kind='bar', stacked=True, ax=ax, color=['#FFA500', '#228B22', '#FF69B4'])
            ax.set_title("Diverse Plants Percentage (Stacked Bar)")
            ax.set_ylabel("Percentage (%)")
            
        elif mode == "utility":
            def count_items(val):
                if pd.isna(val) or val == "": return 0
                return len(str(val).split('|'))
            df['Count'] = df['Item_used'].apply(count_items)
            ax.scatter(df['Hour'], df['Count'], color='purple', s=100, alpha=0.6)
            ax.set_title("Item Utility: Items Used per Hour (Scatter)")
            ax.set_xlabel("Game Hour")
            ax.set_xticks(range(1, 13))

        elif mode == "room":
            heatmap_data = pd.crosstab(df['Area_ID'], df['Hour'])
            sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", ax=ax, fmt='d')
            ax.set_title("Favorite Room: Area vs Hour (Heatmap)")

        elif mode == "hourly":
            df['Total_Score'] = df['Fr_Score'] + df['V_Score'] + df['Fl_Score']
            
            sns.boxplot(x='Hour', y='Total_Score', data=df, ax=ax, palette='Spectral')
            
            sns.stripplot(x='Hour', y='Total_Score', data=df, ax=ax, color='black', size=3, alpha=0.3)
            
            ax.set_title("Hourly Productivity Distribution (Box Plot)")
            ax.set_xlabel("Game Hour")
            ax.set_ylabel("Total Score")
            ax.set_xticks(range(0, 12)) 
            ax.set_xticklabels(range(1, 13))
            ax.grid(axis='y', linestyle='--', alpha=0.5)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # --- Navigation Buttons ---
    nav_frame = ttk.Frame(root)
    nav_frame.pack(side="top", fill="x", padx=10, pady=5)

    ttk.Button(nav_frame, text="Overall Stats", command=show_overall_stats).pack(side="left", padx=2)
    ttk.Button(nav_frame, text="Hourly Productivity", command=lambda: show_visuals("hourly")).pack(side="left", padx=2)
    ttk.Button(nav_frame, text="Diverse Plants", command=lambda: show_visuals("diversity")).pack(side="left", padx=2)
    ttk.Button(nav_frame, text="Item Utility", command=lambda: show_visuals("utility")).pack(side="left", padx=2)
    ttk.Button(nav_frame, text="Favorite Room", command=lambda: show_visuals("room")).pack(side="left", padx=2)

    show_overall_stats()
    root.mainloop()

if __name__ == "__main__":
    open_data_dashboard()