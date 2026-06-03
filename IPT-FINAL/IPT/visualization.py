import matplotlib
matplotlib.use('Agg')  # Fix: non-interactive backend, must be before pyplot import

import matplotlib.pyplot as plt
import os

SAVE_DIR = os.path.join("static", "Images")  # ✅ Correct path for Flask static files


class DataVisualization:

    def __init__(self, df):
        self.df = df
        os.makedirs(SAVE_DIR, exist_ok=True)  # ✅ Create folder if it doesn't exist

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

            self._save("barchart.png")

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

        # GENERATE ALL CHARTS
    def generate_all_charts(self):
        try:
            self.bar_chart()
            self.histogram_plot()
            self.boxplot_chart()
            self.grouped_bar_chart()
            self.pie_chart()
            print("\nAll charts generated successfully!")

        except Exception as e:
            print("Visualization Error:", e)
