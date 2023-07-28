# Created by: Christopher Cormier
# Description: Automagically stylizes and aligns text within the constraint.
# Created on: 2023/06/3 - 2023/06/7


# Defining variables:
import math as m

Constraint = 100
BorderStyle = {"Y": ["-", 2], "X": ["|", 4]}
SpecialCharacters = ["%l["]
Direction = ["(L:", "(C:", "(R:"]
Border = False
Section = 0
SectionPadding = 4
ConjoinCharacter = " "
Memory = {0: {}, 1: {}}


# Processing functions:

# Checks if a number can be a float.
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


# Gets the y cord for the section in use for indexing the dictionary in the display() function.
def get_y_cord():
    y = 1
    if len(Memory[Section]) != 0:
        for i in Memory[Section]:
            if i >= y:
                y = i+1
    else:
        if Border and BorderStyle["Y"][1] != 0:
            y = y+1
    return y


def add(item, *override):
    Memory[Section][get_y_cord()] = item


# Sets the border style to the inputted strings.
def set_border_style(*style):
    if len(style) == 2:
        BorderStyle["X"] = [style[0], len((style[0])*2)-2]
        BorderStyle["Y"] = [style[1], len(style[1])*2]
    else:
        BorderStyle["X"] = [style[0], len((style[0])*2)-2]


# Creates a number of blank lines, default = 1.
def spacing(*value):
    xconstraint = Constraint
    if Border:
        xconstraint = xconstraint - BorderStyle["X"][1]
    if len(value) != 0:
        for i in range(0, value[0]):
            add(" " * xconstraint)
    else:
        add(" " * xconstraint)


# Creates a line of the specified style.
# You can plot the line by passing through two number values, i.e 0.5, 1 for a line that is
# half the length of Constraint and extends to the right. You can pass through whole numbers as well,
# as long as they are both whole values.
def line(*style):
    xconstraint = Constraint
    if Border:
        xconstraint = xconstraint - BorderStyle["X"][1]
    if len(style) == 1:
        add((style[0] * xconstraint)[:xconstraint])
    elif len(style) == 3:
        if isfloat(style[1]):
            if isfloat(style[2]):
                if 0 <= float(style[1]) < float(style[2]) <= 1:
                    cords = [m.floor(xconstraint * float(style[1])), m.floor(xconstraint * float(style[2]))]
                elif 0 <= float(style[1]) < float(style[2]) <= xconstraint:
                    cords = [int(style[1]), int(style[2])]
                else:
                    print(style[1], "is larger than:", style[2], "or they exceed range.")
                    return False
                length = abs(cords[0] - cords[1])
                add(" "*cords[0]+(style[0]*length)[:length]+" "*abs(xconstraint-cords[1]))
            else:
                print(style[2], "is not a number.")
        else:
            print(style[1], "is not a number.")
    else:
        add("-" * xconstraint)


# Aligns the strings passed through, enter them from left to right.
# Accepts any amount of string values, you may use 0-1 or 0-Constraint in place of R/C/L for more
# specific placement, fractions are also accepted such as 1/2 for center, it
# should be formatted like so "(.5:", "(1/2:", "(50:" these will all align center, if constraint is 100.
# You may also add "R"/"C"/"L" for the placement, i.e "C" will center the text
# on the placement point. like so: "(R.4:" places it on .4 or 40% with it being
# placed on the right of the specified point.
def align(*values):
    if len(values) != 0:
        processed = ""
        xconstraint = Constraint
        if Border:
            xconstraint = xconstraint - BorderStyle["X"][1]
        for i in values:
            if i[:3].upper() == Direction[0]:
                processed = i[3:]
            elif i[:3].upper() == Direction[1]:
                processed = processed + " " * m.floor((xconstraint-len(i[3:]))/2-len(processed)) + i[3:]
            elif i[:3].upper() == Direction[2]:
                processed = processed + " " * m.floor(xconstraint-len(i[3:])-len(processed)) + i[3:]
            else:
                if i[:0].find("(") and i.find(":"):
                    val = i[i.find("(") + 1:i.find(":", i.find("("))]
                    word_align = "C"
                    for x in Direction:
                        if val[:1].upper() == x[1]:
                            word_align = x[1]
                            val = val[1:]
                    if "/" in val:
                        val = val.split("/")
                    if type(val) == list:
                        if isfloat(val[0]) and isfloat(val[1]):
                            val[0] = float(val[0])
                            val[1] = float(val[1])
                            val = val[0] / val[1]
                        else:
                            print(val[0] + "," + val[1] + " are not numbers.")
                    elif isfloat(val):
                        val = float(val)
                    else:
                        print(val, "is not a number.")
                    if isfloat(val):
                        if val <= 1:
                            if val >= 0:
                                placement = m.ceil(Constraint * val)
                                temp = i[i.find(":")+1:]
                                if placement == Constraint:
                                    processed = processed+" "*m.floor(xconstraint-len(temp)-len(processed))+temp
                                elif placement == 0:
                                    processed = temp
                                else:
                                    if word_align == "C":
                                        processed = processed+" "*m.floor((placement-len(processed))-len(temp)/2)+temp
                                    elif word_align == "L":
                                        processed = processed+" "*m.floor((placement-len(processed))-len(temp)-1)+temp
                                    elif word_align == "R":
                                        processed = processed+" "*m.floor((placement-len(processed)))+temp
                            else:
                                print(val, "exceeds constraint.")
                        elif val <= xconstraint:
                            placement = val
                            temp = i[i.find(":") + 1:]
                            if placement == Constraint:
                                processed = processed + " " * m.floor(xconstraint - len(temp) - len(processed)) + temp
                            elif placement == 0:
                                processed = temp
                            else:
                                if word_align == "C":
                                    processed = processed + " " * m.floor(
                                        (placement - len(processed)) - len(temp) / 2) + temp
                                elif word_align == "L":
                                    processed = processed + " " * m.floor(
                                        (placement - len(processed)) - len(temp) - 1) + temp
                                elif word_align == "R":
                                    processed = processed + " " * m.floor((placement - len(processed))) + temp
                        else:
                            print(val, "exceeds constraint.")
        if len(processed) != xconstraint:
            processed = processed + " " * (xconstraint - len(processed))
        add(processed)


# Compiles all of the strings into one and adds the border if set to true, returns the compiled string.
def display():
    comp = ""
    if Border:
        if len(Memory[1]) == 0:
            comp = BorderStyle["Y"][0] * Constraint
        else:
            comp = BorderStyle["Y"][0] * (Constraint*2+SectionPadding)
    for i in Memory[0]:
        if not Border or len(Memory[0][i]) >= Constraint:
            comp = comp + "\n" + Memory[0][i]
        else:
            comp = comp + "\n" + BorderStyle["X"][0] + " " + Memory[0][i] + " " + BorderStyle["X"][0]
        if i in Memory[1]:
            if comp[len(comp)-Constraint:] == "-"*Constraint and Memory[1][i] == "-"*Constraint:
                comp = comp + "-" * SectionPadding + Memory[1][i]
            else:
                if Border:
                    comp = comp+ConjoinCharacter * SectionPadding+BorderStyle["X"][0]+Memory[1][i]+BorderStyle["X"][0]
                else:
                    comp = comp + ConjoinCharacter * SectionPadding + Memory[1][i]
    if Border:
        if len(Memory[1]) == 0:
            comp = comp + "\n" + BorderStyle["Y"][0] * Constraint
        else:
            comp = comp + "\n" + BorderStyle["Y"][0] * (Constraint*2+SectionPadding)
    Memory[0].clear()
    Memory[1].clear()
    return comp
