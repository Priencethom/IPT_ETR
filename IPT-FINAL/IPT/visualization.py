import matplotlib
matplotlib.use('Agg')  # Fix: non-interactive backend, must be before pyplot import

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
import os

SAVE_DIR = os.path.join("static", "Images")  # ✅ Correct path for Flask static files

class DataVisualization:

    def __init__(self, df):
        self.df = df
        os.makedirs(SAVE_DIR, exist_ok=True)  # ✅ Create folder if it doesn't exist
        
        # Isaayos ang order ng social interaction level kung mayroon sa dataset
        if 'social_interaction_level' in self.df.columns:
            self.df['social_interaction_level'] = pd.Categorical(
                self.df['social_interaction_level'], 
                categories=['low', 'medium', 'high'], 
                ordered=True
            )

    def _save(self, filename):
        """Helper: save to static/Images/ and close the figure."""
        path = os.path.join(SAVE_DIR, filename)
        plt.savefig(path, bbox_inches='tight')
        plt.close()
        return path

    #BAR CHART
    def bar_chart(self):

        try:

            data = self.df.groupby(
                "Social_Media_Usage_Level"
            )["academic_performance"].mean()

            order = ["Low", "Moderate", "Heavy"]
            data = data.reindex(order)

            plt.figure(figsize=(8, 6))

            bars = plt.bar(
                data.index,
                data.values,
                color=["green", "orange", "red"]
            )

            plt.xlabel("Social Media Usage Level")
            plt.ylabel("Average Academic Grade")
            plt.title(
                "Average Academic Grade by Social Media Usage Level"
            )

            plt.ylim(
                data.min() - 0.2,
                data.max() + 0.2
            )

            for bar in bars:

                height = round(bar.get_height(), 2)

                plt.text(
                    bar.get_x() + bar.get_width()/2,
                    height,
                    str(height),
                    ha="center",
                    va="bottom"
                )

            plt.grid(axis="y")

            self._save("bar_chart.png")

            print("Bar chart saved successfully!")

        except Exception as e:

            print("Bar Chart Error:", e)

    # HISTOGRAM
    def histogram_plot(self):
        try:
            plt.figure(figsize=(8, 6))

            plt.hist(
                self.df["stress_level"],
                bins=10,
                edgecolor="black",
                rwidth=0.9,
                color="skyblue"
            )

            plt.xlabel("Stress Level")
            plt.ylabel("Frequency")
            plt.title("Stress Level Distribution")
            plt.grid(axis="y")

            self._save("histogram_plot.png")
            print("Histogram saved successfully!")

        except Exception as e:
            print("Histogram Error:", e)

    # BOXPLOT
    def boxplot_chart(self):
        try:
            plt.figure(figsize=(8, 6))

            plt.boxplot(
                [
                    self.df["sleep_hours"],
                    self.df["academic_performance"]
                ],
                labels=["Sleep Hours", "Academic Performance"],
                patch_artist=True
            )

            plt.title("Sleep Hours vs Academic Performance")
            plt.grid(True)

            self._save("boxplot_chart.png")
            print("Boxplot saved successfully!")

        except Exception as e:
            print("Boxplot Error:", e)

    # GROUPED BAR CHART
    def grouped_bar_chart(self):
        try:
            grouped_data = self.df.groupby(
                "Social_Media_Usage_Level"
            )["anxiety_level"].mean()

            plt.figure(figsize=(8, 6))

            bars = plt.bar(
                grouped_data.index,
                grouped_data.values,
                color=["green", "orange", "red"]
            )

            plt.xlabel("Usage Level")
            plt.ylabel("Average Anxiety Level")
            plt.title("Usage Level vs Anxiety Level")
            plt.grid(axis="y")

            for bar in bars:
                height = bar.get_height()
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    round(height, 2),
                    ha="center",
                    va="bottom"
                )

            self._save("grouped_bar_chart.png")
            print("Grouped bar chart saved successfully!")

        except Exception as e:
            print("Grouped Bar Chart Error:", e)

    # PIE CHART
    def pie_chart(self):
        try:
            platform_counts = self.df["platform_usage"].value_counts()

            plt.figure(figsize=(8, 6))

            plt.pie(
                platform_counts.values,
                labels=platform_counts.index,
                autopct="%1.1f%%",
                startangle=90
            )

            plt.title("Platform Usage Distribution")

            self._save("pie_chart.png")
            print("Pie chart saved successfully!")

        except Exception as e:
            print("Pie Chart Error:", e)

    def stress_vs_age(self):
        grouped = self.df.groupby("age")["stress_level"].mean()

        plt.figure(figsize=(8,6))

        plt.plot(
            grouped.index,
            grouped.values,
            marker='o'
        )
        plt.grid(axis="y")
        plt.xlabel("Age")
        plt.ylabel("Average Stress Level")
        plt.title("Average Stress Level by Age")

        self._save("stress_age.png")
        print("Stress vs. Age saved successfully!")

    
    def bar_chart2(self):
        try:

            data = self.df.groupby(
                "Social_Media_Usage_Level"
            )["physical_activity"].mean()

            plt.figure(figsize=(8, 6))

            bars = plt.bar(
                data.index,
                data.values,
                color=["green", "orange", "red"]
            )

            plt.xlabel("Social Media Usage Level")
            plt.ylabel("Average Physical Activity (Hours)")
            plt.title("Social Media Usage Level vs Physical Activity")

            plt.grid(axis="y")

            for bar in bars:

                height = round(bar.get_height(), 2)

                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    str(height),
                    ha="center",
                    va="bottom"
                )

            self._save("bar_chart2.png")

            print("Bar chart saved successfully!")

        except Exception as e:

            print("Bar Chart Error:", e)

    # 2. 2D HISTOGRAM: Sleep hours at Screentime before sleep
    def histogram_plot2(self):
        try:
            plt.figure(figsize=(8, 6))
            
            h = plt.hist2d(self.df["screen_time_before_sleep"], self.df["sleep_hours"], 
                           bins=6, cmap="Blues", edgecolor='white', linewidth=0.5)
            
            cbar = plt.colorbar(h[3])
            cbar.set_label('Total Number of Teens in this Range', fontweight='bold', fontsize=11)
            
            counts, xedges, yedges, image = h
            max_count = counts.max()
            
            for i in range(len(xedges)-1):
                for j in range(len(yedges)-1):
                    if counts[i, j] > 0: 
                        x_center = (xedges[i] + xedges[i+1]) / 2
                        y_center = (yedges[j] + yedges[j+1]) / 2
                        text_color = "white" if counts[i, j] > (max_count / 2) else "black"
                        
                        plt.text(x_center, y_center, int(counts[i, j]), 
                                 ha="center", va="center", color=text_color, fontsize=10, fontweight='bold')

            plt.title("4. Screen Time Before Sleep vs Sleep Hours (Density Grid)")
            plt.xlabel("Screen Time Before Sleep (Hours)")
            plt.ylabel("Hours of Sleep")
            
            self._save("histogram_plot2.png")
            print("2D Histogram saved successfully!")

        except Exception as e:
            print("Histogram Error:", e)

        # 4. BAR GRAPH: Physical activity at Depression level (Saves as grouped_bar_chart.png)
    def grouped_bar_chart2(self):
        try:
            plt.figure(figsize=(8, 6))
            bar_data = self.df.groupby('depression_label')['physical_activity'].mean().reset_index()
            bar_data['depression_label'] = bar_data['depression_label'].map({0: 'Normal', 1: 'Depressed'})
            
            colors = ['#66c2a5', '#fc8d62']
            bars = plt.bar(bar_data['depression_label'], bar_data['physical_activity'], color=colors)
            
            plt.bar_label(bars, fmt='%.2f hrs', padding=3, fontsize=12, fontweight='bold')
            
            legend_elements = [
                Patch(facecolor='#66c2a5', label='Normal (No Depression)'),
                Patch(facecolor='#fc8d62', label='Depressed Label')
            ]
            plt.legend(handles=legend_elements, title="Category Guide", loc="upper right")
            
            plt.title("5. Average Physical Activity by Depression Level")
            plt.xlabel("Clinical Assessment (Depression Level)")
            plt.ylabel("Average Physical Activity (Hours)")
            plt.ylim(0, bar_data['physical_activity'].max() * 1.3)
            plt.grid(axis='y', linestyle='--', alpha=0.6)
            
            self._save("grouped_bar_chart2.png")
            print("Bar chart saved successfully!")

        except Exception as e:
            print("Grouped Bar Chart Error:", e)

    # 5. PIE CHART: Social Media Hours at Social Interactions
    def pie_chart2(self):
        try:
            plt.figure(figsize=(9, 6)) 
            pie_data = self.df.groupby('social_interaction_level', observed=False)['daily_social_media_hours'].sum()
            
            labels = pie_data.index.str.title()
            colors = ['#ff9999','#66b3ff','#99ff99']
            
            wedges, texts, autotexts = plt.pie(
                pie_data, labels=labels, autopct='%1.1f%%', 
                startangle=140, colors=colors,
                textprops={'fontsize': 11, 'weight': 'bold'}
            )
            
            plt.legend(wedges, labels, title="Interaction Levels", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            
            plt.title("2. Share of Social Media Hours per Social Interaction Level")
            
            self._save("pie_chart2.png")
            print("Pie chart saved successfully!")

        except Exception as e:
            print("Pie Chart Error:", e)


        # GENERATE ALL CHARTS
    def generate_all_charts(self):
        try:
            self.bar_chart()
            self.histogram_plot()
            self.boxplot_chart()
            self.grouped_bar_chart()
            self.pie_chart()
            self.stress_vs_age()
            self.bar_chart2()
            self.histogram_plot2()
            self.boxplot_chart2()
            self.grouped_bar_chart2()
            self.pie_chart2()
            print("\nAll charts generated successfully!")

        except Exception as e:
            print("Visualization Error:", e)
