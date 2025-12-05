def val_age(age_str):
    """
    validate age(10-130)
    """
    try:
        age = float(age_str)
        if age < 10 or age > 130:
            return False, "Age must be between 10 and 130"
        return True, age
    except:
        return False, "Age must be a valid number"
    
def val_bmi(bmi_str):
    """
    Validate BMI (10 - 70)
    """
    try:
        bmi = float(bmi_str)
        if bmi < 10 or bmi > 70:
            return False, "BMI must be between 10 and 70"
        return True, bmi
    except:
        return False, "BMI must be valid number"
def val_glucose(glucose_str):
    """
    Validate glucose level (40-300)
    """
    try:
        glucose = float(glucose_str)
        if glucose < 40 or glucose > 300:
            return False, "Glucose must be between 40 and 300"
        return True, glucose
    except:
        return False, "Glucose must be a valid number"
def val_binary(value_str, field_name):
    """
    Validate 0 or 1
    """
    if value_str not in ['0', '1']:
        return False, f"{field_name} must be 0 or 1"
    return True, int(value_str)
def val_required(value, field_name):
    """ 
    check field  is not empty
    """
    if not value or not str(value).strip():
        return False, f"{field_name} is required"
    return True, str(value).strip()
           
         

