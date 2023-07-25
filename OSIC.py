# Written by: Christopher Cormier
# Written on: 18/07/2023-19/07/2023
# Description: Calculates and logs policies forming them into a neat receipt.

# Imports:
from Modules.Validizer import Validate as V
from datetime import datetime
from tqdm import tqdm
from time import sleep
import Modules.Stylier as Sty

# Defining variables and loading defaults:
Provinces = [
    "AB",
    "MB",
    "BC",
    "NB",
    "NL",
    "NS",
    "NT",
    "NU",
    "ON",
    "PE",
    "QC",
    "SK",
    "YT"
]
Values = []
# Values 0-7 are equal to the values within OSICDef.dat in order left to right.
Policies = {}
with open("OSICDef.dat", "r") as f:
    for i in f.read().split(" "):
        # Using my number validation to convert to number since it returns what is put in so that 23 won't become 23.0
        Values.append(V.number(i)[1])
    # Splits the string read from OSICDef into values at every point where a space appears.
# Uses the with statement to open the file which closes it after executing code in block.
while True:
    Policies[Values[0]] = []
    # Defines a list within the Policies dictionary.

    # Inputs and validations:
    print("Please enter customer's information as requested: ")
    CFirstName = V(V.name, "First name: ").V
    Policies[Values[0]].append(CFirstName)
    # Saves each policy value to a list value in a dictionary which is equal to the current policy number.
    CLastName = V(V.name, "Last name: ").V
    Policies[Values[0]].append(CLastName)
    CAddress = V(V.name, "Address: ", set("ABCDEFGHIJKLMNOPQRSTUVWXYZ.,'-1234567890 ")).V
    # Made it so you can pass through a set into name validation in case you need more characters such as numbers.
    Policies[Values[0]].append(CAddress)
    CCity = V(V.name, "City: ").V
    Policies[Values[0]].append(CCity)
    CProvince = V(V.string, "Province: ", Provinces).V
    Policies[Values[0]].append(CProvince)
    CPostalCode = V(V.postal_code, "Postal code: ").V
    Policies[Values[0]].append(CPostalCode)
    CPhoneNumber = V(V.phone_number, "Phone number: ").V
    Policies[Values[0]].append(CPhoneNumber)
    CarNumber = V(V.number, "Number of cars being insured: ", "int").V
    Policies[Values[0]].append(CarNumber)
    ExtraLiability = V(V.string, "Extra liability up to $1,000,000 (Y/N): ", "Y,N").V
    Policies[Values[0]].append(ExtraLiability)
    GlassCoverage = V(V.string, "Glass coverage (Y/N): ", "Y,N").V
    Policies[Values[0]].append(GlassCoverage)
    LoanerCar = V(V.string, "Loaner car (Y/N): ", "Y,N").V
    Policies[Values[0]].append(LoanerCar)
    PaymentType = V(V.string, "Full or monthly payment: ", ["Full", "Monthly"]).V
    Policies[Values[0]].append(PaymentType)
    # The .V after every value is because the class gives each object 3-4 values but I only needed the formatted value.
    # .V for formatted value.
    # .UP for unprocessed value (useful if you want to validate a number for an id like 014).
    # .NV for number value if applicable (for when you set number validation to return cash value).
    # .T for type, less useful is equal to function name _ removed adjusted to title case.

    # Processing
    InsurancePremium = Values[1] + (Values[1]-(Values[1] * Values[2]) * (CarNumber-1))
    ExtraCost = 0
    if ExtraLiability == "Y":
        ExtraCost += Values[3] * CarNumber
    if GlassCoverage == "Y":
        ExtraCost += Values[4] * CarNumber
    if LoanerCar == "Y":
        ExtraCost += Values[5] * CarNumber
    TotalInsurancePremium = InsurancePremium + ExtraCost
    Policies[Values[0]].append(TotalInsurancePremium)
    HST = TotalInsurancePremium * Values[6]
    TotalCost = TotalInsurancePremium + HST
    Payment = TotalCost
    if PaymentType == "Monthly":
        Payment = (TotalCost + Values[7])/8
    InvoiceDate = datetime.now().strftime("%Y-%m-%d")
    Processed = InvoiceDate.split("-")
    if Processed[1] == "12":
        Processed[1] = "01"
    elif int(Processed[1]) >= 9:
        Processed[1] = int(Processed[1]) + 1
    else:
        Processed[1] = f"0{int(Processed[1])+1}"
    Processed[2] = "01"
    NextPayDate = f"{Processed[0]}-{Processed[1]}-{Processed[2]}"

    # Output:
    Sty.Border = True
    Sty.Constraint = 45
    for i in range(0, 50):
        print()
    Sty.align("(C:One Stop Insurance Company")
    Sty.line()
    Sty.align("(L:Policy number:", f"(R:{Values[0]}")
    Sty.align("(L:Name:", f"(R:{CFirstName} {CLastName}")
    Sty.spacing()
    Sty.align("(L:Address:", f"(R:{CAddress}, {CPostalCode}")
    Sty.align(f"(R:{CCity}, {CProvince}")
    Sty.align("(L:Phone number:", f"(R:{CPhoneNumber}")
    Sty.line()
    Sty.align(f"(C:Payment plan: {PaymentType}")
    Sty.align(f"(C:Extra Liability: {ExtraLiability}")
    Sty.align(f"(C:Glass Coverage: {GlassCoverage}")
    Sty.align(f"(C:Loaner Car: {LoanerCar}")
    Sty.line()
    Sty.align("(L:Car Amount:", f"(R:{CarNumber}")
    Sty.align("(L:Insurance Premium:", f"(R:${InsurancePremium:,.2f}")
    if ExtraCost > 0:
        Sty.align("(L:Extra cost:", f"(R:${ExtraCost:,.2f}")
        Sty.align("(L:Subtotal:", f"(R:${TotalInsurancePremium:,.2f}")
    Sty.align("(L:HST:", f"(R:${HST:.2f}")
    Sty.align("(L:Total:", f"(R:${TotalCost:,.2f}")
    if PaymentType == "Monthly":
        Sty.line()
        Sty.align("(L:Monthly Payment:", f"(R:${Payment:.2f}")
        Sty.align(f"(L:Next payment due:", f"(R:{NextPayDate}")
    Sty.line()
    Sty.align("(L:Invoice date:", f"(R:{InvoiceDate}")
    # Stylier module is really good at making receipts.
    print(Sty.display())
    Values[0] += 1

    # Saving and end prompt.
    End = V(V.string, "Continue filing? (Y/N): ", "Y,N").V
    if End == "N":
        comp = ""
        for i in Values:
            comp = f"{comp} {i}"
        with open("OSICDef.dat", "w") as f:
            f.write(comp[1:])
        # Compiles Values into a string and saves them.
        comp = ""
        for i in Policies:
            comp = f"\n{comp}\n{i}, {InvoiceDate}"
            for x in Policies[i]:
                comp = f"{comp}, {x}"
        with open("Policies.dat", "a") as f:
            f.write(comp[2:])
        # Compiles Policies into a string and saves them.
        for i in tqdm(range(0, 10), ncols=100, desc="Writing data: "):
            sleep(.1)
        # Creates a loading bar.
        break
