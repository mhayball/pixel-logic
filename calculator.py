import numpy as np
import plot
import itertools
from pprint import pprint

class Strip:
    def __init__(self, ID, RC, RCNum, inputArray, length):
        self.ID = ID
        self.RC = RC
        self.RCNum = RCNum
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
            self.active = 1
            self.identified = 0
            self.workingsArray = workingsArray


def setup(rows, columns):

    # first test to see if solvable, e.g. sum of rows = sum of cols
    sumCheck(rows, columns)

    # setup initial strips
    strips = dict()

    # rows
    for i in range(len(rows)):
        dictID = "R" + str(i)
        strips[dictID] = Strip(dictID, "R", i, rows[i], len(columns))

    # cols
    for i in range(len(columns)):
        dictID = "C" + str(i)
        strips[dictID] = Strip(dictID, "C", i, columns[i], len(rows))

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


def sumCheck(rows, columns):
    rowsSum = np.nansum(np.nansum(rows))
    columnsSum = np.nansum(np.nansum(columns))

    if rowsSum != columnsSum:
        raise Exception("error - rowsSum != columnsSum", rowsSum, columnsSum)

    return


def firstPass():
    # first check of strips following setup
    # all permutations of elements calculated (elementPermutations) and added to elementList
    # stripPermutations then calculated based on product of elementList
    # possibleArray is a temporary list that shows possible positions of elements based on minimum length
    # all permutations of possibleArray are considered and then recorded

    for i in strips:

        #printStrip(strips[i].RC, strips[i].ID)

        if strips[i].inputArray[0] == 0:  # special case if strip is 0 e.g. blank

            strips[i].workingsPermutations[0] = strips[i].WorkingsPermutations(0, [0 for i in range(strips[i].length)])

        else: # calculate permutations

            elementList = []

            for j in strips[i].elements:

                # create element permutations
                elementPermutations = []

                for k in range(strips[i].elements[j].minimumLength, (strips[i].elements[j].maximumLength + 1)):
                    elementSubPermutations = []
                    for l in range(k):
                        elementSubPermutations.append(strips[i].elements[j].ID)
                    elementPermutations.append(elementSubPermutations)

                strips[i].elements[j].premutations = elementPermutations

                # append elementPermutations into elementList for strip
                elementList.append(elementPermutations)

            strips[i].elementList = elementList

            # stripPermutations then calculated as produce of elementList
            stripPermutations = itertools.product(*elementList)
            strips[i].stripPermutations = stripPermutations


            # only permutations with exact length of strip are possible
            # flatten lists first, then check lengths
            counter = 0
            for j in list(stripPermutations):
                flattened = list(itertools.chain(*j))
                #print(j, len(j), flattened, len(flattened))

                if len(flattened) == strips[i].length:
                    # only permutations of same length can be possible and added as possible workingsArray
                    strips[i].workingsPermutations[counter] = strips[i].WorkingsPermutations(counter, flattened)
                    counter += 1

        buildWorkingsArray(strips[i])


def buildWorkingsArray(strip):
    # takes current WorkingsPermutations of a strip and returns the WorkingsArray

    #printStrip(strip.ID)

    masterWorkingsArray = [[] for i in range(strip.length)]

    for i in strip.workingsPermutations:

        #print(masterWorkingsArray)
        #print(strip.workingsPermutations[i].workingsArray)

        if strip.workingsPermutations[i].active == 1: # only consider permutations that are active

            for j in range(len(strip.workingsPermutations[i].workingsArray)):

                possibleElement = strip.workingsPermutations[i].workingsArray[j]

                #print(j, strip.workingsPermutations[i].workingsArray[j], "possibleElement - ", possibleElement)

                # j = location in workingsArray
                # if not in workingsArray, and doesn't = NaN, then add to workingsArray

                if possibleElement not in masterWorkingsArray[j] and not np.isnan(possibleElement):
                    #print("add to masterWorkingsArray", j, possibleElement, masterWorkingsArray)
                    #print("masterWorkingsArray[j]", masterWorkingsArray[j])
                    masterWorkingsArray[j].append(possibleElement)
                    #print("masterWorkingsArray - ", masterWorkingsArray)

    #print("masterWorkingsArray - ", masterWorkingsArray)

    strip.workingsArray = masterWorkingsArray

    return


def checkTable():
    # check the strips, attempt to solve table

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
                        mark(strips[i], j, 1) # mark, but we don't know which element yet
                    if even:
                        mark(strips[i], j, 0) # mark, but we don't know which element yet


def printStrip(ID):
    # print a strip - handy debug function

    print("---", ID, "---")

    """
    print("ID:", strips[ID].ID, "RC:", strips[ID].RC, "RCNum:", strips[ID].RCNum)
    print("inputArray:", strips[ID].inputArray)
    print("length:", strips[ID].length)
    print("workingsArray:", strips[ID].workingsArray)
    print("outputArray:", strips[ID].outputArray)
    print("complete:", strips[ID].complete)
    """

    pprint(vars(strips[ID]))

    print("---", ID, "- WorkingsPermutations ---")
    for j in strips[ID].workingsPermutations:
        pprint(vars(strips[ID].workingsPermutations[j]))

    print("---", ID, "- Elements ---")
    for j in strips[ID].elements:
        pprint(vars(strips[ID].elements[j]))

    print("------")


def mark(strip, location, type, element = np.nan):
    # marks a unit in a strip at location, with type, and element if known

    if strip.outputArray[location] == 0 and type == 1:
        print("Error")
        printStrip(strip.ID)
        raise Exception("Mark error - trying to mark a unit with type 1 that is already marked as type 0")

    elif strip.outputArray[location] == 1 and type == 0:
        print("Error")
        printStrip(strip.ID)
        raise Exception("Mark error - trying to mark a unit with type 0 that is already marked as type 1")

    elif strip.outputArray[location] == type:  # already marked, so do nothing
        # print("already marked")
        pass
    else:  # mark the unit
        # print "marked - location:", location, "type:", type

        strip.outputArray[location] = type  # mark the unit

        removeWorkings(strip, location, type, element)

        checkPermutations(strip)

        if strip.RC == 'R' and showPlot == 1:
            plot.addFrameToPlotFigure(rows, columns, strips, figure, showWorkings)

        markCorrespondingStrip(strip, location, type)
        checkStripComplete(strip)


def markCorrespondingStrip(strip, location, type):  # find corresponding unit in row/column strip
    # e.g. if RC = C, strip.id = 8 and location = 9, then look for RC = R, ID = location, location = ID

    # print("correspondingStrip -"), strip.ID, location, strip.RC
    # print strips

    if strip.RC == 'R':
        correspondingDictID = "C" + str(location)
    elif strip.RC == 'C':
        correspondingDictID = "R" + str(location)

    if correspondingDictID in strips:
        # print "found correspondingDictID", correspondingDictID
        mark(strips[correspondingDictID], strip.RCNum, type)


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


def removeWorkings(strip, location, type, element):
    # after a cell has been marked, update and removes workings from said cell

    if not np.isnan(element): # if element is known, then simply replace workingsArray with the given element

        strip.workingsArray[location] = [element]

    else: # if element isn't known, then remove possible elements that don't have the same type

        for i in range(len(strip.workingsArray[location]) -1, -1, -1): # if type = 0, then only elements with an even number can be correct
            if isItOdd(strip.workingsArray[location][i]) and type == 0:
                del strip.workingsArray[location][i]
            elif not isItOdd(strip.workingsArray[location][i]) and type == 1:
                del strip.workingsArray[location][i]



def checkPermutations(strip):
    # workingsArray has potentially been modified following a unit being marked
    # as such cycle through permutations to see which no longer fit

    for i in range(len(strip.outputArray)):

        if not np.isnan(strip.outputArray[i]): # e.g. it has been marked/identified

            possibleElements = strip.workingsArray[i]
            #print("### possibleElements", possibleElements, i)
            #printStrip(strip.ID)

            for j in strip.workingsPermutations:
                if strip.workingsPermutations[j].workingsArray[i] not in possibleElements:
                    if strip.workingsPermutations[j].identified == 1:
                        print("Error")
                        print(strip.workingsPermutations[j])
                        printStrip(strip.ID)
                        raise Exception("Error - identified permutation trying to be set inactive")
                    strip.workingsPermutations[j].active = 0

    # if only 1 permutation left active, then it must be the identified permutation
    counter = 0
    identifiedPermutation = 0

    for i in strip.workingsPermutations:
        if strip.workingsPermutations[i].active == 1:
            counter += 1
            identifiedPermutation = i

    if counter == 1:

        if strip.workingsPermutations[identifiedPermutation].active == 0:
            print("Error")
            print(identifiedPermutation)
            printStrip(strip.ID)
            raise Exception("Permutation error - trying to set inactive permutation as identified")
        else:
            strip.workingsPermutations[identifiedPermutation].identified = 1

    if counter == 0:
        print("Error")
        printStrip(strip.ID)
        raise Exception("Permutation error - no permutations available")

    buildWorkingsArray(strip) # rebuildWorkingsArray


def output():

    output = []

    for i in strips:
        if strips[i].RC =='R':
            output.append(strips[i].outputArray)

    return output


def checkResults():
    # check that sum of inputArray == sum of outputArray
    # note this does not check that elements have been correctly checked

    for i in strips:
        if np.sum(strips[i].inputArray) == np.sum(strips[i].outputArray):
            #print(strips[i].ID, strips[i].inputArray, np.sum(strips[i].inputArray), strips[i].outputArray, np.sum(strips[i].outputArray))
            pass
        else:
            print("Error")
            printStrip(strips[i].ID)
            raise Exception("CheckResults error - sum of input and output array did not match")


def solver(inputRows, inputColumns, inputShowPlot):

    global showPlot, showWorkings, strips, rows, columns

    rows = np.array(inputRows)
    columns = np.array(inputColumns)
    showPlot = inputShowPlot
    showWorkings = True

    strips = setup(rows, columns)




    """
    for i in strips:

        printStrip(strips[i].ID)


        
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
        printStrip(strips[i].ID)
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

    print("--------start of final results---------")

    """
    for i in strips:
        printStrip(strips[i].ID)
    """

    #for i in strips:
        #print(strips[i].ID, strips[i].complete, strips[i].outputArray)


    if tableComplete == 1:

        checkResults()

        return ["tableComplete", output()]
    else:
        return ["tableNotComplete", output()]

