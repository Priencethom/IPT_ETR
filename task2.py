import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#==========================DEMIE================================
class DataCleaning:
    
    def __init__(self):
        self.df = None

    def load_data(self):

        try:
            self.df = pd.read_csv("Teen_Mental_Health_Dataset.csv")
            print("Dataset loaded successfully!")

        except FileNotFoundError:
            print("CSV file not found.")

        except Exception as e:
            print("Error:", e)

    def show_data_info(self):

        print("\nDATASET INFO")
        print(self.df.info())

        print("\nDATASET DESCRIPTION")
        print(self.df.describe())

    def check_missing_values(self):

        print("\nMISSING VALUES")
        print(self.df.isnull().sum())

    def fill_missing_values(self):

        self.df = self.df.fillna(0)

        print("\nMissing values filled.")

    def remove_duplicate_rows(self):

        print("\nDUPLICATED ROWS:")
        print(self.df.duplicated())

        self.df = self.df.drop_duplicates()

        print("\nDuplicate rows removed.")

    def standardize_gender(self):

        self.df["gender"] = self.df["gender"].str.upper()

        print("\nGender values standardized.")

    def convert_data_types(self):

        self.df["age"] = self.df["age"].astype(int)
        self.df["daily_social_media_hours"] = self.df["daily_social_media_hours"].astype(float)
        self.df["sleep_hours"] = self.df["sleep_hours"].astype(float)

        print("\nData types converted.")

    def create_usage_level(self):

        usage_level = []

        for hours in self.df["daily_social_media_hours"]:

            if hours <= 2:
                usage_level.append("Low")

            elif hours <= 5:
                usage_level.append("Moderate")

            else:
                usage_level.append("Heavy")

        self.df["Social_Media_Usage_Level"] = usage_level

        print("\nSocial media usage level created.")

    def create_sleep_category(self):

        sleep_category = []

        for hours in self.df["sleep_hours"]:

            if hours < 5:
                sleep_category.append("Poor")

            elif hours <= 8:
                sleep_category.append("Normal")

            else:
                sleep_category.append("Healthy")

        self.df["Sleep_Category"] = sleep_category

        print("\nSleep category created.")

    def validate_dataset(self):

        print("\nCLEANED DATASET")

        print("\nFIRST 5 ROWS:")
        print(self.df.head())

        print("\nLAST 5 ROWS:")
        print(self.df.tail())

        print("\nFINAL MISSING VALUES")
        print(self.df.isnull().sum())

        print("\nNUMBER OF DUPLICATED ROWS")
        print(self.df.duplicated().sum())

        print("\nDATASET SHAPE")
        print(self.df.shape)

    def save_dataset(self):

        self.df.to_csv("cleaned_teen_mental_dataset.csv", index=False)

        print("\nCleaned dataset saved successfully!")

#==========================DEMIE================================


#====================PAM====================

class DataAnalytics:

    def __init__(self, df):
        self.df = df

    def summary_statistics(self):

        print("\n===== SUMMARY STATISTICS =====")

        cols = [
            "daily_social_media_hours",
            "academic_performance",
            "stress_level",
            "sleep_hours"
        ]

        for col in cols:

            try:
                print(f"\n{col}")
                print("Average:", np.mean(self.df[col]))
                print("Median:", np.median(self.df[col]))
                print("Std Dev:", np.std(self.df[col]))
                print("Min:", np.min(self.df[col]))
                print("Max:", np.max(self.df[col]))

            except Exception as e:
                print(f"{col} Error:", e)

    def correlation_analysis(self):

        print("\n===== CORRELATION ANALYSIS =====")

        pairs = [
            ("daily_social_media_hours", "academic_performance"),
            ("sleep_hours", "stress_level"),
            ("addiction_level", "depression_label")
        ]

        for x, y in pairs:

            try:
                corr = np.corrcoef(self.df[x], self.df[y])[0, 1]

                print(f"{x} vs {y}: {corr}")

            except Exception as e:
                print("Error:", e)

    def grouped_analysis(self):

        print("\n===== GENDER ANALYSIS =====")

        try:
            print(
                self.df.groupby("gender")[
                    ["stress_level", "sleep_hours"]
                ].mean()
            )

        except Exception as e:
            print("Error:", e)

        print("\n===== PLATFORM ANALYSIS =====")

        try:
            print(
                self.df.groupby("platform_usage")[
                    ["daily_social_media_hours"]
                ].mean()
            )

        except Exception as e:
            print("Error:", e)

        print("\n===== USAGE LEVEL ANALYSIS =====")

        try:
            print(
                self.df.groupby("Social_Media_Usage_Level")[
                    ["academic_performance"]
                ].mean()
            )

        except Exception as e:
            print("Error:", e)

    def dashboard_kpis(self):

        print("\n===== KPI DASHBOARD =====")

        try:
            print("Total Students:", len(self.df))

            print(
                "Average Social Media Hours:",
                round(np.mean(self.df["daily_social_media_hours"]), 2)
            )

            print(
                "Average Sleep Hours:",
                round(np.mean(self.df["sleep_hours"]), 2)
            )

            print(
                "Average Stress Level:",
                round(np.mean(self.df["stress_level"]), 2)
            )

        except Exception as e:
            print("Error:", e)

#====================PAM====================


#====================DACASIN====================

class DataVisualization:

    def __init__(self, df):
        self.df = df

    # SCATTER PLOT
    def scatter_plot(self):

        try:
            plt.figure(figsize=(8, 6))

            usage_levels = self.df["Social_Media_Usage_Level"]

            colors = []

            for level in usage_levels:

                if level == "Low":
                    colors.append("green")

                elif level == "Moderate":
                    colors.append("orange")

                else:
                    colors.append("red")

            plt.scatter(
                self.df["daily_social_media_hours"],
                self.df["academic_performance"],
                c=colors,
                alpha=0.7
            )

            plt.xlabel("Social Media Usage Hours")
            plt.ylabel("Academic Performance")
            plt.title("Social Media Usage vs Academic Performance")

            plt.grid(True)

            plt.savefig("scatter_plot.png")

            plt.close()

            print("Scatter plot saved successfully!")

        except Exception as e:
            print("Scatter Plot Error:", e)

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

            plt.savefig("histogram_plot.png")

            plt.close()

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

            plt.savefig("boxplot_chart.png")

            plt.close()

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

            plt.savefig("grouped_bar_chart.png")

            plt.close()

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

            plt.savefig("pie_chart.png")

            plt.close()

            print("Pie chart saved successfully!")

        except Exception as e:
            print("Pie Chart Error:", e)

    # GENERATE ALL CHARTS
    def generate_all_charts(self):

        try:
            self.scatter_plot()
            self.histogram_plot()
            self.boxplot_chart()
            self.grouped_bar_chart()
            self.pie_chart()

            print("\nAll charts generated successfully!")

        except Exception as e:
            print("Visualization Error:", e)

#====================DACASIN====================


clean = DataCleaning()

clean.load_data()
clean.show_data_info()
clean.check_missing_values()
clean.fill_missing_values()
clean.remove_duplicate_rows()
clean.standardize_gender()
clean.convert_data_types()
clean.create_usage_level()
clean.create_sleep_category()
clean.validate_dataset()
clean.save_dataset()

analytics = DataAnalytics(clean.df)

analytics.summary_statistics()
analytics.correlation_analysis()
analytics.grouped_analysis()
analytics.dashboard_kpis()

visuals = DataVisualization(clean.df)

visuals.generate_all_charts()