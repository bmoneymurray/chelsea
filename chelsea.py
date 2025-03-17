{\rtf1\ansi\ansicpg1252\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 HelveticaNeue;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab560
\pard\pardeftab560\slleading20\partightenfactor0

\f0\fs26 \cf0 import pandas as pd\
import matplotlib.pyplot as plt\
import os\
\
def load_data(file_path):\
    try:\
        # Check if file exists before loading\
        if os.path.exists(file_path):\
            data = pd.read_csv(file_path)\
            return data\
        else:\
            print(f"Error: File '\{file_path\}' not found.")\
            return None\
    except Exception as e:\
        print(f"Error loading data: \{e\}")\
        return None\
\
def clean_data(data):\
    try:\
        # Clean column names by stripping any whitespace\
        data.columns = data.columns.str.strip()\
        \
        # Check if required columns exist\
        required_columns = ['session_date', 'metric', 'value', 'season_name']\
        if all(col in data.columns for col in required_columns):\
            data['session_date'] = pd.to_datetime(data['session_date'])\
            \
            # Filter for rows with 'recovery' in the 'metric' column\
            recovery_data = data[data['metric'].str.contains('recovery', na=False)]\
            \
            # Drop rows with missing required values\
            recovery_data = recovery_data.dropna(subset=['session_date', 'metric', 'value', 'season_name'])\
            \
            return recovery_data\
        else:\
            print("Error: Required columns do not exist in the data.")\
            return None\
    except Exception as e:\
        print(f"Error cleaning data: \{e\}")\
        return None\
\
def visualize_recovery(recovery_data):\
    try:\
        # Group data by season and metric, and calculate the mean of 'value'\
        grouped_data = recovery_data.groupby(['season_name', 'metric'])['value'].mean().reset_index()\
        \
        # Optionally filter the top 5 seasons to make the plot clearer\
        top_seasons = grouped_data['season_name'].value_counts().head(5).index\
        grouped_data = grouped_data[grouped_data['season_name'].isin(top_seasons)]\
        \
        # Plot recovery status for each season\
        for season in grouped_data['season_name'].unique():\
            season_data = grouped_data[grouped_data['season_name'] == season]\
            plt.plot(season_data['metric'], season_data['value'], label=season)\
        \
        plt.xlabel('Recovery Metric')\
        plt.ylabel('Value')\
        plt.title('Recovery Status by Season')\
        plt.legend()\
        plt.show()\
    except Exception as e:\
        print(f"Error visualizing recovery data: \{e\}")\
\
def main():\
    # Allow dynamic file path input or default to the given path\
    file_path = '/Applications/Python 3.13/CFC Recovery status Data.csv'\
    \
    data = load_data(file_path)\
    if data is not None:\
        recovery_data = clean_data(data)\
        if recovery_data is not None:\
            visualize_recovery(recovery_data)\
        else:\
            print("No recovery data to visualize.")\
    else:\
        print("Failed to load data.")\
\
if __name__ == "__main__":\
    main()}