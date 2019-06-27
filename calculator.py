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
        self.workingsPermutations = dict()
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

    class WorkingsPermutations:
        def __init__(self, ID, workingsArray):
            self.ID = ID
            self.workingsArray = workingsArray


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

                else: # are all options in the workings array of the same type (e.g. odd or even)

                    odd = True
                    even = True

                    for k in range(len(strips[i].workingsArray[j])):
                        if isItOdd(strips[i].workingsArray[j][k]):
                            odd *= True
                            even *= False
                        else:
                            odd *= False
                            even *= True

                    if odd:
                        mark(strips[i], j, 1)
                    if even:
                        mark(strips[i], j, 0)


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

    #printStrip(strip.RC, strip.ID)

    checkWorkingsElementsCount(strip)
    checkWorkingsElementsPositions(strip)
    checkWorkingsHigherLowerElements(strip)
    checkWorkingsOfSurroundingMarkedElements(strip)
    checkWorkingsOfSurroundingElementsLength(strip)
    checkWorkingsOfSurroundingMarkedElementsLength(strip)
    checkWorkingsOfSurroundingElements(strip)
    checkWorkingsOfRemainingSpace(strip)
    checkWorkingsCheckLengthsOfPossibleElements(strip)


    #printStrip(strip.RC, strip.ID)


def checkWorkingsCheckLengthsOfPossibleElements(strip):
    # if unit has been marked, but element not identified, check lengths of possible elements.
    # calculate maximum length.
    # then check for adjacent marked units and compare against maximum length.

    counter = 0

    for i in range(len(strip.outputArray)):
        if not np.isnan(strip.outputArray[i]) and len(strip.workingsArray[i]) > 1:

            maximumLength = 0

            #print("found some: ", strip.RC, strip.ID, i, maximumLength)

            for j in range(len(strip.workingsArray[i])):
                element = strip.workingsArray[i][j]

                #print(j, element, strip.elements[element].maximumLength)

                if strip.elements[element].maximumLength > maximumLength:
                    maximumLength = strip.elements[element].maximumLength

            #print("found some: ", strip.RC, strip.ID, i, maximumLength)

            # this needs to be finished to check adjacent units. simplyfying for maximumLength of 1 for now

            if maximumLength == 1 and strip.outputArray[i] == 1:
                if i != 0: mark(strip, i-1, 0)
                if i < len(strip.outputArray): mark(strip, i+1, 0)





def checkWorkingsOfRemainingSpace(strip):
    # check workings for given element. check they are continuous. compare length to minimumlength. mark middle cross over bits

    for element in strip.elements:
        if strip.elements[element].complete == 0:
            totalCounter = 0

            for i in range(len(strip.workingsArray)):
                if strip.elements[element].ID in strip.workingsArray[i]: totalCounter += 1

            continuousCounter = 0

            for i in range(len(strip.workingsArray)):
                if strip.elements[element].ID in strip.workingsArray[i]: continuousCounter += 1
                if strip.elements[element].ID not in strip.workingsArray[i] and continuousCounter > 0:
                    break

            if totalCounter == continuousCounter:
                buffer = totalCounter - strip.elements[element].minimumLength

                for i in range(len(strip.workingsArray)):
                    if strip.elements[element].ID in strip.workingsArray[i]:
                        for j in range(totalCounter - buffer - buffer):
                            strip.workingsArray[i+buffer] = [strip.elements[element].ID]
                        break


def checkWorkingsOfSurroundingElements(strip):
    # if unit has element identified, look forward/backward - workings can only contain elements that are +/- 1 element

    for i in range(len(strip.workingsArray)):
        if len(strip.workingsArray[i]) == 1: # therefore element has been identified and marked
            element = strip.workingsArray[i][0]

            if i != 0: # check unit before
                for j in range(len(strip.workingsArray[i-1])-1, -1, -1):
                    if strip.workingsArray[i-1][j] < (element - 1):
                        del strip.workingsArray[i-1][j]

            if i != strip.length - 1: # check unit after
                for j in range(len(strip.workingsArray[i+1]) - 1, -1, -1):
                        if strip.workingsArray[i+1][j] > (element + 1):
                            del strip.workingsArray[i+1][j]




def checkWorkingsOfSurroundingMarkedElementsLength(strip):
    # if unit has element identified, look backward/forward for constraints (e.g. not in workingsArray) and then mark units accordingly

    for i in range(len(strip.workingsArray)):
        if len(strip.workingsArray[i]) == 1: # therefore element has been identified and marked
            element = strip.workingsArray[i][0]
            elementType = strip.elements[element].type
            elementMinimumLength = strip.elements[element].minimumLength

            # look backwards
            backwardsConstraint = 0
            for j in range(i - 1, -1, -1):
                if element in strip.workingsArray[j]:
                    backwardsConstraint += 1
                else:
                    break

            # amount forward must be minimumLength - 1 - backwardsConstraint
            amountForward = elementMinimumLength - 1 - backwardsConstraint

            for j in range(amountForward+1):
                strip.workingsArray[i+j] = [element]

            # look forwards
            forwardsConstraint = 0
            for j in range(i+1, strip.length, +1):
                if element in strip.workingsArray[j]:
                    forwardsConstraint += 1
                else:
                    break

            # amount backward must be minimumLength - 1 - forwardsConstraint
            amountBackward = elementMinimumLength - 1 - forwardsConstraint

            for j in range(amountBackward, -1, -1):
                strip.workingsArray[i - j] = [element]
                




def checkWorkingsOfSurroundingElementsLength(strip):
    # if unit is marked, check following units, if marked, calculate length, and compare to workingsArray

    for i in range(len(strip.workingsArray)):
        if strip.outputArray[i] == 1:  # therefore unit has been marked
            length = 1
            for j in range(i+1, len(strip.outputArray)):
                if strip.outputArray[j] == 1:
                    length += 1
                else:
                    break

            for j in range(len(strip.workingsArray[i])-1, -1 , -1):
                element = strip.workingsArray[i][j]
                elementMaximumLength = strip.elements[element].maximumLength

                if length > elementMaximumLength:
                    del strip.workingsArray[i][j]






def checkWorkingsOfSurroundingMarkedElements(strip):
    # if unit has element identified, check surrounding units, if marked they must be part of same element

    for i in range(len(strip.workingsArray)):
        if len(strip.workingsArray[i]) == 1: # therefore element has been identified and marked
            element = strip.workingsArray[i][0]
            elementType = strip.elements[element].type

            #print(elementType)

            if i != 0: # check unit before
                if strip.outputArray[i-1] == elementType:
                    strip.workingsArray[i-1] = [element]

            if i != strip.length - 1: # check unit after
                if strip.outputArray[i+1] == elementType:
                    strip.workingsArray[i+1] = [element]








def checkWorkingsElementsPositions(strip):
    # if unit has element identified, take max length and look forward/backward to ensure element isn't in workingsArray

    for i in range(len(strip.workingsArray)):
        if len(strip.workingsArray[i]) == 1: # therefore element has been identified
            element = strip.workingsArray[i][0]
            maximumLength = strip.elements[element].maximumLength

            for j in range(len(strip.workingsArray)):
                distanceFromi = abs(j-i)
                if distanceFromi >= maximumLength: # workings must be removed
                    for k in range(len(strip.workingsArray[j]) -1 , -1, -1):
                        if strip.workingsArray[j][k] == element: del strip.workingsArray[j][k]


def checkWorkingsHigherLowerElements(strip):
    # check that previous units don't have workings that are higher than the higher in this unit
    # equally, check that later units don't have workings that are lower than the lowest in this unit

    for i in range(len(strip.workingsArray)):
        minElement = min(strip.workingsArray[i])
        maxElement = max(strip.workingsArray[i])

        for j in range(0, i):
            #maxWorkingsElement = max(strip.workingsArray[j])

            #print("len", len(strip.workingsArray[j]))

            for k in range(len(strip.workingsArray[j])-1, -1, -1):

                #print("k", k)

                #print(strip.workingsArray[j][k], maxElement)

                if strip.workingsArray[j][k] > maxElement:
                    #print("workingsElement > maxElement", strip.ID, strip.RC, i, strip.workingsArray[j], strip.workingsArray[j][k], maxElement)
                    del strip.workingsArray[j][k]
                    #print("maxWorkingsElement > maxElement", strip.ID, strip.RC, i, strip.workingsArray[j], "-", maxElement)


        for j in range(i, strip.length):
            #minWorkingsElement = min(strip.workingsArray[j])

            # print("len", len(strip.workingsArray[j]))

            for k in range(len(strip.workingsArray[j]) - 1, -1, -1):

                # print("k", k)

                # print(strip.workingsArray[j][k], maxElement)

                if strip.workingsArray[j][k] < minElement:
                    # print("workingsElement < minElement", strip.ID, strip.RC, i, strip.workingsArray[j], strip.workingsArray[j][k], minElement)
                    del strip.workingsArray[j][k]
                    # print("minWorkingsElement < minElement", strip.ID, strip.RC, i, strip.workingsArray[j], "-", minElement)


def checkWorkingsElementsCount(strip):
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

    #printStrip('R', 14)

    if tableComplete == 1:
        return ["tableComplete", output()]
    else:
        return ["tableNotComplete", output()]

