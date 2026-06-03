import pandas as pd


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

        print("\nLAST 5 ROWS")
        print(self.df.tail())

        print("\nFINAL MISSING VALUES")
        print(self.df.isnull().sum())

        print("\nNUMBER OF DUPLICATED ROWS")
        print(self.df.duplicated().sum())

        print("\nDATASET SHAPE")
        print(self.df.shape)
