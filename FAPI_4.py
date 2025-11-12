#frontend/FAPI_Fourth.py


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

#app = FastAPI()

# Add this new route
@app.get("/hello")
def read_hello():
    return {"message": "Hello from FastAPI!", "status": "Backend is operational"}

# =======================================================================
# 1. TAX DATA STRUCTURE (MASTER_TAX_SCHEDULE)
#    (All the individual lists/data structures remain exactly the same)
# ... (Paste the entire MASTER_TAX_SCHEDULE definition here) ...
# =======================================================================

# --- IMPORTANT: Paste all the tax bracket lists here (e.g., employment_tax_brackets_before_2025) ---
# ... (All data from Step 1 of the previous answer) ... 

# --- THE MASTER TAX TABLE DICTIONARY ---
# (I'll just paste the complete dictionary placeholder to keep this answer clean)

MASTER_TAX_SCHEDULE = {
    "Before 2025 Revision": {
        "Income from employment": [
            {"min_income": 0, "max_income": 600, "deduction": 0.00, "rate": 0.00},
            {"min_income": 601, "max_income": 1650, "deduction": 60.00, "rate": 0.10},
            {"min_income": 1651, "max_income": 3200, "deduction": 142.50, "rate": 0.15},
            {"min_income": 3201, "max_income": 5250, "deduction": 302.50, "rate": 0.20},
            {"min_income": 5251, "max_income": 7800, "deduction": 565.00, "rate": 0.25},
            {"min_income": 7801, "max_income": 10900, "deduction": 955.00, "rate": 0.30},
            {"min_income": 10901, "max_income": float('inf'), "deduction": 1500.00, "rate": 0.35},
        ],
        "Income from rental of buildings": [
            {"min_income": 0, "max_income": 7200, "deduction": 0.00, "rate": 0.00},
            {"min_income": 7201, "max_income": 19800, "deduction": 720.00, "rate": 0.10},
            {"min_income": 19801, "max_income": 38400, "deduction": 1710.00, "rate": 0.15},
            {"min_income": 38401, "max_income": 63000, "deduction": 3630.00, "rate": 0.20},
            {"min_income": 63001, "max_income": 93600, "deduction": 6780.00, "rate": 0.25},
            {"min_income": 93601, "max_income": 130800, "deduction": 11460.00, "rate": 0.30},
            {"min_income": 130801, "max_income": float('inf'), "deduction": 18000.00, "rate": 0.35},
        ],
        "Income from Business": [
            {"min_income": 0, "max_income": 7200, "deduction": 0.00, "rate": 0.00},
            {"min_income": 7201, "max_income": 19800, "deduction": 720.00, "rate": 0.10},
            {"min_income": 19801, "max_income": 38400, "deduction": 1710.00, "rate": 0.15},
            {"min_income": 38401, "max_income": 63000, "deduction": 3630.00, "rate": 0.20},
            {"min_income": 63001, "max_income": 93600, "deduction": 6780.00, "rate": 0.25},
            {"min_income": 93601, "max_income": 130800, "deduction": 11460.00, "rate": 0.30},
            {"min_income": 130801, "max_income": float('inf'), "deduction": 18000.00, "rate": 0.35},
        ],
        # Fixed-rate categories (Before)
        "Income from Technical Services": {"type": "fixed", "rate": 0.10},
        "Income from Dividends": {"type": "fixed", "rate": 0.10},
        "Income from Rental of Property (Fixed)": {"type": "fixed", "rate": 0.15},
        "Income from Interest on Deposits": {"type": "fixed", "rate": 0.05},
        "Income from Games of Chance": {"type": "fixed", "rate": 0.15},
        "Income from Royalties": {"type": "fixed", "rate": 0.05},
    },

    "After 2025 Revision": {
        "Employment Income (Monthly)": [
            {"min_income": 0, "max_income": 2000, "deduction": 0.00, "rate": 0.00},
            {"min_income": 2001, "max_income": 4000, "deduction": 300.00, "rate": 0.15},
            {"min_income": 4001, "max_income": 7000, "deduction": 500.00, "rate": 0.20},
            {"min_income": 7001, "max_income": 10000, "deduction": 850.00, "rate": 0.25},
            {"min_income": 10001, "max_income": 14000, "deduction": 1350.00, "rate": 0.30},
            {"min_income": 14001, "max_income": float('inf'), "deduction": 2050.00, "rate": 0.35},
        ],
        "Rental Income (Annual)": [
            {"min_income": 0, "max_income": 24000, "deduction": 0.00, "rate": 0.00},
            {"min_income": 24001, "max_income": 48000, "deduction": 0.00, "rate": 0.15},
            {"min_income": 48001, "max_income": 84000, "deduction": 0.00, "rate": 0.20},
            {"min_income": 84001, "max_income": 120000, "deduction": 0.00, "rate": 0.25},
            {"min_income": 120001, "max_income": 168000, "deduction": 0.00, "rate": 0.30},
            {"min_income": 168001, "max_income": float('inf'), "deduction": 0.00, "rate": 0.35},
        ],
        "Business Income (Annual)": [
            {"min_income": 0, "max_income": 24000, "deduction": 0.00, "rate": 0.00},
            {"min_income": 24001, "max_income": 48000, "deduction": 0.00, "rate": 0.15},
            {"min_income": 48001, "max_income": 84000, "deduction": 0.00, "rate": 0.20},
            {"min_income": 84001, "max_income": 120000, "deduction": 0.00, "rate": 0.25},
            {"min_income": 120001, "max_income": 168000, "deduction": 0.00, "rate": 0.30},
            {"min_income": 168001, "max_income": float('inf'), "deduction": 0.00, "rate": 0.35},
        ],
        "Category B - Tax on annual gross sales": [
            {"min_income": 0, "max_income": 100000, "deduction": 0.00, "rate": 0.02},
            {"min_income": 100001, "max_income": 500000, "deduction": 0.00, "rate": 0.03},
            {"min_income": 500001, "max_income": 1000000, "deduction": 0.00, "rate": 0.05},
            {"min_income": 1000001, "max_income": 1500000, "deduction": 0.00, "rate": 0.07},
            {"min_income": 1500001, "max_income": 2000000, "deduction": 0.00, "rate": 0.09},
        ],
        
        # Fixed-rate categories (After)
        "Dividends": {"type": "fixed", "rate": 0.10},
        "Royalties": {"type": "fixed", "rate": 0.15},
        "Games of Chance": {"type": "fixed", "rate": 0.20},
        "Capital Gains (Immovable Property - Class A)": {"type": "fixed", "rate": 0.15},
        "Capital Gains (Shares/Bonds - Class B)": {"type": "fixed", "rate": 0.15},
        "Income From Digital Content Creation": {"type": "fixed", "rate": 0.15},
        "Royalties Related to Art and Culture": {"type": "fixed", "rate": 0.05},
        "Entertainer Performance Taking Place in Ethiopia": {"type": "fixed", "rate": 0.15},
        "Management or Technical Services Fee": {"type": "fixed", "rate": 0.15},
        "Insurance Premium": {"type": "fixed", "rate": 0.10}, 
        "Interest on Deposits": {"type": "fixed", "rate": 0.10},
        "Offshore Indirect Transfers (Gains From Ethiopia)": {"type": "fixed", "rate": 0.15},
    }
}


# =======================================================================
# 2. CALCULATION LOGIC (Functions remain the same)
# =======================================================================

def calculate_tax(income, tax_data):
    """Calculates the tax payable based on the income and the specific tax data."""
    if isinstance(tax_data, dict) and tax_data.get("type") == "fixed":
        tax = income * tax_data["rate"]
        return max(0, tax)
    elif isinstance(tax_data, list):
        for bracket in tax_data:
            min_income = bracket["min_income"]
            max_income = bracket["max_income"]
            if min_income <= income <= max_income:
                tax = (income * bracket["rate"]) - bracket["deduction"]
                return max(0, tax)
        return 0.0
    else:
        # Should be caught by the API endpoint's logic
        return 0.0


def handle_calculation(revision_key, category_key, income_amount):
    """The main controller function that links the selections to the calculation."""
    tax_data = MASTER_TAX_SCHEDULE[revision_key][category_key]
    tax_payable = calculate_tax(income_amount, tax_data)
    
    # Determine the final rate and deduction for display
    if isinstance(tax_data, dict) and tax_data.get("type") == "fixed":
        final_rate = tax_data["rate"]
        deduction_used = 0.0
    elif isinstance(tax_data, list):
        final_rate = 0.0
        deduction_used = 0.0
        for bracket in tax_data:
            if income_amount >= bracket["min_income"] and income_amount <= bracket["max_income"]:
                final_rate = bracket["rate"]
                deduction_used = bracket["deduction"]
                break
    
    return tax_payable, final_rate * 100, deduction_used


# =======================================================================
# 3. FASTAPI IMPLEMENTATION
# =======================================================================

app = FastAPI(
    title="Ethiopian Tax Calculation API",
    description="API for calculating various Ethiopian taxes based on Revision and Category."
)

# Pydantic model for the response object
class TaxCalculationResponse(BaseModel):
    tax_payable: float
    applicable_rate_percent: float
    deduction_used: float

# Endpoint to get all valid revision and category keys
@app.get("/tax/metadata", summary="Get all valid revisions and categories")
async def get_tax_metadata():
    """Returns the structure of the tax schedule for populating client dropdowns."""
    return MASTER_TAX_SCHEDULE

# Endpoint for the calculation
@app.get("/tax/calculate", response_model=TaxCalculationResponse, summary="Calculate tax for a given income, revision, and category")
async def calculate_tax_endpoint(
    revision: str, 
    category: str, 
    income: float
):
    """
    Calculates the tax payable based on the provided revision, category, and income.
    """
    
    # Validation
    if revision not in MASTER_TAX_SCHEDULE:
        raise HTTPException(status_code=400, detail=f"Invalid revision: '{revision}'. Must be one of: {list(MASTER_TAX_SCHEDULE.keys())}")
        
    if category not in MASTER_TAX_SCHEDULE[revision]:
        raise HTTPException(status_code=400, detail=f"Invalid category for revision '{revision}'. Must be one of: {list(MASTER_TAX_SCHEDULE[revision].keys())}")
        
    if income < 0:
        raise HTTPException(status_code=400, detail="Income cannot be negative.")

    # Core Calculation
    tax, rate_percent, deduction = handle_calculation(revision, category, income)
    
    return TaxCalculationResponse(
        tax_payable=round(tax, 2),
        applicable_rate_percent=round(rate_percent, 2),
        deduction_used=round(deduction, 2)
    )

# To run the application:
# 1. Save the code as a Python file (e.g., 'tax_api.py').
# 2. Run the command in your terminal: 
#    uvicorn tax_api:app --reload

# The API will be available at http://127.0.0.1:8000
# You can test the endpoints in your browser at http://127.0.0.1:8000/docs
