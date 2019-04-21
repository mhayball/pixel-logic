import numpy as np
import plot
from pprint import pprint

class Strip:
    def __init__(self, RC, ID, inputArray, length):
        self.RC = RC
        self.ID = ID
        self.inputArray = inputArray
        self.length = length
        self.elements = dict()

        self.workingsArray = [np.nan] * length
        self.outputArray = [np.nan] * length
        self.complete = 0
        self.noOfElements = 1

        for i in range(len(self.workingsArray)):
            self.workingsArray[i] = []

    class Element:
        def __init__(self, ID, minimumLength, type):
            self.ID = ID
            self.minimumLength = minimumLength
            self.type = type # 1 = marked, 0 = blank
            self.complete = 0
            self.unitsIdentified = 0


def setup(rows, columns):  # setup initial strips
    # size = [rows.size, columns.size]
    # print size
    strips = dict()

    # rows
    for i in range(len(rows)):
        dictID = "R", i
        strips[dictID] = Strip("R", i, rows[i], len(columns))

    # cols
    for i in range(len(columns)):
        dictID = "C", i
        strips[dictID] = Strip("C", i, columns[i], len(rows))

    # set up elements
    for i in strips:

        if strips[i].inputArray[0] == 0: # special case if strip is 0 e.g. blank

            strips[i].elements[0] = strips[i].Element(0, strips[i].length, 0)

        else:

            # first element could be zero length
            strips[i].elements[0] = strips[i].Element(0, 0, 0)

            x = 1  # counter
            for j in range(0, len(strips[i].inputArray)):
                if j != 0:  # already put in place first element above, otherwise, put in space with minimum length of 1:
                    strips[i].elements[x] = strips[i].Element(x, 1, 0)
                    x += 1

                strips[i].elements[x] = strips[i].Element(x, strips[i].inputArray[j], 1)
                x += 1

            # final element could be zero length
            strips[i].elements[x] = strips[i].Element(x, 0, 0)
            strips[i].noOfElements = x+1

        # set up maximum lengths
        totalMinimumLength = 0
        for j in strips[i].elements:
            totalMinimumLength = totalMinimumLength + strips[i].elements[j].minimumLength

        strips[i].minimumLength = totalMinimumLength
        # print totalMinimumLength

        for j in strips[i].elements:
            if strips[i].elements[j].type == 1:
                strips[i].elements[j].maximumLength = strips[i].elements[j].minimumLength
            else:
                strips[i].elements[j].maximumLength = strips[i].length - totalMinimumLength + strips[i].elements[
                    j].minimumLength

    return strips


def firstPass():  # first check of strips following setup

    # add workings
    # possibleArray shows possible positions of elements based on minimum length
    # all permutations of possibleArray are considered and then added to workingsArray

    for i in strips:

        #printStrip(strips[i].RC, strips[i].ID)

        if strips[i].inputArray[0] == 0:  # special case if strip is 0 e.g. blank

            strips[i].workingsArray = [[0]] * strips[i].length
        else:

            for j in range(0, strips[i].elements[0].maximumLength + 1): # loop through possible options

                possibleArray = [np.nan] * strips[i].length

                x = j

                if x > 0: # adds first element (0) as possible options
                    for k in range(0, x + 1):
                        possibleArray[k] = 0

                for k in range(0, len(strips[i].elements)): # loop through all elements

                    for l in range(0, strips[i].elements[k].minimumLength): # loop through length of given element

                        possibleArray[x] = strips[i].elements[k].ID
                        x = x + 1

                if x < strips[i].length: # adds last element as possible option
                    for k in range(x, strips[i].length):
                        possibleArray[k] = strips[i].elements[strips[i].noOfElements - 1].ID

                # possibleArray is now complete, now to add to workingsArray

                for k in range(0, len(possibleArray)):

                    if possibleArray[k] not in strips[i].workingsArray[k] and not np.isnan(possibleArray[k]):
                        strips[i].workingsArray[k].append(possibleArray[k])


def checkTable():  # check the strips, attempt to solve table
    for i in strips:

        if strips[i].complete == 0:  # ignore strips that are complete

            for j in range(len(strips[i].workingsArray)):  # check contents of workings array

                if len(strips[i].workingsArray[j]) == 1:  # if only 1 option, then must be correct - mark!
                    element = strips[i].workingsArray[j][0]
                    mark(strips[i], j, strips[i].elements[element].type, element)


def printStrip(RC, number):  # print strip - handy debug function
    i = (RC, number)
    pprint(vars(strips[i]))
    for j in strips[i].elements:
        pprint(vars(strips[i].elements[j]))


def mark(strip, location, type, element = np.nan):  # marks a unit in a strip at location, with type

    if strip.outputArray[location] == 0 and type == 1:
        print("error")
    elif strip.outputArray[location] == 1 and type == 0:
        print("error")
    elif strip.outputArray[location] == type:  # already marked, so do nothing
        # print("already marked")
        pass
    else:  # mark the unit
        # print "marked - location:", location, "type:", type

        strip.outputArray[location] = type  # mark the unit

        removeWorkings(strip, location, type, element)
        checkWorkings(strip)
        checkUnitsIdentifiedInElements(strip)

        if strip.RC == 'R' and showPlot == 1:
            plot.addFrameToPlotFigure(rows, columns, strips, figure, showWorkings)

        markCorrespondingStrip(strip, location, type)
        checkStripComplete(strip)


def markCorrespondingStrip(strip, location, type):  # find corresponding unit in row/column strip
    # e.g. if RC = C, strip.id = 8 and location = 9, then look for RC = R, ID = location, location = ID

    # print("correspondingStrip -"), strip.ID, location, strip.RC
    # print strips

    if strip.RC == 'R':
        correspondingDictID = 'C', location
    elif strip.RC == 'C':
        correspondingDictID = 'R', location

    if correspondingDictID in strips:
        # print "found correspondingDictID", correspondingDictID
        mark(strips[correspondingDictID], strip.ID, type)


def checkStripComplete(strip):  # check strip to see if it is complete
    # print "check"
    stripInputSum = np.nansum(strip.inputArray)
    stripOutputSum = np.nansum(strip.outputArray)

    if stripInputSum == stripOutputSum:  # strip is complete
        strip.complete = 1

        for i in range(len(strip.outputArray)):
            # print "removing nan", strip.outputArray[i], np.nan
            if np.isnan(strip.outputArray[i]):
                # print "removing nan", strip.outputArray[i]
                mark(strip, i, 0)


def isItOdd(x):
    if x % 2 > 0:
        return True
    else:
        return False


def removeWorkings(strip, location, type, element):  # after a cell has been marked, update and removes workings from said cell

    if not np.isnan(element): # if element is known, then simply replace workingsArray with the given element

        strip.workingsArray[location] = [element]

    else: # if element isn't known, then remove possible elements that don't have the same type

        for i in range(len(strip.workingsArray[location]) -1, -1, -1): # if type = 0, then only elements with an even number can be correct
            if isItOdd(strip.workingsArray[location][i]) and type == 0:
                del strip.workingsArray[location][i]
            elif not isItOdd(strip.workingsArray[location][i]) and type == 1:
                del strip.workingsArray[location][i]


def checkWorkings(strip):

    checkWorkingsElements(strip)

    #printStrip(strip.RC, strip.ID)

    for i in range(len(strip.workingsArray)):
        if strip.complete != 1:

            #print(strip.workingsArray[i])

            minElement = min(strip.workingsArray[i])
            maxElement = max(strip.workingsArray[i])

            for j in range(0, i):  # if there are any workings elements greater than the maxElement, prior to j, remove them
                minElement = min(strip.workingsArray[i])
                maxElement = max(strip.workingsArray[i])
                #print("test")

            for j in range(i, len(strip.workingsArray)):  # if there are any workings elements less than the minElement, after j, remove them
                minElement = min(strip.workingsArray[i])
                maxElement = max(strip.workingsArray[i])
                #print("test")


def checkWorkingsElements(strip):
    # count how many times element has been identified in workingsArray
    # if this equals the minimum length of said element, then said units must contain that element. Update workingsArray

    for element in strip.elements:
        howManyTimesIdentified = 0
        for i in range(len(strip.workingsArray)):
            if strip.elements[element].ID in strip.workingsArray[i]: howManyTimesIdentified += 1

        if howManyTimesIdentified == strip.elements[element].minimumLength:
            for i in range(len(strip.workingsArray)):
                if strip.elements[element].ID in strip.workingsArray[i]: strip.workingsArray[i] = [strip.elements[element].ID]


def checkUnitsIdentifiedInElements(strip):  # how many units of an element have been identified? Across a whole strip.
    for element in strip.elements:  # reset to zero
        strip.elements[element].unitsIdentified = 0

    for i in range(len(strip.workingsArray)):
        if len(strip.workingsArray[i]) == 1:
            element = strip.workingsArray[i][0]
            strip.elements[element].unitsIdentified += 1

    for element in strip.elements:
        # if unitsIdentified = max, then element is complete
        if strip.elements[element].unitsIdentified == strip.elements[element].maximumLength:
            completeElement(strip, strip.elements[element])

            """ this currently doesn't work
            # if element not in workingsArray, then doesn't exist and must be complete
            if strip.elements[element].ID not in strip.workingsArray:
                strip.elements[element].complete = 1
            """


def completeElement(strip, element):
    if element.complete == 0:  # mark element as complete, and do stuff!
        element.complete = 1

        for j in range(len(strip.workingsArray)):  # remove element from OTHER workingsArray
            if element.ID in strip.workingsArray[j] and len(strip.workingsArray[j]) > 1:
                strip.workingsArray[j].remove(element.ID)

        # check units before and after a complete element, and remove any of same type (as type must be different)
        for j in range(len(strip.workingsArray)):
            if element.ID in strip.workingsArray[j] and len(strip.workingsArray[j]) == 1:
                beforeAndAfter = [max(0, j - 1), min(j + 1, strip.length - 1)]
                for k in beforeAndAfter:
                    for l in strip.workingsArray[k]:
                        if strip.elements[l].type == element.type and l != element.ID:
                            strip.workingsArray[k].remove(l)


def output():

    output = []

    for i in strips:
        if strips[i].RC =='R':
            output.append(strips[i].outputArray)

    return output


def solver(inputRows, inputColumns, inputShowPlot):

    global showPlot, showWorkings, strips, rows, columns

    rows = np.array(inputRows)
    columns = np.array(inputColumns)
    showPlot = inputShowPlot
    showWorkings = True

    strips = setup(rows, columns)


    """
    for i in strips:

        printStrip(strips[i].RC, strips[i].ID)

        print(strips[i].ID, strips[i].RC, strips[i].inputArray)
        for j in strips[i].elements:
            print(strips[i].elements[j].ID, strips[i].elements[j].minimumLength, strips[i].elements[j].maximumLength)

    """

    if showPlot == 1: # frame 0 shows set up
        global figure
        figure = plot.setupPlotFigure(rows, columns, strips, showWorkings)

    firstPass()

    if showPlot == 1 and showWorkings == 1: # frame 1 will then shows workings
        plot.addFrameToPlotFigure(rows, columns, strips, figure, showWorkings)

    print("--------start of first pass---------")

    """
    for i in strips:
        printStrip(strips[i].RC, strips[i].ID)
    """

    print("--------end of first pass---------")

    i = 1
    longstop = 10
    tableComplete = 0

    while i < longstop:

        if tableComplete == 1: i = longstop  # use this to do one final check!

        checkTable()

        # have all strips been completed?
        tableComplete = 1
        for j in strips:
            if strips[j].complete == 0: tableComplete = 0

        i += 1


    if showPlot == 1: # final frame for completeness
        plot.addFrameToPlotFigure(rows, columns, strips, figure, showWorkings)
        plot.showPlotFigure(figure)

    """
    for i in strips:
        printStrip(strips[i].RC, strips[i].ID)
    """

    if tableComplete == 1:
        return ["tableComplete", output()]
    else:
        return ["tableNotComplete", output()]