import pandas as pd
from plotly.offline import plot


def setupPlotFigure(rows, columns, strips, showWorkings):  # setup plotly figures

    figure = {
        'data': [],
        'layout': {},
        'frames': []
    }

    data = createPlotFigureData(rows, columns, strips, showWorkings)
    header = data[0]
    cells = data[1]

    figure['data'] = [{'type': 'table', 'header': header, 'cells': cells, 'columnwidth': [100, 25]}]
    figure['frames'].append({'name': 0, 'data': [{'type': 'table', 'header': header, 'cells': cells}]})

    figure['layout']['updatemenus'] = [
        {
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top',
            'buttons': [
                {
                    'label': 'Play',
                    'method': 'animate',
                    'args': [None,
                             {
                                 'frame': {
                                     'duration': 20,
                                     'redraw': False
                                 },
                                 'fromcurrent': True,
                                 'transition': {
                                     'duration': 20,
                                     'easing': 'quadratic-in-out'
                                 }
                             }]
                },
                {
                    'label': 'Pause',
                    'method': 'animate',
                    'args': [[None],
                             {
                                 'frame': {
                                     'duration': 0,
                                     'redraw': False
                                 },
                                 'mode': 'immediate',
                                 'transition': {'duration': 0}
                             }
                             ]
                }
            ]
        }
    ]

    return figure


def createPlotFigureData(rows, columns, strips, showWorkings):  # creates plot figure data for plotly figure

    # set up columns

    columnLabels = []  # new column to work in df

    for i in range(len(columns)):

        text = "(" + str(i) + ") <br> - "
        for j in range(len(columns[i])):
            text += "<br> " + str(columns[i][j])

        columnLabels.append(text)

    # set up rows

    rowLabels = []
    rowsColor = []

    for i in range(len(rows)):
        text = "(" + str(i) + ") - "

        for j in range(len(rows[i])):
            text += str(rows[i][j])

            if j != (len(rows[i]) - 1):
                text += ", "

        rowLabels.append(text)
        rowsColor.append('darkgrey')

    if showWorkings:

        rowLabels.append("")
        rowsColor.append('white')
        rowLabels.append("cols workings")
        rowsColor.append('white')

        for i in range(len(rows)):
            text = "(" + str(i) + ") - "

            for j in range(len(rows[i])):
                text += str(rows[i][j])

                if j != (len(rows[i]) - 1):
                    text += ", "

            rowLabels.append(text)
            rowsColor.append('darkgrey')

        rowLabels.append("rows workings")
        rowsColor.append('white')

        for i in range(len(rows)):
            text = "(" + str(i) + ") - "

            for j in range(len(rows[i])):
                text += str(rows[i][j])

                if j != (len(rows[i]) - 1):
                    text += ", "

            text += " - Elements: "

            first = True

            stripID = "R" + str(i)

            for j in strips[stripID].elements:
                if first:
                    first = False
                else:
                    text += ", "
                text += str(strips[stripID].elements[j].ID)

            rowLabels.append(text)
            rowsColor.append('darkgrey')

    # set up grid

    grid = []
    colorsGrid = []

    for i in sorted(strips):  # sort strips to display in right order
        if strips[i].RC == 'R':  # only need to show rows (as columns will match)

            grid.append(strips[i].outputArray)

            rowColors = []

            for j in strips[i].outputArray:

                if j == 1:
                    rowColors.append('green')
                elif j == 0:
                    rowColors.append('lightgrey')
                else:
                    rowColors.append('white')

            colorsGrid.append(rowColors)

    if showWorkings:

        newBlankRow = []
        newWhiteRow = []
        for i in range(len(columns)):
            newBlankRow.append('')
            newWhiteRow.append('white')

        grid.append(newBlankRow)
        colorsGrid.append(newWhiteRow)
        newColumnLabels = []

        for i in range(len(columnLabels)):
            text = columnLabels[i]
            text += "<br>-<br>Elements:"

            stripID = "C" + str(i)

            for j in strips[stripID].elements:
                text += "<br>" + str(strips[stripID].elements[j].ID)

            newColumnLabels.append(text)

        grid.append(newColumnLabels)
        colorsGrid.append(newWhiteRow)

        for i in sorted(strips):  # sort strips to display in right order
            if strips[i].RC == 'R':  # only need to show rows (as columns will match)
                newRow = []
                for j in range(len(columnLabels)):
                    stripID = "C" + str(j)
                    newRow.append(strips[stripID].workingsArray[strips[i].RCNum])

                newerRow = []
                for k in range(len(newRow)):
                    text = ""
                    first = 1
                    for l in range(len(newRow[k])):
                        if first == 0: text += ", "
                        text += str(newRow[k][l])
                        first = 0
                    newerRow.append(text)

                grid.append(newerRow)

                rowColors = []

                for j in strips[i].outputArray:

                    if j == 1:
                        rowColors.append('green')
                    elif j == 0:
                        rowColors.append('lightgrey')
                    else:
                        rowColors.append('white')

                colorsGrid.append(rowColors)

        grid.append(newBlankRow)
        colorsGrid.append(newWhiteRow)

        for i in sorted(strips):  # sort strips to display in right order
            if strips[i].RC == 'R':  # only need to show rows (as columns will match)
                newRow = []
                for k in range(len(strips[i].workingsArray)):
                    text = ""
                    first = 1
                    for l in range(len(strips[i].workingsArray[k])):
                        if first == 0: text += ", "
                        text += str(strips[i].workingsArray[k][l])
                        first = 0
                    newRow.append(text)

                grid.append(newRow)

                rowColors = []

                for j in strips[i].outputArray:

                    if j == 1:
                        rowColors.append('green')
                    elif j == 0:
                        rowColors.append('lightgrey')
                    else:
                        rowColors.append('white')

                colorsGrid.append(rowColors)


    df = pd.DataFrame(data=grid, index=rowLabels, columns=columnLabels)
    dfColors = pd.DataFrame(data=colorsGrid, index=rowsColor, columns=columnLabels)

    data = [dict(values=['-'] + list(df.columns), fill=dict(color='darkgrey'), align='left'),
            dict(values=[v for v in df.reset_index().values.T],
                 fill=dict(color=[v for v in dfColors.reset_index().values.T]), align='left', height=25,
                 line=dict(width=1))]

    return data


def addFrameToPlotFigure(rows, columns, strips, figure, showWorkings):  # adds frames to plotly figure

    i = len(figure['frames'])

    data = createPlotFigureData(rows, columns, strips, showWorkings)
    header = data[0]
    cells = data[1]

    figure['frames'].append({'name': i, 'data': [{'type': 'table', 'header': header, 'cells': cells}]})

    return figure


def showPlotFigure(figure):  # finalise (e.g. create sliders for animation) and show plotly figure

    sliders_dict = {
        'visible': True,
        'yanchor': 'top',
        'xanchor': 'left',
        'currentvalue': {
            'font': {'size': 20},
            'prefix': 'Step:',
            'visible': True,
            'xanchor': 'right'
        },
        'transition': {'duration': 20, 'easing': 'cubic-in-out'},
        'pad': {'b': 10, 't': 50},
        'len': 0.9,
        'x': 0.1,
        'y': 0,
        'steps': []
    }


    for i in range(len(figure['frames'])):
        slider_step = {'args': [
            [i],
            {'frame': {'duration': 20, 'redraw': False},
             'mode': 'immediate',
             'transition': {'duration': 20}}
        ],
            'label': i,
            'method': 'animate'}
        sliders_dict['steps'].append(slider_step)



    figure['layout']['sliders'] = [sliders_dict]

    #print(figure)

    plot(figure)


