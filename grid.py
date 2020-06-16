#https://stackoverflow.com/questions/30023763/how-to-make-an-interactive-2d-grid-in-a-window-in-python
import tkinter as tk
import numpy as np

class Cell:
    COLORS = {
            0: 'white',    # untried
            1: 'black',    # obstacle
            2: 'green',    # start
            3: 'red',      # finish
            4: 'blue',     # open
            5: 'gray',     # closed
            6: 'orange',   # path
         }

    def __init__(self, master, x, y, size, value):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.fill = Cell.COLORS[0]
        self.value = value

    def setValue(self, value):
        self.value = value

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None:

            self.fill = Cell.COLORS[self.value]
                
            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=self.fill, outline='black')

class CellGrid(tk.Canvas):
    def __init__(self, master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        tk.Canvas.__init__(self, master, width=cellSize*columnNumber, height=cellSize*rowNumber, *args, **kwargs)

        self.rowNumber = rowNumber
        self.columnNumber = columnNumber
        self.cellSize = cellSize

        # instantiate empty grid
        self.emptyGrid()

        self.current_value = 0
        self.coord_map = np.zeros((rowNumber, columnNumber))

        #memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)
        #bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

        self.draw()

    def setCurrentValue(self, value):
        self.current_value = value

    def getMap(self):
        return self.coord_map

    def draw(self):
        for row in self._grid:
            for cell in row:
                cell.draw()

    def emptyGrid(self):
        self._grid = []
        for row in range(self.rowNumber):
            line = []
            for column in range(self.columnNumber):
                line.append(Cell(self, column, row, self.cellSize, 0))

            self._grid.append(line)

        self.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column
    
    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self._grid[row][column]
        cell.setValue(self.current_value)
        cell.draw()
        #add the cell to the list of cell switched during the click
        self.switched.append(cell)
        self.coord_map[row, column] = self.current_value

    def handleMouseMotion(self, event):
        row, column = self._eventCoords(event)
        cell = self._grid[row][column]

        if cell not in self.switched:
            cell.setValue(self.current_value)
            cell.draw()
            self.switched.append(cell)
            self.coord_map[row, column] = self.current_value

class InteractiveGrid:

    def __init__(self, parent, rowNumber, columnNumber, cellSize, *args, **kwargs):
        self.parent = parent
        parent.title("Interactive Path Finding")

        self.cellgrid = CellGrid(self.parent, rowNumber, columnNumber, cellSize)
        # Buttons
        self.obstacles_button = tk.Button(self.parent, text='Obstacles', command=self.obstaclesCallBack)
        self.points_button = tk.Button(self.parent, text='Points', command=self.pointsCallBack)
        self.clear_button = tk.Button(self.parent, text='Clear' ,command=self.clearCallBack)
        self.map_button = tk.Button(self.parent, text='Print Map', command=self.mapCallBack)

        # Layout
        self.cellgrid.grid(row=0, columnspan=4)
        self.map_button.grid(row=1, column=0, sticky='W')
        self.obstacles_button.grid(row=1, column=1, sticky='E')
        self.points_button.grid(row=1, column=2, sticky='W')
        self.clear_button.grid(row=1, column=3, sticky='E')

    def obstaclesCallBack(self):
        self.cellgrid.setCurrentValue(1)

    def pointsCallBack(self):
        self.cellgrid.setCurrentValue(2)

    def mapCallBack(self):
        print(self.cellgrid.getMap())

    def clearCallBack(self):
        self.cellgrid.emptyGrid()


if __name__ == "__main__":
    app = tk.Tk()

    grid = InteractiveGrid(app, 20, 20, 30)
    # grid.pack()

    app.mainloop()
