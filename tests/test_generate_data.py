import os
import pandas as pd
import pytest
from generate_data import generate_state_data, generate_master_csv


def test_generate_state_data_structure():
    df = generate_state_data('Test', 1.0, 1.0, 10.0, 10.0, 5.0, 5.0, 50, 50)
    expected_cols = {
        'State', 'Year', 'Population_Millions', 'Diabetes_Prev_Pct',
        'Pre_Diabetes_Prev_Pct', 'Diagnosis_Rate_Pct', 'Total_Diabetics_Millions',
        'Total_Pre_Diabetics_Millions', 'Diagnosed_Millions', 'Undiagnosed_Millions'
    }
    assert expected_cols.issubset(set(df.columns))
    assert df.shape[0] == 11  # 2015-2025 inclusive
    # Spot-check calculation
    calculated = round(df['Population_Millions'].iloc[0] * df['Diabetes_Prev_Pct'].iloc[0] / 100, 3)
    assert df['Total_Diabetics_Millions'].iloc[0] == calculated


def test_generate_master_csv_creates_file(tmp_path):
    csv_file = tmp_path / 'test_master.csv'
    df = generate_master_csv(str(csv_file))
    assert csv_file.exists()
    assert csv_file.stat().st_size > 0
    assert len(df) > 0
