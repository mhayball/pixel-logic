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
    for i in range(rows.size):
        dictID = "R", i
        strips[dictID] = Strip("R", i, rows[i], columns.size)

    # cols
    for i in range(columns.size):
        dictID = "C", i
        strips[dictID] = Strip("C", i, columns[i], rows.size)

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

        #print("workingsArray", strips[i].workingsArray)


def checkTable():  # check the strips, attempt to solve table
    for i in strips:

        if strips[i].complete == 0:  # ignore strips that are complete

            for j in range(len(strips[i].workingsArray)):  # check contents of workings array

                if len(strips[i].workingsArray[j]) == 1:  # if only 1 option, then must be correct - mark!
                    element = strips[i].workingsArray[j][0]
                    mark(strips[i], j, strips[i].elements[element].type, element)


def checkTableOLD():  # check the strips, attempt to solve table
    for i in strips:

        if strips[i].complete == 0:  # ignore strips that are complete

            # print("--- Strip ---")
            # print "i", i
            # pprint(vars(strips[i]))

            for j in range(len(strips[i].workingsArray)):  # check workings array

                if len(strips[i].workingsArray[j]) == 1:  # if only 1 option, then mark!
                    element = strips[i].workingsArray[j][0]
                    mark(strips[i], j, strips[i].elements[element].type)

                    # look forward and backward and remove impossibilities from workings given maximum length
                    beforeLocation = max(0, (j - strips[i].elements[element].maximumLength))
                    afterLocation = min(strips[i].length, (j + strips[i].elements[element].maximumLength))

                    for k in range(0, beforeLocation):
                        if element in strips[i].workingsArray[k]: strips[i].workingsArray[k].remove(element)

                    for k in range(afterLocation, strips[i].length):
                        if element in strips[i].workingsArray[k]: strips[i].workingsArray[k].remove(element)

                    # remove elements that are higher/lower as appropriate

                    for k in range(0, j):
                        for l in strips[i].workingsArray[k]:
                            if l > element: strips[i].workingsArray[k].remove(l)

                    for k in range(j, strips[i].length):
                        for l in strips[i].workingsArray[k]:
                            if l < element: strips[i].workingsArray[k].remove(l)

            for j in strips[i].elements:

                if strips[i].elements[j].minimumLength > 0:  # only look at elements that have minimumLength > 0

                    # count how many possible cells
                    counter = 0
                    for k in strips[i].workingsArray:
                        if strips[i].elements[j].ID in k:
                            counter += 1

                    # pprint(vars(strips[i].elements[j]))
                    # print counter

                    if strips[i].elements[
                        j].minimumLength == counter:  # if counter = minimum, then all must be marked and workings updated
                        for k in range(len(strips[i].workingsArray)):
                            if strips[i].elements[j].ID in strips[i].workingsArray[k]:
                                mark(strips[i], k, strips[i].elements[j].type)
                                strips[i].workingsArray[k] = [strips[i].elements[j].ID]


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

        if strip.RC == 'R' and showPlot == 1:
            plot.addFrameToPlotFigure(rows, columns, strips, figure)

        removeWorkings(strip, location, type, element)
        checkWorkings(strip)
        markCorrespondingStrip(strip, location, type)
        checkUnitsIdentifiedInElements(strip)
        checkStrip(strip)


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


def checkStrip(strip):  # check strip to see if it is complete
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


def removeWorkings(strip, location, type, element):  # after a cell has been marked, update and removes workings from said cell

    # print "checkWorkings -", strip.ID, location, strip.workingsArray, strip.workingsArray[location], type

    if not np.isnan(element): # if element is known, then simply replace workingsArray with the given element

        strip.workingsArray[location] = [element]

    else: # if element isn't known, then remove possible elements that don't have the same type

        delWorkingsArrayLocations = []  # empty array for identifying which elements are removed from the workings

        print("test", strip.workingsArray[location])

        print(len(strip.workingsArray[location]))

        for i in range(len(strip.workingsArray[location])):

            element = strip.workingsArray[location][i]

            # print " - element", element, strip.elements[element].type

            if strip.elements[
                element].type != type:  # if type of suggested element doesn't match what's been marked, then add to delete array
                # print " - element type:", strip.elements[element].type, "type:", type, i, strip.workingsArray[location]
                # print " - ", strip.workingsArray[location][i]
                delWorkingsArrayLocations.append(i)

        delWorkingsArrayLocations.sort(reverse=True)  # work in reverse order to not mess up the locations.

        # print " - delWorkingsArrayLocations", delWorkingsArrayLocations

        for j in range(len(delWorkingsArrayLocations)):  # delete from the workingsArray
            delete = delWorkingsArrayLocations[j]
            # print " - delete:", j, delete
            del strip.workingsArray[location][delete]

        # print " - checked Workings", strip.ID, location, strip.workingsArray, strip.workingsArray[location], type


def checkWorkings(strip):

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

    global showPlot, strips, rows, columns

    rows = np.array(inputRows)
    columns = np.array(inputColumns)
    showPlot = inputShowPlot

    strips = setup(rows, columns)


    """
    for i in strips:

        printStrip(strips[i].RC, strips[i].ID)

        print(strips[i].ID, strips[i].RC, strips[i].inputArray)
        for j in strips[i].elements:
            print(strips[i].elements[j].ID, strips[i].elements[j].minimumLength, strips[i].elements[j].maximumLength)

    """

    if showPlot == 1:
        global figure
        figure = plot.setupPlotFigure(rows, columns, strips)

    firstPass()

    print("--------start of first pass---------")

    for i in strips:
        printStrip(strips[i].RC, strips[i].ID)

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


    if showPlot == 1:
        plot.showPlotFigure(figure)

    for i in strips:
        printStrip(strips[i].RC, strips[i].ID)

    return output()