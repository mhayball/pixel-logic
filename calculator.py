import numpy as np


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

        for i in range(len(self.workingsArray)):
            self.workingsArray[i] = []

    class Element:
        def __init__(self, ID, minimumLength, type):
            self.ID = ID
            self.minimumLength = minimumLength
            self.type = type
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


def firstPass(strips):  # first check of strips following setup
    for i in strips:

        checkStrip(strips[i])

        if strips[i].complete == 0:

            # print "i", i
            # pprint(vars(strips[i]))

            for j in range(strips[i].elements[0].minimumLength - 1, strips[i].elements[0].maximumLength):

                # print "min, max, j", strips[i].elements[0].minimumLength, strips[i].elements[0].maximumLength, j
                # print len(strips[i].elements)

                forwardArray = [np.nan] * strips[i].length

                x = j + 1

                for k in range(0, len(strips[i].elements)):

                    # print "k", k

                    # forwardArray[j+k] = strips[i].elements[k].ID

                    # print strips[i].elements[k].minimumLength

                    for l in range(0, strips[i].elements[k].minimumLength):
                        forwardArray[x] = strips[i].elements[k].ID
                        x = x + 1
                        # print "k+l+j", k+l+j, k, l, j

                # print("forwardArray", forwardArray)

                x = 0
                while np.isnan(forwardArray[x]):
                    forwardArray[x] = 0
                    # print x
                    x = x + 1

                # print("forwardArray", forwardArray)

                x = strips[i].length - 1
                while np.isnan(forwardArray[x]):
                    forwardArray[x] = len(strips[i].elements) - 1
                    x = x - 1

                # print("forwardArray", forwardArray)

                for k in range(0, len(forwardArray)):

                    # print "forwardArray[l] strips[i].workingsArray[l] -", forwardArray[l], strips[i].workingsArray[l]

                    if forwardArray[k] not in strips[i].workingsArray[k]:

                        # print strips[i].outputArray[k]

                        if np.isnan(strips[i].outputArray[k]):

                            strips[i].workingsArray[k].append(forwardArray[k])

                        elif strips[i].outputArray[k] == strips[i].elements[forwardArray[k]].type:
                            # print "already found, 0"
                            # print k
                            # print forwardArray[k]
                            # print strips[i].elements[forwardArray[k]].type

                            strips[i].workingsArray[k].append(forwardArray[k])

    for i in strips:

        if strips[i].complete == 0:

            for k in range(0, len(strips[i].workingsArray)):

                # print "len workingArray - ", len(strips[i].workingsArray[k])

                if len(strips[i].workingsArray[k]) == 1:
                    key = strips[i].workingsArray[k][0]

                    if not np.isnan(key):
                        mark(strips[i], k, strips[i].elements[key].type)

        # print stuff
        """
        print("--- Strip ---")
        print "i", i
        pprint(vars(strips[i]))
        print("--- WorkingsArray ---")
        for j in range(len(strips[i].workingsArray)):
            print strips[i].workingsArray[j]
        print("--- Elements ---")
        for j in strips[i].elements:
            pprint(vars(strips[i].elements[j]))
        print("----------------")
        """


def printStrip(RC, number):  # print strips - handy debug function
    i = (RC, number)
    pprint(vars(strips[i]))
    for j in strips[i].elements:
        pprint(vars(strips[i].elements[j]))


def mark(strip, location, type):  # marks a unit in a strip at location, with type

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

        if strip.RC == 'R':
            addFrameToPlotFigure(rows, columns, strips, figure)

        removeWorkings(strip, location, type)
        checkWorkings(strip)
        markCorrespondingStrip(strip, location, type)
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


def removeWorkings(strip, location, type):  # after a cell has been marked, update and removes workings from said cell

    # print "checkWorkings -", strip.ID, location, strip.workingsArray, strip.workingsArray[location], type

    delWorkingsArrayLocations = []  # empty array for identifying which elements are removed from the workings

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

    for i in range(len(strip.workingsArray)):

        minElement = min(strip.workingsArray[i])
        maxElement = max(strip.workingsArray[i])

        for j in range(0, i):  # if there are any workings elements greater than the maxElement, prior to j, remove them
            print("test")

        for j in range(i, len(strip.workingsArray)):  # if there are any workings elements less than the minElement, after j, remove them
            print("test")



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


def checkTable(strips):  # check the strips, attempt to solve table
    for i in strips:

        checkUnitsIdentifiedInElements(strips[i])

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


def solver(rows, columns, plot):

    print(rows)
    print(columns)

    strips = setup(rows, columns)

    firstPass(strips)

    i = 1
    longstop = 10
    tableComplete = 0

    while i < longstop:

        if tableComplete == 1: i = longstop  # use this to do one final check!

        checkTable(strips)

        # have all strips been completed?
        tableComplete = 1
        for j in strips:
            if strips[j].complete == 0: tableComplete = 0

        i += 1

    return 1





def calculator(input):
    return input+2