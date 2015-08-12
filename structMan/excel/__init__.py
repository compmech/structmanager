"""
Excel (:mod:`structMan.excel`)
==============================

.. currentmodule:: structMan.excel

Derived from "Python Programming on Win32" by Mark Hammond and Andy Robinson.

"""
class Excel(object):
    """Wrapper class to deal with Excel files

    Parameters
    ----------
    filename : str
        The name to the Excel file.

    """
    def __init__(self, filename=None):
        import win32com.client
        import win32com.client.dynamic

        self.xlApp = win32com.client.dynamic.Dispatch('Excel.Application')
        if filename:
            self.filename = filename
            self.xlBook = self.xlApp.Workbooks.Open(filename)
        else:
            self.xlBook = self.xlApp.Workbooks.Add()
            self.filename = ''


    def save(self, newfilename=None):
        """Saves the Excel file

        It will save in the current location if ``newfilename`` is not passed.

        Parameters
        ----------
        newfilename : str, optional
            The Excel file name. It is optional if the file already exists.

        """
        if newfilename is not None:
            try:
                self.filename = newfilename
                self.xlBook.SaveAs(newfilename)
            except:
                raise RuntimeError(
                'Excel file cannot be saved! Please, check if it is opened.')
        else:
            try:
                self.xlBook.Save()
            except:
                raise RuntimeError(
                    'For a new Excel file the "newfilename" must be given!')


    def close(self):
        """Closes the current Excel file"""
        self.xlBook.Close(SaveChanges=0)
        del self.xlApp


    def show(self):
        """Shows the current Excel file"""
        self.xlApp.Visible = 1


    def hide(self):
        """Hides the current Excel file"""
        self.xlApp.Visible = 0


    def get_cell(self, sheet, row, col):
        """Get value of one cell

        Parameters
        ----------
        sheet : str
            The Excel sheet name.
        row : int
            The row index starting at ``1``.
        col : int
            The column index starting at ``1``.

        Returns
        -------
        value : str or float or int
            The value of the corresponding cell.

        """
        sht = self.xlBook.Worksheets(sheet)
        return sht.Cells(row, col).Value


    def set_cell(self, sheet, row, col, value):
        """Set value of one cell

        Parameters
        ----------
        sheet : str
            The Excel sheet name.
        row : int
            The row index starting at ``1``.
        col : int
            The column index starting at ``1``.
        value : str or float or int
            The new value for the cell.

        """
        sht = self.xlBook.Worksheets(sheet)
        sht.Cells(row, col).Value = value


    def get_range(self, sheet, row1, col1, row2, col2):
        """Get a range from Excel as a 2d array (tuple of tuples)

        Parameters
        ----------
        sheet : str
            The Excel sheet name.
        row1 : int
            The first row of the range box.
        col1 : int
            The first column of the range box.
        row2 : int
            The last row of the range box.
        col2 : int
            The last column of the range box.

        """
        sht = self.xlBook.worksheets(sheet)
        return sht.Range(sht.Cells(row1, col1), sht.Cells(row2,
        col2)).Value


    def set_range(self, sheet, leftCol, topRow, data):
        """Set a range in Excel from a 2d array (tuple of tuples)

        Only the left-upper corner of the range box must be supplied, such that
        the right-lower corner is determined based on ``data``.

        Parameters
        ----------
        sheet : str
            The Excel sheet name.
        leftCol : int
            The left column of the range box.
        topRow : int
            The upper row of the range box.
        data : tuple of tuples
            A tuple of tuples representing the 2d array of values.

        """
        bottomRow = topRow + len(data) - 1
        rightCol = leftCol + len(data[0]) - 1
        sht = self.xlBook.Worksheets(sheet)
        sht.Range(sht.Cells(topRow, leftCol), sht.Cells(bottomRow,
        rightCol)).Value = data

#    def runMacro(self, name):
#        self.xlBook.Run(name)
#        self.xlBook.DisplayAlerts = 0

