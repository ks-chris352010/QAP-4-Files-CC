# Written by: Christopher Cormier
# Written on: 2023/07/20
# Description: Takes in sales numbers for each month of the year and forms them into a graph.

# Imports:
from Modules.Validizer import Validate as V
from Modules.Validizer import Month_Names
import matplotlib.pyplot as plt

# Defining variables:
YAxis = []
XAxis = [i[:3] for i in Month_Names]
# List comprehension, converts Month_Names which is full month names to partial.

# Processing:
for i in Month_Names:
    YAxis.append(V(V.number, f"Enter the total sales for {i}: ").V)
    # Asks for and adds the sale number for the list using the Validizer.

# Output:
plt.plot(XAxis, YAxis)
plt.title('Sales from January-December:')
plt.xlabel('Months')
plt.ylabel('Sales($)')
plt.show()
