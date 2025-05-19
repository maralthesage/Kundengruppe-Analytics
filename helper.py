import datetime as dt
import pandas as pd

from datetime import datetime, date

def assign_age(aa):
    current_date = dt.datetime.now()
    aa['GEBURT'] = aa['GEBURT'].fillna("")
    aa['AGE'] = aa['GEBURT'].apply(lambda x: current_date.year - x.year - ((current_date.month, current_date.day) < (x.month, x.day)))

    # Define age groups
    def assign_age_group(age):
        if age <= 18:
            return "0-18"
        elif age <= 30:
            return "19-30"
        elif age <= 50:
            return "31-50"
        elif age <= 65:
            return "51-65"
        elif age >= 65:
            return "65+"
        else:
            return "NA"

    aa['AGE_GROUP'] = aa['AGE'].apply(assign_age_group)
    return aa


def process_id(data):
    data = data.astype(str)
    data = data.replace(".0","")
    data = data.str.zfill(10)
    return data

def process_date(data):
    return pd.to_datetime(data,format='mixed',errors='coerce')



def get_half_year_info(today: date = None):
    if today is None:
        today = date.today()
    
    # Base reference: H1 2025 -> number 49
    base_half_year_start = date(2025, 1, 1)
    base_number = 49

    # Determine if we're in H1 or H2
    if today.month <= 6:
        # H1 of current year
        current_half_index = 0
    else:
        # H2 of current year
        current_half_index = 1

    # Total number of half years since base
    years_diff = today.year - base_half_year_start.year
    half_year_offset = years_diff * 2 + current_half_index

    # Calculated number
    number = base_number + half_year_offset

    # Determine previous half-year
    if current_half_index == 0:
        # If we're in H1, previous half-year is H2 of last year
        prev_start = date(today.year - 1, 7, 1)
        prev_end = date(today.year - 1, 12, 31)
    else:
        # If we're in H2, previous half-year is H1 of same year
        prev_start = date(today.year, 1, 1)
        prev_end = date(today.year, 6, 30)

    return {
        'number': number,
        'prev_start': prev_start,
        'prev_end': prev_end
    }
