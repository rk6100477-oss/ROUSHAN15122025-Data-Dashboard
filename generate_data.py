# Install dependencies: run `pip install -r requirements.txt` in the project venv
import pandas as pd
import numpy as np

# Function to interpolate data year-by-year (2015-2025)
def generate_state_data(state, pop15, pop25, diab15, diab25, pre15, pre25, diag15, diag25):
    years = np.arange(2015, 2026)
    # Linear interpolation for smooth trends
    pop = np.linspace(pop15, pop25, len(years))
    diab = np.linspace(diab15, diab25, len(years))
    pre = np.linspace(pre15, pre25, len(years))
    diag = np.linspace(diag15, diag25, len(years))
    
    df = pd.DataFrame({
        'State': state, 'Year': years, 'Population_Millions': pop,
        'Diabetes_Prev_Pct': diab, 'Pre_Diabetes_Prev_Pct': pre, 'Diagnosis_Rate_Pct': diag
    })
    
    # Calculate absolute numbers (Millions)
    df['Total_Diabetics_Millions'] = (df['Population_Millions'] * df['Diabetes_Prev_Pct'] / 100)
    df['Total_Pre_Diabetics_Millions'] = (df['Population_Millions'] * df['Pre_Diabetes_Prev_Pct'] / 100)
    df['Diagnosed_Millions'] = df['Total_Diabetics_Millions'] * (df['Diagnosis_Rate_Pct'] / 100)
    df['Undiagnosed_Millions'] = df['Total_Diabetics_Millions'] - df['Diagnosed_Millions']
    
    return df.round(3)

# Parameters for 8 States (Based on Research Data)
states_data = [
    # State, Pop15, Pop25, Diab15, Diab25, Pre15, Pre25, Diag15, Diag25
    ('Goa', 1.48, 1.59, 16.8, 26.8, 18.5, 19.8, 55, 60),
    ('New Delhi', 18.5, 22.28, 14.2, 17.8, 15.0, 18.0, 45, 50),
    ('Tamil Nadu', 73.6, 77.4, 11.7, 15.1, 9.5, 12.6, 55, 60),
    ('West Bengal', 94.5, 102.5, 11.5, 14.2, 13.0, 15.5, 38, 45),
    ('Haryana', 27.5, 31.1, 9.5, 12.4, 12.0, 15.0, 35, 43),
    ('Maharashtra', 118.0, 128.7, 9.2, 11.9, 12.8, 14.0, 35, 43),
    ('Odisha', 43.5, 46.95, 8.0, 12.1, 11.0, 16.0, 35, 45),
    ('Rajasthan', 73.5, 83.1, 4.5, 7.0, 13.0, 18.0, 30, 35)
]

def generate_master_csv(filename='india_diabetes_master.csv'):
    """Generate master DataFrame and save to CSV. Returns the DataFrame."""
    master_df = pd.concat([generate_state_data(*s) for s in states_data])
    master_df.to_csv(filename, index=False)
    return master_df


if __name__ == '__main__':
    df = generate_master_csv()
    print(f"✅ Master Data Generated: {df.shape[0]} rows -> india_diabetes_master.csv")