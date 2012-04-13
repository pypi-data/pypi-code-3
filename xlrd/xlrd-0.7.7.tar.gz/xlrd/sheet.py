# -*- coding: cp1252 -*-

##
# <p> Portions copyright � 2005-2012 Stephen John Machin, Lingfo Pty Ltd</p>
# <p>This module is part of the xlrd package, which is released under a BSD-style licence.</p>
##

# 2010-04-25 SJM fix zoom factors cooking logic
# 2010-04-15 CW  r4253 fix zoom factors cooking logic
# 2010-04-09 CW  r4248 add a flag so xlutils knows whether or not to write a PANE record
# 2010-03-29 SJM Fixed bug in adding new empty rows in put_cell_ragged
# 2010-03-28 SJM Tailored put_cell method for each of ragged_rows=False (fixed speed regression) and =True (faster)
# 2010-03-25 CW  r4236 Slight refactoring to remove method calls
# 2010-03-25 CW  r4235 Collapse expand_cells into put_cell and enhance the raggedness. This should save even more memory!
# 2010-03-25 CW  r4234 remove duplicate chunks for extend_cells; refactor to remove put_number_cell and put_blank_cell which essentially duplicated the code of put_cell
# 2010-03-10 SJM r4222 Added reading of the PANE record.
# 2010-03-10 SJM r4221 Preliminary work on "cooked" mag factors; use at own peril
# 2010-03-01 SJM Reading SCL record
# 2010-03-01 SJM Added ragged_rows functionality
# 2009-08-23 SJM Reduced CPU time taken by parsing MULBLANK records.
# 2009-08-18 SJM Used __slots__ and sharing to reduce memory consumed by Rowinfo instances
# 2009-05-31 SJM Fixed problem with no CODEPAGE record on extremely minimal BIFF2.x 3rd-party file
# 2009-04-27 SJM Integrated on_demand patch by Armando Serrano Lombillo
# 2008-02-09 SJM Excel 2.0: build XFs on the fly from cell attributes
# 2007-12-04 SJM Added support for Excel 2.x (BIFF2) files.
# 2007-10-11 SJM Added missing entry for blank cell type to ctype_text
# 2007-07-11 SJM Allow for BIFF2/3-style FORMAT record in BIFF4/8 file
# 2007-04-22 SJM Remove experimental "trimming" facility.

from biffh import *
from timemachine import *
from struct import unpack, calcsize
from formula import dump_formula, decompile_formula, rangename2d, FMLA_TYPE_CELL, FMLA_TYPE_SHARED
from formatting import nearest_colour_index, Format
import time

DEBUG = 0
OBJ_MSO_DEBUG = 0

_WINDOW2_options = (
    # Attribute names and initial values to use in case
    # a WINDOW2 record is not written.
    ("show_formulas", 0),
    ("show_grid_lines", 1),
    ("show_sheet_headers", 1),
    ("panes_are_frozen", 0),
    ("show_zero_values", 1),
    ("automatic_grid_line_colour", 1),
    ("columns_from_right_to_left", 0),
    ("show_outline_symbols", 1),
    ("remove_splits_if_pane_freeze_is_removed", 0),
    # Multiple sheets can be selected, but only one can be active
    # (hold down Ctrl and click multiple tabs in the file in OOo)
    ("sheet_selected", 0),
    # "sheet_visible" should really be called "sheet_active"
    # and is 1 when this sheet is the sheet displayed when the file
    # is open. More than likely only one sheet should ever be set as
    # visible.
    # This would correspond to the Book's sheet_active attribute, but
    # that doesn't exist as WINDOW1 records aren't currently processed.
    # The real thing is the visibility attribute from the BOUNDSHEET record.
    ("sheet_visible", 0),
    ("show_in_page_break_preview", 0),
    )

##
# <p>Contains the data for one worksheet.</p>
#
# <p>In the cell access functions, "rowx" is a row index, counting from zero, and "colx" is a
# column index, counting from zero.
# Negative values for row/column indexes and slice positions are supported in the expected fashion.</p>
#
# <p>For information about cell types and cell values, refer to the documentation of the {@link #Cell} class.</p>
#
# <p>WARNING: You don't call this class yourself. You access Sheet objects via the Book object that
# was returned when you called xlrd.open_workbook("myfile.xls").</p>


class Sheet(BaseObject):
    ##
    # Name of sheet.
    name = ''

    ##
    # A reference to the Book object to which this sheet belongs.
    # Example usage: some_sheet.book.datemode
    book = None
    
    ##
    # Number of rows in sheet. A row index is in range(thesheet.nrows).
    nrows = 0

    ##
    # Nominal number of columns in sheet. It is 1 + the maximum column index
    # found, ignoring trailing empty cells. See also open_workbook(ragged_rows=?)
    # and Sheet.{@link #Sheet.row_len}(row_index).
    ncols = 0

    ##
    # The map from a column index to a {@link #Colinfo} object. Often there is an entry
    # in COLINFO records for all column indexes in range(257).
    # Note that xlrd ignores the entry for the non-existent
    # 257th column. On the other hand, there may be no entry for unused columns.
    # <br /> -- New in version 0.6.1. Populated only if open_workbook(formatting_info=True).
    colinfo_map = {}

    ##
    # The map from a row index to a {@link #Rowinfo} object. Note that it is possible
    # to have missing entries -- at least one source of XLS files doesn't
    # bother writing ROW records.
    # <br /> -- New in version 0.6.1. Populated only if open_workbook(formatting_info=True).
    rowinfo_map = {}

    ##
    # List of address ranges of cells containing column labels.
    # These are set up in Excel by Insert > Name > Labels > Columns.
    # <br> -- New in version 0.6.0
    # <br>How to deconstruct the list:
    # <pre>
    # for crange in thesheet.col_label_ranges:
    #     rlo, rhi, clo, chi = crange
    #     for rx in xrange(rlo, rhi):
    #         for cx in xrange(clo, chi):
    #             print "Column label at (rowx=%d, colx=%d) is %r" \
    #                 (rx, cx, thesheet.cell_value(rx, cx))
    # </pre>
    col_label_ranges = []

    ##
    # List of address ranges of cells containing row labels.
    # For more details, see <i>col_label_ranges</i> above.
    # <br> -- New in version 0.6.0
    row_label_ranges = []

    ##
    # List of address ranges of cells which have been merged.
    # These are set up in Excel by Format > Cells > Alignment, then ticking
    # the "Merge cells" box.
    # <br> -- New in version 0.6.1. Extracted only if open_workbook(formatting_info=True).
    # <br>How to deconstruct the list:
    # <pre>
    # for crange in thesheet.merged_cells:
    #     rlo, rhi, clo, chi = crange
    #     for rowx in xrange(rlo, rhi):
    #         for colx in xrange(clo, chi):
    #             # cell (rlo, clo) (the top left one) will carry the data
    #             # and formatting info; the remainder will be recorded as
    #             # blank cells, but a renderer will apply the formatting info
    #             # for the top left cell (e.g. border, pattern) to all cells in
    #             # the range.
    # </pre>
    merged_cells = []
    
    ##
    # Mapping of (rowx, colx) to list of (offset, font_index) tuples. The offset
    # defines where in the string the font begins to be used.
    # Offsets are expected to be in ascending order.
    # If the first offset is not zero, the meaning is that the cell's XF's font should
    # be used from offset 0.
    # <br /> This is a sparse mapping. There is no entry for cells that are not formatted with  
    # rich text.
    # <br>How to use:
    # <pre>
    # runlist = thesheet.rich_text_runlist_map.get((rowx, colx))
    # if runlist:
    #     for offset, font_index in runlist:
    #         # do work here.
    #         pass
    # </pre>
    # Populated only if open_workbook(formatting_info=True).
    # <br /> -- New in version 0.7.2.
    # <br /> &nbsp;
    rich_text_runlist_map = {}    

    ##
    # Default column width from DEFCOLWIDTH record, else None.
    # From the OOo docs:<br />
    # """Column width in characters, using the width of the zero character
    # from default font (first FONT record in the file). Excel adds some
    # extra space to the default width, depending on the default font and
    # default font size. The algorithm how to exactly calculate the resulting
    # column width is not known.<br />
    # Example: The default width of 8 set in this record results in a column
    # width of 8.43 using Arial font with a size of 10 points."""<br />
    # For the default hierarchy, refer to the {@link #Colinfo} class.
    # <br /> -- New in version 0.6.1
    defcolwidth = None

    ##
    # Default column width from STANDARDWIDTH record, else None.
    # From the OOo docs:<br />
    # """Default width of the columns in 1/256 of the width of the zero
    # character, using default font (first FONT record in the file)."""<br />
    # For the default hierarchy, refer to the {@link #Colinfo} class.
    # <br /> -- New in version 0.6.1
    standardwidth = None

    ##
    # Default value to be used for a row if there is
    # no ROW record for that row.
    # From the <i>optional</i> DEFAULTROWHEIGHT record.
    default_row_height = None

    ##
    # Default value to be used for a row if there is
    # no ROW record for that row.
    # From the <i>optional</i> DEFAULTROWHEIGHT record.
    default_row_height_mismatch = None

    ##
    # Default value to be used for a row if there is
    # no ROW record for that row.
    # From the <i>optional</i> DEFAULTROWHEIGHT record.
    default_row_hidden = None

    ##
    # Default value to be used for a row if there is
    # no ROW record for that row.
    # From the <i>optional</i> DEFAULTROWHEIGHT record.
    default_additional_space_above = None

    ##
    # Default value to be used for a row if there is
    # no ROW record for that row.
    # From the <i>optional</i> DEFAULTROWHEIGHT record.
    default_additional_space_below = None

    ##
    # Visibility of the sheet. 0 = visible, 1 = hidden (can be unhidden
    # by user -- Format/Sheet/Unhide), 2 = "very hidden" (can be unhidden
    # only by VBA macro).
    visibility = 0

    ##
    # A 256-element tuple corresponding to the contents of the GCW record for this sheet.
    # If no such record, treat as all bits zero.
    # Applies to BIFF4-7 only. See docs of the {@link #Colinfo} class for discussion.
    gcw = (0, ) * 256

    ##
    # <p>A list of {@link #Hyperlink} objects corresponding to HLINK records found
    # in the worksheet.<br />-- New in version 0.7.2 </p>
    hyperlink_list = []

    ##
    # <p>A sparse mapping from (rowx, colx) to an item in {@link #Sheet.hyperlink_list}.
    # Cells not covered by a hyperlink are not mapped.
    # It is possible using the Excel UI to set up a hyperlink that 
    # covers a larger-than-1x1 rectangle of cells.
    # Hyperlink rectangles may overlap (Excel doesn't check).
    # When a multiply-covered cell is clicked on, the hyperlink that is activated
    # (and the one that is mapped here) is the last in hyperlink_list.
    # <br />-- New in version 0.7.2 </p>
    hyperlink_map = {}

    ##
    # <p>A sparse mapping from (rowx, colx) to a {@link #Note} object.
    # Cells not containing a note ("comment") are not mapped.
    # <br />-- New in version 0.7.2 </p>
    cell_note_map = {}    
    
    ##
    # Number of columns in left pane (frozen panes; for split panes, see comments below in code)
    vert_split_pos = 0

    ##
    # Number of rows in top pane (frozen panes; for split panes, see comments below in code)
    horz_split_pos = 0

    ##
    # Index of first visible row in bottom frozen/split pane
    horz_split_first_visible = 0

    ##
    # Index of first visible column in right frozen/split pane
    vert_split_first_visible = 0

    ##
    # Frozen panes: ignore it. Split panes: explanation and diagrams in OOo docs.
    split_active_pane = 0

    ##
    # Boolean specifying if a PANE record was present, ignore unless you're xlutils.copy
    has_pane_record = 0

    ##
    # A list of the horizontal page breaks in this sheet.
    # Breaks are tuples in the form (index of row after break, start col index, end col index).
    # Populated only if open_workbook(formatting_info=True).
    # <br /> -- New in version 0.7.2
    horizontal_page_breaks = []

    ##
    # A list of the vertical page breaks in this sheet.
    # Breaks are tuples in the form (index of col after break, start row index, end row index).
    # Populated only if open_workbook(formatting_info=True).
    # <br /> -- New in version 0.7.2
    vertical_page_breaks = []


    def __init__(self, book, position, name, number):
        self.book = book
        self.biff_version = book.biff_version
        self._position = position
        self.logfile = book.logfile
        self.pickleable = book.pickleable
        if array_array and (CAN_PICKLE_ARRAY or not book.pickleable):
            # use array
            self.bt = array_array('B', [XL_CELL_EMPTY])
            self.bf = array_array('h', [-1])
        else:
            # don't use array
            self.bt = [XL_CELL_EMPTY]
            self.bf = [-1]
        self.name = name
        self.number = number
        self.verbosity = book.verbosity
        self.formatting_info = book.formatting_info
        self.ragged_rows = book.ragged_rows
        if self.ragged_rows:
            self.put_cell = self.put_cell_ragged
        else:
            self.put_cell = self.put_cell_unragged
        self._xf_index_to_xl_type_map = book._xf_index_to_xl_type_map
        self.nrows = 0 # actual, including possibly empty cells
        self.ncols = 0
        self._maxdatarowx = -1 # highest rowx containing a non-empty cell
        self._maxdatacolx = -1 # highest colx containing a non-empty cell
        self._dimnrows = 0 # as per DIMENSIONS record
        self._dimncols = 0
        self._cell_values = []
        self._cell_types = []
        self._cell_xf_indexes = []
        self.defcolwidth = None
        self.standardwidth = None
        self.default_row_height = None
        self.default_row_height_mismatch = 0
        self.default_row_hidden = 0
        self.default_additional_space_above = 0
        self.default_additional_space_below = 0
        self.colinfo_map = {}
        self.rowinfo_map = {}
        self.col_label_ranges = []
        self.row_label_ranges = []
        self.merged_cells = []
        self.rich_text_runlist_map = {}
        self.horizontal_page_breaks = []
        self.vertical_page_breaks = []
        self._xf_index_stats = [0, 0, 0, 0]
        self.visibility = book._sheet_visibility[number] # from BOUNDSHEET record
        for attr, defval in _WINDOW2_options:
            setattr(self, attr, defval)
        self.first_visible_rowx = 0
        self.first_visible_colx = 0
        self.gridline_colour_index = 0x40
        self.gridline_colour_rgb = None # pre-BIFF8
        self.hyperlink_list = []
        self.hyperlink_map = {}
        self.cell_note_map = {}

        # Values calculated by xlrd to predict the mag factors that
        # will actually be used by Excel to display your worksheet.
        # Pass these values to xlwt when writing XLS files.
        # Warning 1: Behaviour of OOo Calc and Gnumeric has been observed to differ from Excel's.
        # Warning 2: A value of zero means almost exactly what it says. Your sheet will be
        # displayed as a very tiny speck on the screen. xlwt will reject attempts to set
        # a mag_factor that is not (10 <= mag_factor <= 400).
        self.cooked_page_break_preview_mag_factor = 60
        self.cooked_normal_view_mag_factor = 100

        # Values (if any) actually stored on the XLS file
        self.cached_page_break_preview_mag_factor = None # from WINDOW2 record
        self.cached_normal_view_mag_factor = None # from WINDOW2 record
        self.scl_mag_factor = None # from SCL record

        self._ixfe = None # BIFF2 only
        self._cell_attr_to_xfx = {} # BIFF2.0 only

        #### Don't initialise this here, use class attribute initialisation.
        #### self.gcw = (0, ) * 256 ####

        if self.biff_version >= 80:
            self.utter_max_rows = 65536
        else:
            self.utter_max_rows = 16384
        self.utter_max_cols = 256

        self._first_full_rowx = -1

        # self._put_cell_exceptions = 0
        # self._put_cell_row_widenings = 0
        # self._put_cell_rows_appended = 0
        # self._put_cell_cells_appended = 0


    ##
    # {@link #Cell} object in the given row and column.
    def cell(self, rowx, colx):
        if self.formatting_info:
            xfx = self.cell_xf_index(rowx, colx)
        else:
            xfx = None
        return Cell(
            self._cell_types[rowx][colx],
            self._cell_values[rowx][colx],
            xfx,
            )

    ##
    # Value of the cell in the given row and column.
    def cell_value(self, rowx, colx):
        return self._cell_values[rowx][colx]

    ##
    # Type of the cell in the given row and column.
    # Refer to the documentation of the {@link #Cell} class.
    def cell_type(self, rowx, colx):
        return self._cell_types[rowx][colx]

    ##
    # XF index of the cell in the given row and column.
    # This is an index into Book.{@link #Book.xf_list}.
    # <br /> -- New in version 0.6.1
    def cell_xf_index(self, rowx, colx):
        self.req_fmt_info()
        xfx = self._cell_xf_indexes[rowx][colx]
        if xfx > -1:
            self._xf_index_stats[0] += 1
            return xfx
        # Check for a row xf_index
        try:
            xfx = self.rowinfo_map[rowx].xf_index
            if xfx > -1:
                self._xf_index_stats[1] += 1
                return xfx
        except KeyError:
            pass
        # Check for a column xf_index
        try:
            xfx = self.colinfo_map[colx].xf_index
            if xfx == -1: xfx = 15
            self._xf_index_stats[2] += 1
            return xfx
        except KeyError:
            # If all else fails, 15 is used as hardwired global default xf_index.
            self._xf_index_stats[3] += 1
            return 15

    ##
    # Returns the effective number of cells in the given row. For use with
    # open_workbook(ragged_rows=True) which is likely to produce rows
    # with fewer than {@link #Sheet.ncols} cells.
    # <br /> -- New in version 0.7.2
    def row_len(self, rowx):
        return len(self._cell_values[rowx])

    ##
    # Returns a sequence of the {@link #Cell} objects in the given row.
    def row(self, rowx):
        return [
            self.cell(rowx, colx)
            for colx in xrange(len(self._cell_values[rowx]))
            ]

    ##
    # Returns a slice of the types
    # of the cells in the given row.
    def row_types(self, rowx, start_colx=0, end_colx=None):
        if end_colx is None:
            return self._cell_types[rowx][start_colx:]
        return self._cell_types[rowx][start_colx:end_colx]

    ##
    # Returns a slice of the values
    # of the cells in the given row.
    def row_values(self, rowx, start_colx=0, end_colx=None):
        if end_colx is None:
            return self._cell_values[rowx][start_colx:]
        return self._cell_values[rowx][start_colx:end_colx]

    ##
    # Returns a slice of the {@link #Cell} objects in the given row.
    def row_slice(self, rowx, start_colx=0, end_colx=None):
        nc = len(self._cell_values[rowx])
        if start_colx < 0:
            start_colx += nc
            if start_colx < 0:
                start_colx = 0
        if end_colx is None or end_colx > nc:
            end_colx = nc
        elif end_colx < 0:
            end_colx += nc
        return [
            self.cell(rowx, colx)
            for colx in xrange(start_colx, end_colx)
            ]

    ##
    # Returns a slice of the {@link #Cell} objects in the given column.
    def col_slice(self, colx, start_rowx=0, end_rowx=None):
        nr = self.nrows
        if start_rowx < 0:
            start_rowx += nr
            if start_rowx < 0:
                start_rowx = 0
        if end_rowx is None or end_rowx > nr:
            end_rowx = nr
        elif end_rowx < 0:
            end_rowx += nr
        return [
            self.cell(rowx, colx)
            for rowx in xrange(start_rowx, end_rowx)
            ]

    ##
    # Returns a slice of the values of the cells in the given column.
    def col_values(self, colx, start_rowx=0, end_rowx=None):
        nr = self.nrows
        if start_rowx < 0:
            start_rowx += nr
            if start_rowx < 0:
                start_rowx = 0
        if end_rowx is None or end_rowx > nr:
            end_rowx = nr
        elif end_rowx < 0:
            end_rowx += nr
        return [
            self._cell_values[rowx][colx]
            for rowx in xrange(start_rowx, end_rowx)
            ]

    ##
    # Returns a slice of the types of the cells in the given column.
    def col_types(self, colx, start_rowx=0, end_rowx=None):
        nr = self.nrows
        if start_rowx < 0:
            start_rowx += nr
            if start_rowx < 0:
                start_rowx = 0
        if end_rowx is None or end_rowx > nr:
            end_rowx = nr
        elif end_rowx < 0:
            end_rowx += nr
        return [
            self._cell_types[rowx][colx]
            for rowx in xrange(start_rowx, end_rowx)
            ]

    ##
    # Returns a sequence of the {@link #Cell} objects in the given column.
    def col(self, colx):
        return self.col_slice(colx)
    # Above two lines just for the docs. Here's the real McCoy:
    col = col_slice

    # === Following methods are used in building the worksheet.
    # === They are not part of the API.

    def tidy_dimensions(self):
        if self.verbosity >= 3:
            fprintf(self.logfile,
                "tidy_dimensions: nrows=%d ncols=%d \n",
                self.nrows, self.ncols,
                )
        if 1 and self.merged_cells:
            nr = nc = 0
            umaxrows = self.utter_max_rows
            umaxcols = self.utter_max_cols
            for crange in self.merged_cells:
                rlo, rhi, clo, chi = crange
                if not (0 <= rlo < rhi <= umaxrows) \
                or not (0 <= clo < chi <= umaxcols):
                    fprintf(self.logfile,
                        "*** WARNING: sheet #%d (%r), MERGEDCELLS bad range %r\n",
                        self.number, self.name, crange)
                if rhi > nr: nr = rhi
                if chi > nc: nc = chi
            if nc > self.ncols:
                self.ncols = nc
            if nr > self.nrows:
                # we put one empty cell at (nr-1,0) to make sure
                # we have the right number of rows. The ragged rows
                # will sort out the rest if needed.
                self.put_cell(nr-1, 0, XL_CELL_EMPTY, -1)
        if self.verbosity >= 1 \
        and (self.nrows != self._dimnrows or self.ncols != self._dimncols):
            fprintf(self.logfile,
                "NOTE *** sheet %d (%r): DIMENSIONS R,C = %d,%d should be %d,%d\n",
                self.number,
                self.name,
                self._dimnrows,
                self._dimncols,
                self.nrows,
                self.ncols,
                )
        if not self.ragged_rows:
            # fix ragged rows
            ncols = self.ncols
            s_cell_types = self._cell_types
            s_cell_values = self._cell_values
            s_cell_xf_indexes = self._cell_xf_indexes
            s_fmt_info = self.formatting_info
            # for rowx in xrange(self.nrows):
            if self._first_full_rowx == -2:
                ubound = self.nrows
            else:
                ubound = self._first_full_rowx
            for rowx in xrange(ubound):
                trow = s_cell_types[rowx]
                rlen = len(trow)
                nextra = ncols - rlen
                if nextra > 0:
                    s_cell_values[rowx][rlen:] = [''] * nextra
                    trow[rlen:] = self.bt * nextra
                    if s_fmt_info:
                        s_cell_xf_indexes[rowx][rlen:] = self.bf * nextra

    def put_cell_ragged(self, rowx, colx, ctype, value, xf_index):
        if ctype is None:
            # we have a number, so look up the cell type
            ctype = self._xf_index_to_xl_type_map[xf_index]
        assert 0 <= colx < self.utter_max_cols
        assert 0 <= rowx < self.utter_max_rows
        fmt_info = self.formatting_info

        try:
            nr = rowx + 1
            if self.nrows < nr:

                scta = self._cell_types.append
                scva = self._cell_values.append
                scxa = self._cell_xf_indexes.append
                bt = self.bt
                bf = self.bf
                for _unused in xrange(self.nrows, nr):
                    scta(bt * 0)
                    scva([])
                    if fmt_info:
                        scxa(bf * 0)
                self.nrows = nr

            types_row = self._cell_types[rowx]
            values_row = self._cell_values[rowx]
            if fmt_info:
                fmt_row = self._cell_xf_indexes[rowx]
            ltr = len(types_row)
            if colx >= self.ncols:
                self.ncols = colx + 1
            num_empty = colx - ltr
            if not num_empty:
                # most common case: colx == previous colx + 1
                # self._put_cell_cells_appended += 1
                types_row.append(ctype)
                values_row.append(value)
                if fmt_info:
                    fmt_row.append(xf_index)
                return
            if num_empty > 0:
                num_empty += 1
                # self._put_cell_row_widenings += 1
                # types_row.extend(self.bt * num_empty)
                # values_row.extend([''] * num_empty)
                # if fmt_info:
                #     fmt_row.extend(self.bf * num_empty)
                types_row[ltr:] = self.bt * num_empty
                values_row[ltr:] = [''] * num_empty
                if fmt_info:
                    fmt_row[ltr:] = self.bf * num_empty
            types_row[colx] = ctype
            values_row[colx] = value
            if fmt_info:
                fmt_row[colx] = xf_index
        except:
            print >> self.logfile, "put_cell", rowx, colx
            raise

    def put_cell_unragged(self, rowx, colx, ctype, value, xf_index):
        if ctype is None:
            # we have a number, so look up the cell type
            ctype = self._xf_index_to_xl_type_map[xf_index]
        # assert 0 <= colx < self.utter_max_cols
        # assert 0 <= rowx < self.utter_max_rows
        try:
            self._cell_types[rowx][colx] = ctype
            self._cell_values[rowx][colx] = value
            if self.formatting_info:
                self._cell_xf_indexes[rowx][colx] = xf_index
        except IndexError:
            # print >> self.logfile, "put_cell extending", rowx, colx
            # self.extend_cells(rowx+1, colx+1)
            # self._put_cell_exceptions += 1
            nr = rowx + 1
            nc = colx + 1
            assert 1 <= nc <= self.utter_max_cols
            assert 1 <= nr <= self.utter_max_rows
            if nc > self.ncols:
                self.ncols = nc
                # The row self._first_full_rowx and all subsequent rows
                # are guaranteed to have length == self.ncols. Thus the
                # "fix ragged rows" section of the tidy_dimensions method
                # doesn't need to examine them.
                if nr < self.nrows:
                    # cell data is not in non-descending row order *AND*
                    # self.ncols has been bumped up.
                    # This very rare case ruins this optmisation.
                    self._first_full_rowx = -2
                elif rowx > self._first_full_rowx > -2:
                    self._first_full_rowx = rowx
            if nr <= self.nrows:
                # New cell is in an existing row, so extend that row (if necessary).
                # Note that nr < self.nrows means that the cell data
                # is not in ascending row order!!
                trow = self._cell_types[rowx]
                nextra = self.ncols - len(trow)
                if nextra > 0:
                    # self._put_cell_row_widenings += 1
                    trow.extend(self.bt * nextra)
                    if self.formatting_info:
                        self._cell_xf_indexes[rowx].extend(self.bf * nextra)
                    self._cell_values[rowx].extend([''] * nextra)
            else:
                scta = self._cell_types.append
                scva = self._cell_values.append
                scxa = self._cell_xf_indexes.append
                fmt_info = self.formatting_info
                nc = self.ncols
                bt = self.bt
                bf = self.bf
                for _unused in xrange(self.nrows, nr):
                    # self._put_cell_rows_appended += 1
                    scta(bt * nc)
                    scva([''] * nc)
                    if fmt_info:
                        scxa(bf * nc)
                self.nrows = nr
            # === end of code from extend_cells()
            try:
                self._cell_types[rowx][colx] = ctype
                self._cell_values[rowx][colx] = value
                if self.formatting_info:
                    self._cell_xf_indexes[rowx][colx] = xf_index
            except:
                print >> self.logfile, "put_cell", rowx, colx
                raise
        except:
           print >> self.logfile, "put_cell", rowx, colx
           raise


    # === Methods after this line neither know nor care about how cells are stored.

    def read(self, bk):
        global rc_stats
        DEBUG = 0
        blah = DEBUG or self.verbosity >= 2
        blah_rows = DEBUG or self.verbosity >= 4
        blah_formulas = 0 and blah
        r1c1 = 0
        oldpos = bk._position
        bk._position = self._position
        XL_SHRFMLA_ETC_ETC = (
            XL_SHRFMLA, XL_ARRAY, XL_TABLEOP, XL_TABLEOP2,
            XL_ARRAY2, XL_TABLEOP_B2,
            )
        self_put_cell = self.put_cell
        local_unpack = unpack
        bk_get_record_parts = bk.get_record_parts
        bv = self.biff_version
        fmt_info = self.formatting_info
        do_sst_rich_text = fmt_info and bk._rich_text_runlist_map
        rowinfo_sharing_dict = {}
        txos = {}
        eof_found = 0
        while 1:
            # if DEBUG: print "SHEET.READ: about to read from position %d" % bk._position
            rc, data_len, data = bk_get_record_parts()
            # if rc in rc_stats:
            #     rc_stats[rc] += 1
            # else:
            #     rc_stats[rc] = 1
            # if DEBUG: print "SHEET.READ: op 0x%04x, %d bytes %r" % (rc, data_len, data)
            if rc == XL_NUMBER:
                # [:14] in following stmt ignores extraneous rubbish at end of record.
                # Sample file testEON-8.xls supplied by Jan Kraus.
                rowx, colx, xf_index, d = local_unpack('<HHHd', data[:14])
                # if xf_index == 0:
                #     fprintf(self.logfile,
                #         "NUMBER: r=%d c=%d xfx=%d %f\n", rowx, colx, xf_index, d)
                self_put_cell(rowx, colx, None, d, xf_index)
            elif rc == XL_LABELSST:
                rowx, colx, xf_index, sstindex = local_unpack('<HHHi', data)
                # print "LABELSST", rowx, colx, sstindex, bk._sharedstrings[sstindex]
                self_put_cell(rowx, colx, XL_CELL_TEXT, bk._sharedstrings[sstindex], xf_index)
                if do_sst_rich_text:
                    runlist = bk._rich_text_runlist_map.get(sstindex)
                    if runlist:
                        self.rich_text_runlist_map[(rowx, colx)] = runlist
            elif rc == XL_LABEL:
                rowx, colx, xf_index = local_unpack('<HHH', data[0:6])
                if bv < BIFF_FIRST_UNICODE:
                    strg = unpack_string(data, 6, bk.encoding or bk.derive_encoding(), lenlen=2)
                else:
                    strg = unpack_unicode(data, 6, lenlen=2)
                self_put_cell(rowx, colx, XL_CELL_TEXT, strg, xf_index)
            elif rc == XL_RSTRING:
                rowx, colx, xf_index = local_unpack('<HHH', data[0:6])
                if bv < BIFF_FIRST_UNICODE:
                    strg, pos = unpack_string_update_pos(data, 6, bk.encoding or bk.derive_encoding(), lenlen=2)
                    nrt = ord(data[pos])
                    pos += 1
                    runlist = []
                    for _unused in xrange(nrt):
                        runlist.append(unpack('<BB', data[pos:pos+2]))
                        pos += 2
                    assert pos == len(data)
                else:
                    strg, pos = unpack_unicode_update_pos(data, 6, lenlen=2)
                    nrt = unpack('<H', data[pos:pos+2])[0]
                    pos += 2
                    runlist = []
                    for _unused in xrange(nrt):
                        runlist.append(unpack('<HH', data[pos:pos+4]))
                        pos += 4
                    assert pos == len(data)
                self_put_cell(rowx, colx, XL_CELL_TEXT, strg, xf_index)
                self.rich_text_runlist_map[(rowx, colx)] = runlist
            elif rc == XL_RK:
                rowx, colx, xf_index = local_unpack('<HHH', data[:6])
                d = unpack_RK(data[6:10])
                self_put_cell(rowx, colx, None, d, xf_index)
            elif rc == XL_MULRK:
                mulrk_row, mulrk_first = local_unpack('<HH', data[0:4])
                mulrk_last, = local_unpack('<H', data[-2:])
                pos = 4
                for colx in xrange(mulrk_first, mulrk_last+1):
                    xf_index, = local_unpack('<H', data[pos:pos+2])
                    d = unpack_RK(data[pos+2:pos+6])
                    pos += 6
                    self_put_cell(mulrk_row, colx, None, d, xf_index)
            elif rc == XL_ROW:
                # Version 0.6.0a3: ROW records are just not worth using (for memory allocation).
                # Version 0.6.1: now used for formatting info.
                if not fmt_info: continue
                rowx, bits1, bits2 = local_unpack('<H4xH4xi', data[0:16])
                if not(0 <= rowx < self.utter_max_rows):
                    print >> self.logfile, \
                        "*** NOTE: ROW record has row index %d; " \
                        "should have 0 <= rowx < %d -- record ignored!" \
                        % (rowx, self.utter_max_rows)
                    continue
                key = (bits1, bits2)
                r = rowinfo_sharing_dict.get(key)
                if r is None:
                    rowinfo_sharing_dict[key] = r = Rowinfo()
                    # Using upkbits() is far too slow on a file
                    # with 30 sheets each with 10K rows :-(
                    #    upkbits(r, bits1, (
                    #        ( 0, 0x7FFF, 'height'),
                    #        (15, 0x8000, 'has_default_height'),
                    #        ))
                    #    upkbits(r, bits2, (
                    #        ( 0, 0x00000007, 'outline_level'),
                    #        ( 4, 0x00000010, 'outline_group_starts_ends'),
                    #        ( 5, 0x00000020, 'hidden'),
                    #        ( 6, 0x00000040, 'height_mismatch'),
                    #        ( 7, 0x00000080, 'has_default_xf_index'),
                    #        (16, 0x0FFF0000, 'xf_index'),
                    #        (28, 0x10000000, 'additional_space_above'),
                    #        (29, 0x20000000, 'additional_space_below'),
                    #        ))
                    # So:
                    r.height = bits1 & 0x7fff
                    r.has_default_height = (bits1 >> 15) & 1
                    r.outline_level = bits2 & 7
                    r.outline_group_starts_ends = (bits2 >> 4) & 1
                    r.hidden = (bits2 >> 5) & 1
                    r.height_mismatch = (bits2 >> 6) & 1
                    r.has_default_xf_index = (bits2 >> 7) & 1
                    r.xf_index = (bits2 >> 16) & 0xfff
                    r.additional_space_above = (bits2 >> 28) & 1
                    r.additional_space_below = (bits2 >> 29) & 1
                    if not r.has_default_xf_index:
                        r.xf_index = -1
                self.rowinfo_map[rowx] = r
                if 0 and r.xf_index > -1:
                    fprintf(self.logfile,
                        "**ROW %d %d %d\n",
                        self.number, rowx, r.xf_index)
                if blah_rows:
                    print >> self.logfile, 'ROW', rowx, bits1, bits2
                    r.dump(self.logfile,
                        header="--- sh #%d, rowx=%d ---" % (self.number, rowx))
            elif rc in XL_FORMULA_OPCODES: # 06, 0206, 0406
                # DEBUG = 1
                # if DEBUG: print "FORMULA: rc: 0x%04x data: %r" % (rc, data)
                if bv >= 50:
                    rowx, colx, xf_index, result_str, flags = local_unpack('<HHH8sH', data[0:16])
                    lenlen = 2
                    tkarr_offset = 20
                elif bv >= 30:
                    rowx, colx, xf_index, result_str, flags = local_unpack('<HHH8sH', data[0:16])
                    lenlen = 2
                    tkarr_offset = 16
                else: # BIFF2
                    rowx, colx, cell_attr,  result_str, flags = local_unpack('<HH3s8sB', data[0:16])
                    xf_index =  self.fixed_BIFF2_xfindex(cell_attr, rowx, colx)
                    lenlen = 1
                    tkarr_offset = 16
                if blah_formulas: # testing formula dumper
                    #### XXXX FIXME
                    fprintf(self.logfile, "FORMULA: rowx=%d colx=%d\n", rowx, colx)
                    fmlalen = local_unpack("<H", data[20:22])[0]
                    decompile_formula(bk, data[22:], fmlalen, FMLA_TYPE_CELL,
                        browx=rowx, bcolx=colx, blah=1, r1c1=r1c1)
                if result_str[6:8] == "\xFF\xFF":
                    if result_str[0]  == '\x00':
                        # need to read next record (STRING)
                        gotstring = 0
                        # if flags & 8:
                        if 1: # "flags & 8" applies only to SHRFMLA
                            # actually there's an optional SHRFMLA or ARRAY etc record to skip over
                            rc2, data2_len, data2 = bk.get_record_parts()
                            if rc2 == XL_STRING or rc2 == XL_STRING_B2:
                                gotstring = 1
                            elif rc2 == XL_ARRAY:
                                row1x, rownx, col1x, colnx, array_flags, tokslen = \
                                    local_unpack("<HHBBBxxxxxH", data2[:14])
                                if blah_formulas:
                                    fprintf(self.logfile, "ARRAY: %d %d %d %d %d\n",
                                        row1x, rownx, col1x, colnx, array_flags)
                                    # dump_formula(bk, data2[14:], tokslen, bv, reldelta=0, blah=1)
                            elif rc2 == XL_SHRFMLA:
                                row1x, rownx, col1x, colnx, nfmlas, tokslen = \
                                    local_unpack("<HHBBxBH", data2[:10])
                                if blah_formulas:
                                    fprintf(self.logfile, "SHRFMLA (sub): %d %d %d %d %d\n",
                                        row1x, rownx, col1x, colnx, nfmlas)
                                    decompile_formula(bk, data2[10:], tokslen, FMLA_TYPE_SHARED,
                                        blah=1, browx=rowx, bcolx=colx, r1c1=r1c1)
                            elif rc2 not in XL_SHRFMLA_ETC_ETC:
                                raise XLRDError(
                                    "Expected SHRFMLA, ARRAY, TABLEOP* or STRING record; found 0x%04x" % rc2)
                            # if DEBUG: print "gotstring:", gotstring
                        # now for the STRING record
                        if not gotstring:
                            rc2, _unused_len, data2 = bk.get_record_parts()
                            if rc2 not in (XL_STRING, XL_STRING_B2):
                                raise XLRDError("Expected STRING record; found 0x%04x" % rc2)
                        # if DEBUG: print "STRING: data=%r BIFF=%d cp=%d" % (data2, self.biff_version, bk.encoding)
                        strg = self.string_record_contents(data2)
                        self.put_cell(rowx, colx, XL_CELL_TEXT, strg, xf_index)
                        # if DEBUG: print "FORMULA strg %r" % strg
                    elif result_str[0] == '\x01':
                        # boolean formula result
                        value = ord(result_str[2])
                        self_put_cell(rowx, colx, XL_CELL_BOOLEAN, value, xf_index)
                    elif result_str[0] == '\x02':
                        # Error in cell
                        value = ord(result_str[2])
                        self_put_cell(rowx, colx, XL_CELL_ERROR, value, xf_index)
                    elif result_str[0] == '\x03':
                        # empty ... i.e. empty (zero-length) string, NOT an empty cell.
                        self_put_cell(rowx, colx, XL_CELL_TEXT, u"", xf_index)
                    else:
                        raise XLRDError("unexpected special case (0x%02x) in FORMULA" % ord(result_str[0]))
                else:
                    # it is a number
                    d = local_unpack('<d', result_str)[0]
                    self_put_cell(rowx, colx, None, d, xf_index)
            elif rc == XL_BOOLERR:
                rowx, colx, xf_index, value, is_err = local_unpack('<HHHBB', data[:8])
                # Note OOo Calc 2.0 writes 9-byte BOOLERR records.
                # OOo docs say 8. Excel writes 8.
                cellty = (XL_CELL_BOOLEAN, XL_CELL_ERROR)[is_err]
                # if DEBUG: print "XL_BOOLERR", rowx, colx, xf_index, value, is_err
                self_put_cell(rowx, colx, cellty, value, xf_index)
            elif rc == XL_COLINFO:
                if not fmt_info: continue
                c = Colinfo()
                first_colx, last_colx, c.width, c.xf_index, flags \
                    = local_unpack("<HHHHH", data[:10])
                #### Colinfo.width is denominated in 256ths of a character,
                #### *not* in characters.
                if not(0 <= first_colx <= last_colx <= 256):
                    # Note: 256 instead of 255 is a common mistake.
                    # We silently ignore the non-existing 257th column in that case.
                    print >> self.logfile, \
                        "*** NOTE: COLINFO record has first col index %d, last %d; " \
                        "should have 0 <= first <= last <= 255 -- record ignored!" \
                        % (first_colx, last_colx)
                    del c
                    continue
                upkbits(c, flags, (
                    ( 0, 0x0001, 'hidden'),
                    ( 1, 0x0002, 'bit1_flag'),
                    # *ALL* colinfos created by Excel in "default" cases are 0x0002!!
                    # Maybe it's "locked" by analogy with XFProtection data.
                    ( 8, 0x0700, 'outline_level'),
                    (12, 0x1000, 'collapsed'),
                    ))
                for colx in xrange(first_colx, last_colx+1):
                    if colx > 255: break # Excel does 0 to 256 inclusive
                    self.colinfo_map[colx] = c
                    if 0:
                        fprintf(self.logfile,
                            "**COL %d %d %d\n",
                            self.number, colx, c.xf_index)
                if blah:
                    fprintf(
                        self.logfile,
                        "COLINFO sheet #%d cols %d-%d: wid=%d xf_index=%d flags=0x%04x\n",
                        self.number, first_colx, last_colx, c.width, c.xf_index, flags,
                        )
                    c.dump(self.logfile, header='===')
            elif rc == XL_DEFCOLWIDTH:
                self.defcolwidth, = local_unpack("<H", data[:2])
                if 0: print >> self.logfile, 'DEFCOLWIDTH', self.defcolwidth
            elif rc == XL_STANDARDWIDTH:
                if data_len != 2:
                    print >> self.logfile, '*** ERROR *** STANDARDWIDTH', data_len, repr(data)
                self.standardwidth, = local_unpack("<H", data[:2])
                if 0: print >> self.logfile, 'STANDARDWIDTH', self.standardwidth
            elif rc == XL_GCW:
                if not fmt_info: continue # useless w/o COLINFO
                assert data_len == 34
                assert data[0:2] == "\x20\x00"
                iguff = unpack("<8i", data[2:34])
                gcw = []
                for bits in iguff:
                    for j in xrange(32):
                        gcw.append(bits & 1)
                        bits >>= 1
                self.gcw = tuple(gcw)
                if 0:
                    showgcw = "".join(map(lambda x: "F "[x], gcw)).rstrip().replace(' ', '.')
                    print >> self.logfile, "GCW:", showgcw
            elif rc == XL_BLANK:
                if not fmt_info: continue
                rowx, colx, xf_index = local_unpack('<HHH', data[:6])
                # if 0: print >> self.logfile, "BLANK", rowx, colx, xf_index
                self_put_cell(rowx, colx, XL_CELL_BLANK, '', xf_index)
            elif rc == XL_MULBLANK: # 00BE
                if not fmt_info: continue
                nitems = data_len >> 1
                result = local_unpack("<%dH" % nitems, data)
                rowx, mul_first = result[:2]
                mul_last = result[-1]
                # print >> self.logfile, "MULBLANK", rowx, mul_first, mul_last, data_len, nitems, mul_last + 4 - mul_first
                assert nitems == mul_last + 4 - mul_first
                pos = 2
                for colx in xrange(mul_first, mul_last + 1):
                    self_put_cell(rowx, colx, XL_CELL_BLANK, '', result[pos])
                    pos += 1
            elif rc == XL_DIMENSION or rc == XL_DIMENSION2:
                # if data_len == 10:
                # Was crashing on BIFF 4.0 file w/o the two trailing unused bytes.
                # Reported by Ralph Heimburger.
                if bv < 80:
                    dim_tuple = local_unpack('<HxxH', data[2:8])
                else:
                    dim_tuple = local_unpack('<ixxH', data[4:12])
                self.nrows, self.ncols = 0, 0
                self._dimnrows, self._dimncols = dim_tuple
                if bv in (21, 30, 40) and self.book.xf_list and not self.book._xf_epilogue_done:
                    self.book.xf_epilogue()
                if blah:
                    fprintf(self.logfile,
                        "sheet %d(%r) DIMENSIONS: ncols=%d nrows=%d\n",
                        self.number, self.name, self._dimncols, self._dimnrows
                        )
            elif rc == XL_HLINK:
                self.handle_hlink(data)
            elif rc == XL_QUICKTIP:
                self.handle_quicktip(data)
            elif rc == XL_EOF:
                DEBUG = 0
                if DEBUG: print >> self.logfile, "SHEET.READ: EOF"
                eof_found = 1
                break
            elif rc == XL_OBJ:
                # handle SHEET-level objects; note there's a separate Book.handle_obj
                saved_obj = self.handle_obj(data)
                if saved_obj: saved_obj_id = saved_obj.id
                else: saved_obj_id = None
            elif rc == XL_MSO_DRAWING:
                self.handle_msodrawingetc(rc, data_len, data)
            elif rc == XL_TXO:
                txo = self.handle_txo(data)
                if txo and saved_obj_id:
                    txos[saved_obj_id] = txo
                    saved_obj_id = None
            elif rc == XL_NOTE:
                self.handle_note(data, txos)
            elif rc == XL_FEAT11:
                self.handle_feat11(data)
            elif rc in bofcodes: ##### EMBEDDED BOF #####
                version, boftype = local_unpack('<HH', data[0:4])
                if boftype != 0x20: # embedded chart
                    print >> self.logfile, \
                        "*** Unexpected embedded BOF (0x%04x) at offset %d: version=0x%04x type=0x%04x" \
                        % (rc, bk._position - data_len - 4, version, boftype)
                while 1:
                    code, data_len, data = bk.get_record_parts()
                    if code == XL_EOF:
                        break
                if DEBUG: print >> self.logfile, "---> found EOF"
            elif rc == XL_COUNTRY:
                bk.handle_country(data)
            elif rc == XL_LABELRANGES:
                pos = 0
                pos = unpack_cell_range_address_list_update_pos(
                        self.row_label_ranges, data, pos, bv, addr_size=8,
                        )
                pos = unpack_cell_range_address_list_update_pos(
                        self.col_label_ranges, data, pos, bv, addr_size=8,
                        )
                assert pos == data_len
            elif rc == XL_ARRAY:
                row1x, rownx, col1x, colnx, array_flags, tokslen = \
                    local_unpack("<HHBBBxxxxxH", data[:14])
                if blah_formulas:
                    print >> self.logfile, "ARRAY:", row1x, rownx, col1x, colnx, array_flags
                    # dump_formula(bk, data[14:], tokslen, bv, reldelta=0, blah=1)
            elif rc == XL_SHRFMLA:
                row1x, rownx, col1x, colnx, nfmlas, tokslen = \
                    local_unpack("<HHBBxBH", data[:10])
                if blah_formulas:
                    print >> self.logfile, "SHRFMLA (main):", row1x, rownx, col1x, colnx, nfmlas
                    decompile_formula(bk, data[10:], tokslen, FMLA_TYPE_SHARED,
                        blah=1, browx=rowx, bcolx=colx, r1c1=r1c1)
            elif rc == XL_CONDFMT:
                if not fmt_info: continue
                assert bv >= 80
                num_CFs, needs_recalc, browx1, browx2, bcolx1, bcolx2 = \
                    unpack("<6H", data[0:12])
                if self.verbosity >= 1:
                    fprintf(self.logfile,
                        "\n*** WARNING: Ignoring CONDFMT (conditional formatting) record\n" \
                        "*** in Sheet %d (%r).\n" \
                        "*** %d CF record(s); needs_recalc_or_redraw = %d\n" \
                        "*** Bounding box is %s\n",
                        self.number, self.name, num_CFs, needs_recalc,
                        rangename2d(browx1, browx2+1, bcolx1, bcolx2+1),
                        )
                olist = [] # updated by the function
                pos = unpack_cell_range_address_list_update_pos(
                    olist, data, 12, bv, addr_size=8)
                # print >> self.logfile, repr(result), len(result)
                if self.verbosity >= 1:
                    fprintf(self.logfile,
                        "*** %d individual range(s):\n" \
                        "*** %s\n",
                        len(olist),
                        ", ".join([rangename2d(*coords) for coords in olist]),
                        )
            elif rc == XL_CF:
                if not fmt_info: continue
                cf_type, cmp_op, sz1, sz2, flags = unpack("<BBHHi", data[0:10])
                font_block = (flags >> 26) & 1
                bord_block = (flags >> 28) & 1
                patt_block = (flags >> 29) & 1
                if self.verbosity >= 1:
                    fprintf(self.logfile,
                        "\n*** WARNING: Ignoring CF (conditional formatting) sub-record.\n" \
                        "*** cf_type=%d, cmp_op=%d, sz1=%d, sz2=%d, flags=0x%08x\n" \
                        "*** optional data blocks: font=%d, border=%d, pattern=%d\n",
                        cf_type, cmp_op, sz1, sz2, flags,
                        font_block, bord_block, patt_block,
                        )
                # hex_char_dump(data, 0, data_len, fout=self.logfile)
                pos = 12
                if font_block:
                    (font_height, font_options, weight, escapement, underline,
                    font_colour_index, two_bits, font_esc, font_underl) = \
                    unpack("<64x i i H H B 3x i 4x i i i 18x", data[pos:pos+118])
                    font_style = (two_bits > 1) & 1
                    posture = (font_options > 1) & 1
                    font_canc = (two_bits > 7) & 1
                    cancellation = (font_options > 7) & 1
                    if self.verbosity >= 1:
                        fprintf(self.logfile,
                            "*** Font info: height=%d, weight=%d, escapement=%d,\n" \
                            "*** underline=%d, colour_index=%d, esc=%d, underl=%d,\n" \
                            "*** style=%d, posture=%d, canc=%d, cancellation=%d\n",
                            font_height, weight, escapement, underline,
                            font_colour_index, font_esc, font_underl,
                            font_style, posture, font_canc, cancellation,
                            )
                    pos += 118
                if bord_block:
                    pos += 8
                if patt_block:
                    pos += 4
                fmla1 = data[pos:pos+sz1]
                pos += sz1
                if blah and sz1:
                    fprintf(self.logfile,
                        "*** formula 1:\n",
                        )
                    dump_formula(bk, fmla1, sz1, bv, reldelta=0, blah=1)
                fmla2 = data[pos:pos+sz2]
                pos += sz2
                assert pos == data_len
                if blah and sz2:
                    fprintf(self.logfile,
                        "*** formula 2:\n",
                        )
                    dump_formula(bk, fmla2, sz2, bv, reldelta=0, blah=1)
            elif rc == XL_DEFAULTROWHEIGHT:
                if data_len == 4:
                    bits, self.default_row_height = unpack("<HH", data[:4])
                elif data_len == 2:
                    self.default_row_height, = unpack("<H", data)
                    bits = 0
                    fprintf(self.logfile,
                        "*** WARNING: DEFAULTROWHEIGHT record len is 2, " \
                        "should be 4; assuming BIFF2 format\n")
                else:
                    bits = 0
                    fprintf(self.logfile,
                        "*** WARNING: DEFAULTROWHEIGHT record len is %d, " \
                        "should be 4; ignoring this record\n",
                        data_len)
                self.default_row_height_mismatch = bits & 1
                self.default_row_hidden = (bits >> 1) & 1
                self.default_additional_space_above = (bits >> 2) & 1
                self.default_additional_space_below = (bits >> 3) & 1
            elif rc == XL_MERGEDCELLS:
                if not fmt_info: continue
                pos = unpack_cell_range_address_list_update_pos(
                    self.merged_cells, data, 0, bv, addr_size=8)
                if blah:
                    fprintf(self.logfile,
                        "MERGEDCELLS: %d ranges\n", int_floor_div(pos - 2, 8))
                assert pos == data_len, \
                    "MERGEDCELLS: pos=%d data_len=%d" % (pos, data_len)
            elif rc == XL_WINDOW2:
                if bv >= 80 and data_len >= 14:
                    (options,
                    self.first_visible_rowx, self.first_visible_colx,
                    self.gridline_colour_index,
                    self.cached_page_break_preview_mag_factor,
                    self.cached_normal_view_mag_factor
                    ) = unpack("<HHHHxxHH", data[:14])
                else:
                    assert bv >= 30 # BIFF3-7
                    (options,
                    self.first_visible_rowx, self.first_visible_colx,
                    ) = unpack("<HHH", data[:6])
                    self.gridline_colour_rgb = unpack("<BBB", data[6:9])
                    self.gridline_colour_index = nearest_colour_index(
                        self.book.colour_map, self.gridline_colour_rgb, debug=0)
                    self.cached_page_break_preview_mag_factor = 0 # default (60%)
                    self.cached_normal_view_mag_factor = 0 # default (100%)
                # options -- Bit, Mask, Contents:
                # 0 0001H 0 = Show formula results 1 = Show formulas
                # 1 0002H 0 = Do not show grid lines 1 = Show grid lines
                # 2 0004H 0 = Do not show sheet headers 1 = Show sheet headers
                # 3 0008H 0 = Panes are not frozen 1 = Panes are frozen (freeze)
                # 4 0010H 0 = Show zero values as empty cells 1 = Show zero values
                # 5 0020H 0 = Manual grid line colour 1 = Automatic grid line colour
                # 6 0040H 0 = Columns from left to right 1 = Columns from right to left
                # 7 0080H 0 = Do not show outline symbols 1 = Show outline symbols
                # 8 0100H 0 = Keep splits if pane freeze is removed 1 = Remove splits if pane freeze is removed
                # 9 0200H 0 = Sheet not selected 1 = Sheet selected (BIFF5-BIFF8)
                # 10 0400H 0 = Sheet not visible 1 = Sheet visible (BIFF5-BIFF8)
                # 11 0800H 0 = Show in normal view 1 = Show in page break preview (BIFF8)
                # The freeze flag specifies, if a following PANE record (6.71) describes unfrozen or frozen panes.
                for attr, _unused_defval in _WINDOW2_options:
                    setattr(self, attr, options & 1)
                    options >>= 1
            elif rc == XL_SCL:
                num, den = unpack("<HH", data)
                result = 0
                if den:
                    result = int_floor_div(num * 100, den)
                if not(10 <= result <= 400):
                    if DEBUG or self.verbosity >= 0:
                        print >> self.logfile, (
                            "WARNING *** SCL rcd sheet %d: should have 0.1 <= num/den <= 4; got %d/%d"
                            % (self.number, num, den)
                            )
                    result = 100
                self.scl_mag_factor = result
            elif rc == XL_PANE:
                (
                self.vert_split_pos,
                self.horz_split_pos,
                self.horz_split_first_visible,
                self.vert_split_first_visible,
                self.split_active_pane,
                ) = unpack("<HHHHB", data[:9])
                self.has_pane_record = 1
            elif rc == XL_HORIZONTALPAGEBREAKS:
                if not fmt_info: continue
                num_breaks, = local_unpack("<H", data[:2])
                assert num_breaks * (2 + 4 * (bv >= 80)) + 2 == data_len
                pos = 2
                if bv < 80:
                    while pos < data_len:
                        self.horizontal_page_breaks.append((local_unpack("<H", data[pos:pos+2])[0], 0, 255))
                        pos += 2
                else:
                    while pos < data_len:
                        self.horizontal_page_breaks.append(local_unpack("<HHH", data[pos:pos+6]))
                        pos += 6
            elif rc == XL_VERTICALPAGEBREAKS:
                if not fmt_info: continue
                num_breaks, = local_unpack("<H", data[:2])
                assert num_breaks * (2 + 4 * (bv >= 80)) + 2 == data_len
                pos = 2
                if bv < 80:
                    while pos < data_len:
                        self.vertical_page_breaks.append((local_unpack("<H", data[pos:pos+2])[0], 0, 65535))
                        pos += 2
                else:
                    while pos < data_len:
                        self.vertical_page_breaks.append(local_unpack("<HHH", data[pos:pos+6]))
                        pos += 6
            #### all of the following are for BIFF <= 4W
            elif bv <= 45:
                if rc == XL_FORMAT or rc == XL_FORMAT2:
                    bk.handle_format(data, rc)
                elif rc == XL_FONT or rc == XL_FONT_B3B4:
                    bk.handle_font(data)
                elif rc == XL_STYLE:
                    if not self.book._xf_epilogue_done:
                        self.book.xf_epilogue()
                    bk.handle_style(data)
                elif rc == XL_PALETTE:
                    bk.handle_palette(data)
                elif rc == XL_BUILTINFMTCOUNT:
                    bk.handle_builtinfmtcount(data)
                elif rc == XL_XF4 or rc == XL_XF3 or rc == XL_XF2: #### N.B. not XL_XF
                    bk.handle_xf(data)
                elif rc == XL_DATEMODE:
                    bk.handle_datemode(data)
                elif rc == XL_CODEPAGE:
                    bk.handle_codepage(data)
                elif rc == XL_FILEPASS:
                    bk.handle_filepass(data)
                elif rc == XL_WRITEACCESS:
                    bk.handle_writeaccess(data)
                elif rc == XL_IXFE:
                    self._ixfe = local_unpack('<H', data)[0]
                elif rc == XL_NUMBER_B2:
                    rowx, colx, cell_attr, d = local_unpack('<HH3sd', data)
                    self_put_cell(rowx, colx, None, d, self.fixed_BIFF2_xfindex(cell_attr, rowx, colx))
                elif rc == XL_INTEGER:
                    rowx, colx, cell_attr, d = local_unpack('<HH3sH', data)
                    self_put_cell(rowx, colx, None, float(d), self.fixed_BIFF2_xfindex(cell_attr, rowx, colx))
                elif rc == XL_LABEL_B2:
                    rowx, colx, cell_attr = local_unpack('<HH3s', data[0:7])
                    strg = unpack_string(data, 7, bk.encoding or bk.derive_encoding(), lenlen=1)
                    self_put_cell(rowx, colx, XL_CELL_TEXT, strg, self.fixed_BIFF2_xfindex(cell_attr, rowx, colx))
                elif rc == XL_BOOLERR_B2:
                    rowx, colx, cell_attr, value, is_err = local_unpack('<HH3sBB', data)
                    cellty = (XL_CELL_BOOLEAN, XL_CELL_ERROR)[is_err]
                    # if DEBUG: print "XL_BOOLERR_B2", rowx, colx, cell_attr, value, is_err
                    self_put_cell(rowx, colx, cellty, value, self.fixed_BIFF2_xfindex(cell_attr, rowx, colx))
                elif rc == XL_BLANK_B2:
                    if not fmt_info: continue
                    rowx, colx, cell_attr = local_unpack('<HH3s', data[:7])
                    self_put_cell(rowx, colx, XL_CELL_BLANK, '', self.fixed_BIFF2_xfindex(cell_attr, rowx, colx))
                elif rc == XL_EFONT:
                    bk.handle_efont(data)
                elif rc == XL_ROW_B2:
                    if not fmt_info: continue
                    rowx, bits1, bits2 = local_unpack('<H4xH2xB', data[0:11])
                    if not(0 <= rowx < self.utter_max_rows):
                        print >> self.logfile, \
                            "*** NOTE: ROW_B2 record has row index %d; " \
                            "should have 0 <= rowx < %d -- record ignored!" \
                            % (rowx, self.utter_max_rows)
                        continue
                    if not (bits2 & 1):  # has_default_xf_index is false
                        xf_index = -1
                    elif data_len == 18:
                        # Seems the XF index in the cell_attr is dodgy
                         xfx = local_unpack('<H', data[16:18])[0]
                         xf_index = self.fixed_BIFF2_xfindex(cell_attr=None, rowx=rowx, colx=-1, true_xfx=xfx)
                    else:
                        cell_attr = data[13:16]
                        xf_index = self.fixed_BIFF2_xfindex(cell_attr, rowx, colx=-1)
                    key = (bits1, bits2, xf_index)
                    r = rowinfo_sharing_dict.get(key)
                    if r is None:
                        rowinfo_sharing_dict[key] = r = Rowinfo()
                        r.height = bits1 & 0x7fff
                        r.has_default_height = (bits1 >> 15) & 1
                        r.has_default_xf_index = bits2 & 1
                        r.xf_index = xf_index
                        # r.outline_level = 0             # set in __init__
                        # r.outline_group_starts_ends = 0 # set in __init__
                        # r.hidden = 0                    # set in __init__
                        # r.height_mismatch = 0           # set in __init__
                        # r.additional_space_above = 0    # set in __init__
                        # r.additional_space_below = 0    # set in __init__
                    self.rowinfo_map[rowx] = r
                    if 0 and r.xf_index > -1:
                        fprintf(self.logfile,
                            "**ROW %d %d %d\n",
                            self.number, rowx, r.xf_index)
                    if blah_rows:
                        print >> self.logfile, 'ROW_B2', rowx, bits1, has_defaults
                        r.dump(self.logfile,
                            header="--- sh #%d, rowx=%d ---" % (self.number, rowx))
                elif rc == XL_COLWIDTH: # BIFF2 only
                    if not fmt_info: continue
                    first_colx, last_colx, width\
                        = local_unpack("<BBH", data[:4])
                    if not(first_colx <= last_colx):
                        print >> self.logfile, \
                            "*** NOTE: COLWIDTH record has first col index %d, last %d; " \
                            "should have first <= last -- record ignored!" \
                            % (first_colx, last_colx)
                        continue
                    for colx in xrange(first_colx, last_colx+1):
                        if self.colinfo_map.has_key(colx):
                            c = self.colinfo_map[colx]
                        else:
                            c = Colinfo()
                            self.colinfo_map[colx] = c
                        c.width = width
                    if blah:
                        fprintf(
                            self.logfile,
                            "COLWIDTH sheet #%d cols %d-%d: wid=%d\n",
                            self.number, first_colx, last_colx, width
                            )
                elif rc == XL_COLUMNDEFAULT: # BIFF2 only
                    if not fmt_info: continue
                    first_colx, last_colx = local_unpack("<HH", data[:4])
                    #### Warning OOo docs wrong; first_colx <= colx < last_colx
                    if blah:
                        fprintf(
                            self.logfile,
                            "COLUMNDEFAULT sheet #%d cols in range(%d, %d)\n",
                            self.number, first_colx, last_colx
                            )
                    if not(0 <= first_colx < last_colx <= 256):
                        print >> self.logfile, \
                            "*** NOTE: COLUMNDEFAULT record has first col index %d, last %d; " \
                            "should have 0 <= first < last <= 256" \
                            % (first_colx, last_colx)
                        last_colx = min(last_colx, 256)
                    for colx in xrange(first_colx, last_colx):
                        offset = 4 + 3 * (colx - first_colx)
                        cell_attr = data[offset:offset+3]
                        xf_index = self.fixed_BIFF2_xfindex(cell_attr, rowx=-1, colx=colx)
                        if self.colinfo_map.has_key(colx):
                            c = self.colinfo_map[colx]
                        else:
                            c = Colinfo()
                            self.colinfo_map[colx] = c
                        c.xf_index = xf_index
                elif rc == XL_WINDOW2_B2: # BIFF 2 only
                    attr_names = ("show_formulas", "show_grid_lines", "show_sheet_headers",
                        "panes_are_frozen", "show_zero_values")
                    for attr, char in zip(attr_names, data[0:5]):
                        setattr(self, attr, int(char != "\x00"))
                    (self.first_visible_rowx, self.first_visible_colx,
                    self.automatic_grid_line_colour,
                    ) = unpack("<HHB", data[5:10])
                    self.gridline_colour_rgb = unpack("<BBB", data[10:13])
                    self.gridline_colour_index = nearest_colour_index(
                        self.book.colour_map, self.gridline_colour_rgb, debug=0)
                    self.cached_page_break_preview_mag_factor = 0 # default (60%)
                    self.cached_normal_view_mag_factor = 0 # default (100%)
            else:
                # if DEBUG: print "SHEET.READ: Unhandled record type %02x %d bytes %r" % (rc, data_len, data)
                pass
        if not eof_found:
            raise XLRDError("Sheet %d (%r) missing EOF record" \
                % (self.number, self.name))
        self.tidy_dimensions()
        self.update_cooked_mag_factors()
        bk._position = oldpos
        return 1
    
    def string_record_contents(self, data):
        bv = self.biff_version
        bk = self.book
        lenlen = (bv >= 30) + 1
        nchars_expected = unpack("<" + "BH"[lenlen - 1], data[:lenlen])[0]
        offset = lenlen
        if bv < 80:
            enc = bk.encoding or bk.derive_encoding()
        nchars_found = 0
        result = u""
        while 1:
            if bv >= 80:
                flag = ord(data[offset]) & 1
                enc = ("latin_1", "utf_16_le")[flag]
                offset += 1
            chunk = unicode(data[offset:], enc)
            result += chunk
            nchars_found += len(chunk)
            if nchars_found == nchars_expected:
                return result
            if nchars_found > nchars_expected:
                msg = ("STRING/CONTINUE: expected %d chars, found %d" 
                    % (nchars_expected, nchars_found))
                raise XLRDErrror(msg)
            rc, _unused_len, data = bk.get_record_parts()
            if rc != XL_CONTINUE:
                raise XLRDError(
                    "Expected CONTINUE record; found record-type 0x%04X" % rc)
            offset = 0

    def update_cooked_mag_factors(self):
        # Cached values are used ONLY for the non-active view mode.
        # When the user switches to the non-active view mode,
        # if the cached value for that mode is not valid,
        # Excel pops up a window which says:
        # "The number must be between 10 and 400. Try again by entering a number in this range."
        # When the user hits OK, it drops into the non-active view mode
        # but uses the magn from the active mode.
        # NOTE: definition of "valid" depends on mode ... see below
        blah = DEBUG or self.verbosity > 0
        if self.show_in_page_break_preview:
            if self.scl_mag_factor is None: # no SCL record
                self.cooked_page_break_preview_mag_factor = 100 # Yes, 100, not 60, NOT a typo
            else:
                self.cooked_page_break_preview_mag_factor = self.scl_mag_factor
            zoom = self.cached_normal_view_mag_factor
            if not (10 <= zoom <=400):
                if blah:
                    print >> self.logfile, (
                        "WARNING *** WINDOW2 rcd sheet %d: Bad cached_normal_view_mag_factor: %d"
                        % (self.number, self.cached_normal_view_mag_factor)
                        )
                zoom = self.cooked_page_break_preview_mag_factor
            self.cooked_normal_view_mag_factor = zoom
        else:
            # normal view mode
            if self.scl_mag_factor is None: # no SCL record
                self.cooked_normal_view_mag_factor = 100
            else:
                self.cooked_normal_view_mag_factor = self.scl_mag_factor
            zoom = self.cached_page_break_preview_mag_factor
            if zoom == 0:
                # VALID, defaults to 60
                zoom = 60
            elif not (10 <= zoom <= 400):
                if blah:
                    print >> self.logfile, (
                        "WARNING *** WINDOW2 rcd sheet %r: Bad cached_page_break_preview_mag_factor: %r"
                        % (self.number, self.cached_page_break_preview_mag_factor)
                        )
                zoom = self.cooked_normal_view_mag_factor
            self.cooked_page_break_preview_mag_factor = zoom

    def fixed_BIFF2_xfindex(self, cell_attr, rowx, colx, true_xfx=None):
        DEBUG = 0
        blah = DEBUG or self.verbosity >= 2
        if self.biff_version == 21:
            if self.book.xf_list:
                if true_xfx is not None:
                    xfx = true_xfx
                else:
                    xfx = ord(cell_attr[0]) & 0x3F
                if xfx == 0x3F:
                    if self._ixfe is None:
                        raise XLRDError("BIFF2 cell record has XF index 63 but no preceding IXFE record.")
                    xfx = self._ixfe
                    # OOo docs are capable of interpretation that each
                    # cell record is preceded immediately by its own IXFE record.
                    # Empirical evidence is that (sensibly) an IXFE record applies to all
                    # following cell records until another IXFE comes along.
                return xfx
            # Have either Excel 2.0, or broken 2.1 w/o XF records -- same effect.
            self.biff_version = self.book.biff_version = 20
        #### check that XF slot in cell_attr is zero
        xfx_slot = ord(cell_attr[0]) & 0x3F
        assert xfx_slot == 0
        xfx = self._cell_attr_to_xfx.get(cell_attr)
        if xfx is not None:
            return xfx
        if blah:
            fprintf(self.logfile, "New cell_attr %r at (%r, %r)\n", cell_attr, rowx, colx)
        if not self.book.xf_list:
            for xfx in xrange(16):
                self.insert_new_BIFF20_xf(cell_attr="\x40\x00\x00", style=xfx < 15)
        xfx = self.insert_new_BIFF20_xf(cell_attr=cell_attr)
        return xfx

    def insert_new_BIFF20_xf(self, cell_attr, style=0):
        DEBUG = 0
        blah = DEBUG or self.verbosity >= 2
        book = self.book
        xfx = len(book.xf_list)
        xf = self.fake_XF_from_BIFF20_cell_attr(cell_attr, style)
        xf.xf_index = xfx
        book.xf_list.append(xf)
        if blah:
            xf.dump(self.logfile, header="=== Faked XF %d ===" % xfx, footer="======")
        if not book.format_map.has_key(xf.format_key):
            if xf.format_key:
                msg = "ERROR *** XF[%d] unknown format key (%d, 0x%04x)\n"
                fprintf(self.logfile, msg,
                        xf.xf_index, xf.format_key, xf.format_key)
            fmt = Format(xf.format_key, FUN, u"General")
            book.format_map[xf.format_key] = fmt
            book.format_list.append(fmt)
        cellty_from_fmtty = {
            FNU: XL_CELL_NUMBER,
            FUN: XL_CELL_NUMBER,
            FGE: XL_CELL_NUMBER,
            FDT: XL_CELL_DATE,
            FTX: XL_CELL_NUMBER, # Yes, a number can be formatted as text.
            }
        fmt = book.format_map[xf.format_key]
        cellty = cellty_from_fmtty[fmt.type]
        self._xf_index_to_xl_type_map[xf.xf_index] = cellty
        self._cell_attr_to_xfx[cell_attr] = xfx
        return xfx

    def fake_XF_from_BIFF20_cell_attr(self, cell_attr, style=0):
        from formatting import XF, XFAlignment, XFBorder, XFBackground, XFProtection
        xf = XF()
        xf.alignment = XFAlignment()
        xf.alignment.indent_level = 0
        xf.alignment.shrink_to_fit = 0
        xf.alignment.text_direction = 0
        xf.border = XFBorder()
        xf.border.diag_up = 0
        xf.border.diag_down = 0
        xf.border.diag_colour_index = 0
        xf.border.diag_line_style = 0 # no line
        xf.background = XFBackground()
        xf.protection = XFProtection()
        (prot_bits, font_and_format, halign_etc) = unpack('<BBB', cell_attr)
        xf.format_key = font_and_format & 0x3F
        xf.font_index = (font_and_format & 0xC0) >> 6
        upkbits(xf.protection, prot_bits, (
            (6, 0x40, 'cell_locked'),
            (7, 0x80, 'formula_hidden'),
            ))
        xf.alignment.hor_align = halign_etc & 0x07
        for mask, side in ((0x08, 'left'), (0x10, 'right'), (0x20, 'top'), (0x40, 'bottom')):
            if halign_etc & mask:
                colour_index, line_style = 8, 1 # black, thin
            else:
                colour_index, line_style = 0, 0 # none, none
            setattr(xf.border, side + '_colour_index', colour_index)
            setattr(xf.border, side + '_line_style', line_style)
        bg = xf.background
        if halign_etc & 0x80:
            bg.fill_pattern = 17
        else:
            bg.fill_pattern = 0
        bg.background_colour_index = 9 # white
        bg.pattern_colour_index = 8 # black
        xf.parent_style_index = (0x0FFF, 0)[style]
        xf.alignment.vert_align = 2 # bottom
        xf.alignment.rotation = 0
        for attr_stem in \
            "format font alignment border background protection".split():
            attr = "_" + attr_stem + "_flag"
            setattr(xf, attr, 1)
        return xf

    def req_fmt_info(self):
        if not self.formatting_info:
            raise XLRDError("Feature requires open_workbook(..., formatting_info=True)")

    ##
    # Determine column display width.
    # <br /> -- New in version 0.6.1
    # <br />
    # @param colx Index of the queried column, range 0 to 255.
    # Note that it is possible to find out the width that will be used to display
    # columns with no cell information e.g. column IV (colx=255).
    # @return The column width that will be used for displaying
    # the given column by Excel, in units of 1/256th of the width of a
    # standard character (the digit zero in the first font).

    def computed_column_width(self, colx):
        self.req_fmt_info()
        if self.biff_version >= 80:
            colinfo = self.colinfo_map.get(colx, None)
            if colinfo is not None:
                return colinfo.width
            if self.standardwidth is not None:
                return self.standardwidth
        elif self.biff_version >= 40:
            if self.gcw[colx]:
                if self.standardwidth is not None:
                    return self.standardwidth
            else:
                colinfo = self.colinfo_map.get(colx, None)
                if colinfo is not None:
                    return colinfo.width
        elif self.biff_version == 30:
            colinfo = self.colinfo_map.get(colx, None)
            if colinfo is not None:
                return colinfo.width
        # All roads lead to Rome and the DEFCOLWIDTH ...
        if self.defcolwidth is not None:
            return self.defcolwidth * 256
        return 8 * 256 # 8 is what Excel puts in a DEFCOLWIDTH record

    def handle_hlink(self, data):
        # DEBUG = 1
        if DEBUG: print >> self.logfile, "\n=== hyperlink ==="
        record_size = len(data)
        h = Hyperlink()
        h.frowx, h.lrowx, h.fcolx, h.lcolx, guid0, dummy, options = unpack('<HHHH16s4si', data[:32])
        assert guid0 == "\xD0\xC9\xEA\x79\xF9\xBA\xCE\x11\x8C\x82\x00\xAA\x00\x4B\xA9\x0B"
        assert dummy == "\x02\x00\x00\x00"
        if DEBUG: print >> self.logfile, "options: %08X" % options
        offset = 32

        def get_nul_terminated_unicode(buf, ofs):
            nb = unpack('<L', buf[ofs:ofs+4])[0] * 2
            ofs += 4
            uc = unicode(buf[ofs:ofs+nb], 'UTF-16le')[:-1]
            ofs += nb
            return uc, ofs

        if options & 0x14: # has a description
            h.desc, offset = get_nul_terminated_unicode(data, offset)
            
        if options & 0x80: # has a target
            h.target, offset = get_nul_terminated_unicode(data, offset)
            
        if (options & 1) and not (options & 0x100): # HasMoniker and not MonikerSavedAsString
            # an OLEMoniker structure
            clsid, = unpack('<16s', data[offset:offset + 16])
            if DEBUG: print >> self.logfile, "clsid=%r" %clsid
            offset += 16
            if clsid == "\xE0\xC9\xEA\x79\xF9\xBA\xCE\x11\x8C\x82\x00\xAA\x00\x4B\xA9\x0B":
                #          E0H C9H EAH 79H F9H BAH CEH 11H 8CH 82H 00H AAH 00H 4BH A9H 0BH
                # URL Moniker
                h.type = u'url'
                nbytes = unpack('<L', data[offset:offset + 4])[0]
                offset += 4
                h.url_or_path = unicode(data[offset:offset + nbytes], 'UTF-16le')
                if DEBUG: print >> self.logfile, "initial url=%r len=%d" % (h.url_or_path, len(h.url_or_path))
                endpos = h.url_or_path.find(u'\x00')
                if DEBUG: print >> self.logfile, "endpos=%d" % endpos
                h.url_or_path = h.url_or_path[:endpos]
                true_nbytes = 2 * (endpos + 1)
                offset += true_nbytes
                extra_nbytes = nbytes - true_nbytes
                extra_data = data[offset:offset + extra_nbytes]
                offset += extra_nbytes
                if DEBUG: print >> self.logfile, "url=%r" % h.url_or_path
                if DEBUG: print >> self.logfile, "extra=%r" % extra_data
                if DEBUG: print >> self.logfile, "nbytes=%d true_nbytes=%d extra_nbytes=%d" % (nbytes, true_nbytes, extra_nbytes)
                assert extra_nbytes in (24, 0)
            elif clsid == "\x03\x03\x00\x00\x00\x00\x00\x00\xC0\x00\x00\x00\x00\x00\x00\x46":
                # file moniker
                h.type = u'local file'
                uplevels, nbytes = unpack("<Hi", data[offset:offset + 6])
                offset += 6
                shortpath = "..\\" * uplevels + data[offset:offset + nbytes - 1] #### BYTES, not unicode
                if DEBUG: print >> self.logfile, "uplevels=%d shortpath=%r" % (uplevels, shortpath)
                offset += nbytes
                offset += 24 # OOo: "unknown byte sequence"
                # above is version 0xDEAD + 20 reserved zero bytes
                sz = unpack('<i', data[offset:offset + 4])[0]
                if DEBUG: print >> self.logfile, "sz=%d" % sz
                offset += 4
                if sz:
                    xl = unpack('<i', data[offset:offset + 4])[0]
                    offset += 4
                    offset += 2 # "unknown byte sequence" MS: 0x0003
                    extended_path = unicode(data[offset:offset + xl], 'UTF-16le') # not zero-terminated
                    offset += xl
                    h.url_or_path = extended_path
                else:
                    h.url_or_path = shortpath
                    #### MS KLUDGE WARNING ####
                    # The "shortpath" is bytes encoded in the **UNKNOWN** creator's "ANSI" encoding.
            else:
                print >> self.logfile, "*** unknown clsid %r" % clsid
        elif options & 0x163 == 0x103: # UNC
            h.type = u'unc'
            h.url_or_path, offset = get_nul_terminated_unicode(data, offset)
        elif options & 0x16B == 8:
            h.type = u'workbook'
        else:
            h.type = u'unknown'
            
        if options & 0x8: # has textmark
            h.textmark, offset = get_nul_terminated_unicode(data, offset)

        assert offset == record_size
        if DEBUG: h.dump(header="... object dump ...")        

        self.hyperlink_list.append(h)
        for rowx in xrange(h.frowx, h.lrowx+1):
            for colx in xrange(h.fcolx, h.lcolx+1):
                self.hyperlink_map[rowx, colx] = h
                
    def handle_quicktip(self, data):
        rcx, frowx, lrowx, fcolx, lcolx = unpack('<5H', data[:10])
        assert rcx == XL_QUICKTIP
        assert self.hyperlink_list
        h = self.hyperlink_list[-1]
        assert (frowx, lrowx, fcolx, lcolx) == (h.frowx, h.lrowx, h.fcolx, h.lcolx)
        assert data[-2:] == '\x00\x00'
        h.quicktip = unicode(data[10:-2], 'utf_16_le')

    def handle_msodrawingetc(self, recid, data_len, data):
        if not OBJ_MSO_DEBUG:
            return
        DEBUG = 1
        if self.biff_version < 80:
            return
        o = MSODrawing()
        pos = 0
        while pos < data_len:
            tmp, fbt, cb = unpack('<HHI', data[pos:pos+8])
            ver = tmp & 0xF
            inst = (tmp >> 4) & 0xFFF
            if ver == 0xF:
                ndb = 0 # container
            else:
                ndb = cb
            if DEBUG:
                hex_char_dump(data, pos, ndb + 8, base=0, fout=self.logfile)
                fprintf(self.logfile,
                    "fbt:0x%04X  inst:%d  ver:0x%X  cb:%d (0x%04X)\n",
                    fbt, inst, ver, cb, cb)
            if fbt == 0xF010: # Client Anchor
                assert ndb == 18
                (o.anchor_unk,
                o.anchor_colx_lo, o.anchor_rowx_lo,
                o.anchor_colx_hi, o.anchor_rowx_hi) = unpack('<Hiiii', data[pos+8:pos+8+ndb])
            elif fbt == 0xF011: # Client Data
                # must be followed by an OBJ record
                assert cb == 0
                assert pos + 8 == data_len
            else:
                pass
            pos += ndb + 8
        else:
            # didn't break out of while loop
            assert pos == data_len
        if DEBUG:
            o.dump(self.logfile, header="=== MSODrawing ===", footer= " ")


    def handle_obj(self, data):
        if self.biff_version < 80:
            return
        o = MSObj()
        data_len = len(data)
        pos = 0
        if OBJ_MSO_DEBUG:
            fprintf(self.logfile, "... OBJ record ...\n")
        while pos < data_len:
            ft, cb = unpack('<HH', data[pos:pos+4])
            if OBJ_MSO_DEBUG:
                hex_char_dump(data, pos, cb, base=0, fout=self.logfile)
            if ft == 0x15: # ftCmo ... s/b first
                assert pos == 0
                o.type, o.id, option_flags = unpack('<HHH', data[pos+4:pos+10])
                upkbits(o, option_flags, (
                    ( 0, 0x0001, 'locked'),
                    ( 4, 0x0010, 'printable'),
                    ( 8, 0x0100, 'autofilter'), # not documented in Excel 97 dev kit
                    ( 9, 0x0200, 'scrollbar_flag'), # not documented in Excel 97 dev kit
                    (13, 0x2000, 'autofill'),
                    (14, 0x4000, 'autoline'),
                    ))
            elif ft == 0x00:
                assert cb == 0
                assert pos + 4 == data_len
            elif ft == 0x0C: # Scrollbar
                values = unpack('<5H', data[pos+8:pos+18])
                for value, tag in zip(values, ('value', 'min', 'max', 'inc', 'page')):
                    setattr(o, 'scrollbar_' + tag, value)
            elif ft == 0x0D: # "Notes structure" [used for cell comments]
                ############## not documented in Excel 97 dev kit
                if OBJ_MSO_DEBUG: fprintf(self.logfile, "*** OBJ record has ft==0x0D 'notes' structure\n")
            elif ft == 0x13: # list box data
                if o.autofilter: # non standard exit. NOT documented
                    break
            else:
                pass
            pos += cb + 4
        else:
            # didn't break out of while loop
            assert pos == data_len
        if OBJ_MSO_DEBUG:
            o.dump(self.logfile, header="=== MSOBj ===", footer= " ")
        return o

    def handle_note(self, data, txos):
        if OBJ_MSO_DEBUG:
            fprintf(self.logfile, '... NOTE record ...\n')
            hex_char_dump(data, 0, len(data), base=0, fout=self.logfile)
        o = Note()
        data_len = len(data)
        if self.biff_version < 80:
            o.rowx, o.colx, expected_bytes = unpack('<HHH', data[:6])
            nb = len(data) - 6
            assert nb <= expected_bytes
            pieces = [data[6:]]
            expected_bytes -= nb
            while expected_bytes > 0:
                rc2, data2_len, data2 = self.book.get_record_parts()
                assert rc2 == XL_NOTE
                dummy_rowx, nb = unpack('<H2xH', data2[:6])
                assert dummy_rowx == 0xFFFF
                assert nb == data2_len - 6
                pieces.append(data2[6:])
                expected_bytes -= nb
            assert expected_bytes == 0
            enc = self.book.encoding or self.book.derive_encoding()
            o.text = unicode(''.join(pieces), enc)
            o.rich_text_runlist = [(0, 0)]
            o.show = 0
            o.row_hidden = 0
            o.col_hidden = 0
            o.author = u''
            o._object_id = None
            self.cell_note_map[o.rowx, o.colx] = o        
            return
        # Excel 8.0+
        o.rowx, o.colx, option_flags, o._object_id = unpack('<4H', data[:8])
        o.show = (option_flags >> 1) & 1
        o.row_hidden = (option_flags >> 7) & 1
        o.col_hidden = (option_flags >> 8) & 1
        # XL97 dev kit book says NULL [sic] bytes padding between string count and string data
        # to ensure that string is word-aligned. Appears to be nonsense.
        o.author, endpos = unpack_unicode_update_pos(data, 8, lenlen=2)
        # There is a random/undefined byte after the author string (not counted in the
        # string length).
        # Issue 4 on github: Google Spreadsheet doesn't write the undefined byte.
        assert (data_len - endpos) in (0, 1)
        if OBJ_MSO_DEBUG:
            o.dump(self.logfile, header="=== Note ===", footer= " ")
        txo = txos.get(o._object_id)
        if txo:
            o.text = txo.text
            o.rich_text_runlist = txo.rich_text_runlist
            self.cell_note_map[o.rowx, o.colx] = o        

    def handle_txo(self, data):
        if self.biff_version < 80:
            return
        o = MSTxo()
        data_len = len(data)
        fmt = '<HH6sHHH'
        fmtsize = calcsize(fmt)
        option_flags, o.rot, controlInfo, cchText, cbRuns, o.ifntEmpty = unpack(fmt, data[:fmtsize])
        o.fmla = data[fmtsize:]
        upkbits(o, option_flags, (
            ( 3, 0x000E, 'horz_align'),
            ( 6, 0x0070, 'vert_align'),
            ( 9, 0x0200, 'lock_text'),
            (14, 0x4000, 'just_last'),
            (15, 0x8000, 'secret_edit'),
            ))
        totchars = 0
        o.text = u''
        while totchars < cchText:
            rc2, data2_len, data2 = self.book.get_record_parts()
            assert rc2 == XL_CONTINUE
            if OBJ_MSO_DEBUG:
                hex_char_dump(data2, 0, data2_len, base=0, fout=self.logfile)
            nb = ord(data2[0]) # 0 means latin1, 1 means utf_16_le
            nchars = data2_len - 1
            if nb:
                assert nchars % 2 == 0
                nchars /= 2
            utext, endpos = unpack_unicode_update_pos(data2, 0, known_len=nchars)
            assert endpos == data2_len
            o.text += utext
            totchars += nchars
        o.rich_text_runlist = []
        totruns = 0
        while totruns < cbRuns: # counts of BYTES, not runs
            rc3, data3_len, data3 = self.book.get_record_parts()
            # print totruns, cbRuns, rc3, data3_len, repr(data3)
            assert rc3 == XL_CONTINUE
            assert data3_len % 8 == 0
            for pos in xrange(0, data3_len, 8):
                run = unpack('<HH4x', data3[pos:pos+8])
                o.rich_text_runlist.append(run)
                totruns += 8
        # remove trailing entries that point to the end of the string
        while o.rich_text_runlist and o.rich_text_runlist[-1][0] == cchText:
            del o.rich_text_runlist[-1]
        if OBJ_MSO_DEBUG:
            o.dump(self.logfile, header="=== MSTxo ===", footer= " ")
            print >> self.logfile, o.rich_text_runlist
        return o

    def handle_feat11(self, data):
        if not OBJ_MSO_DEBUG:
            return
        # rt: Record type; this matches the BIFF rt in the first two bytes of the record; =0872h
        # grbitFrt: FRT cell reference flag (see table below for details)
        # Ref0: Range reference to a worksheet cell region if grbitFrt=1 (bitFrtRef). Otherwise blank.
        # isf: Shared feature type index =5 for Table
        # fHdr: =0 since this is for feat not feat header
        # reserved0: Reserved for future use =0 for Table
        # cref: Count of ref ranges this feature is on
        # cbFeatData: Count of byte for the current feature data.
        # reserved1: =0 currently not used
        # Ref1: Repeat of Ref0. UNDOCUMENTED
        rt, grbitFrt, Ref0, isf, fHdr, reserved0, cref, cbFeatData, reserved1, Ref1 = unpack('<HH8sHBiHiH8s', data[0:35])
        assert reserved0 == 0
        assert reserved1 == 0
        assert isf == 5
        assert rt == 0x872
        assert fHdr == 0
        assert Ref1 == Ref0
        print >> self.logfile, "FEAT11: grbitFrt=%d  Ref0=%r cref=%d cbFeatData=%d" % (grbitFrt, Ref0, cref, cbFeatData)
        # lt: Table data source type:
        #   =0 for Excel Worksheet Table =1 for read-write SharePoint linked List
        #   =2 for XML mapper Table =3 for Query Table
        # idList: The ID of the Table (unique per worksheet)
        # crwHeader: How many header/title rows the Table has at the top
        # crwTotals: How many total rows the Table has at the bottom
        # idFieldNext: Next id to try when assigning a unique id to a new field
        # cbFSData: The size of the Fixed Data portion of the Table data structure.
        # rupBuild: the rupBuild that generated the record
        # unusedShort: UNUSED short that can be used later. The value is reserved during round-tripping.
        # listFlags: Collection of bit flags: (see listFlags' bit setting table below for detail.)
        # lPosStmCache: Table data stream position of cached data
        # cbStmCache: Count of bytes of cached data
        # cchStmCache: Count of characters of uncompressed cached data in the stream
        # lem: Table edit mode (see List (Table) Editing Mode (lem) setting table below for details.)
        # rgbHashParam: Hash value for SharePoint Table
        # cchName: Count of characters in the Table name string rgbName
        (lt, idList, crwHeader, crwTotals, idFieldNext, cbFSData,
        rupBuild, unusedShort, listFlags, lPosStmCache, cbStmCache,
        cchStmCache, lem, rgbHashParam, cchName) = unpack('<iiiiiiHHiiiii16sH', data[35:35+66])
        print >> self.logfile, "lt=%d  idList=%d crwHeader=%d  crwTotals=%d  idFieldNext=%d cbFSData=%d\n"\
            "rupBuild=%d  unusedShort=%d listFlags=%04X  lPosStmCache=%d  cbStmCache=%d\n"\
            "cchStmCache=%d  lem=%d  rgbHashParam=%r  cchName=%d" % (
            lt, idList, crwHeader, crwTotals, idFieldNext, cbFSData,
            rupBuild, unusedShort,listFlags, lPosStmCache, cbStmCache,
            cchStmCache, lem, rgbHashParam, cchName)

class MSODrawing(BaseObject):
    pass

class MSObj(BaseObject):
    pass

class MSTxo(BaseObject):
    pass

##    
# <p> Represents a user "comment" or "note".
# Note objects are accessible through Sheet.{@link #Sheet.cell_note_map}.
# <br />-- New in version 0.7.2  
# </p>
class Note(BaseObject):
    ##
    # Author of note
    author = u''
    ##
    # True if the containing column is hidden
    col_hidden = 0 
    ##
    # Column index
    colx = 0
    ##
    # List of (offset_in_string, font_index) tuples.
    # Unlike Sheet.{@link #Sheet.rich_text_runlist_map}, the first offset should always be 0.
    rich_text_runlist = None
    ##
    # True if the containing row is hidden
    row_hidden = 0
    ##
    # Row index
    rowx = 0
    ##
    # True if note is always shown
    show = 0
    ##
    # Text of the note
    text = u''

##
# <p>Contains the attributes of a hyperlink.
# Hyperlink objects are accessible through Sheet.{@link #Sheet.hyperlink_list}
# and Sheet.{@link #Sheet.hyperlink_map}.
# <br />-- New in version 0.7.2
# </p>   
class Hyperlink(BaseObject):
    ##
    # Index of first row
    frowx = None
    ##
    # Index of last row
    lrowx = None
    ##
    # Index of first column
    fcolx = None
    ##
    # Index of last column
    lcolx = None
    ##
    # Type of hyperlink. Unicode string, one of 'url', 'unc',
    # 'local file', 'workbook', 'unknown'
    type = None
    ##
    # The URL or file-path, depending in the type. Unicode string, except 
    # in the rare case of a local but non-existent file with non-ASCII
    # characters in the name, in which case only the "8.3" filename is available,
    # as a bytes (3.x) or str (2.x) string, <i>with unknown encoding.</i>
    url_or_path = None
    ##
    # Description ... this is displayed in the cell,
    # and should be identical to the cell value. Unicode string, or None. It seems
    # impossible NOT to have a description created by the Excel UI.
    desc = None
    ##
    # Target frame. Unicode string. Note: I have not seen a case of this.
    # It seems impossible to create one in the Excel UI.
    target = None
    ##
    # "Textmark": the piece after the "#" in 
    # "http://docs.python.org/library#struct_module", or the Sheet1!A1:Z99
    # part when type is "workbook".
    textmark = None
    ##
    # The text of the "quick tip" displayed when the cursor
    # hovers over the hyperlink.
    quicktip = None

# === helpers ===

def unpack_RK(rk_str):
    flags = ord(rk_str[0])
    if flags & 2:
        # There's a SIGNED 30-bit integer in there!
        i,  = unpack('<i', rk_str)
        i >>= 2 # div by 4 to drop the 2 flag bits
        if flags & 1:
            return i / 100.0
        return float(i)
    else:
        # It's the most significant 30 bits of an IEEE 754 64-bit FP number
        d, = unpack('<d', '\0\0\0\0' + chr(flags & 252) + rk_str[1:4])
        if flags & 1:
            return d / 100.0
        return d

##### =============== Cell ======================================== #####

cellty_from_fmtty = {
    FNU: XL_CELL_NUMBER,
    FUN: XL_CELL_NUMBER,
    FGE: XL_CELL_NUMBER,
    FDT: XL_CELL_DATE,
    FTX: XL_CELL_NUMBER, # Yes, a number can be formatted as text.
    }

ctype_text = {
    XL_CELL_EMPTY: 'empty',
    XL_CELL_TEXT: 'text',
    XL_CELL_NUMBER: 'number',
    XL_CELL_DATE: 'xldate',
    XL_CELL_BOOLEAN: 'bool',
    XL_CELL_ERROR: 'error',
    XL_CELL_BLANK: 'blank',
    }

##
# <p>Contains the data for one cell.</p>
#
# <p>WARNING: You don't call this class yourself. You access Cell objects
# via methods of the {@link #Sheet} object(s) that you found in the {@link #Book} object that
# was returned when you called xlrd.open_workbook("myfile.xls").</p>
# <p> Cell objects have three attributes: <i>ctype</i> is an int, <i>value</i>
# (which depends on <i>ctype</i>) and <i>xf_index</i>.
# If "formatting_info" is not enabled when the workbook is opened, xf_index will be None.
# The following table describes the types of cells and how their values
# are represented in Python.</p>
#
# <table border="1" cellpadding="7">
# <tr>
# <th>Type symbol</th>
# <th>Type number</th>
# <th>Python value</th>
# </tr>
# <tr>
# <td>XL_CELL_EMPTY</td>
# <td align="center">0</td>
# <td>empty string u''</td>
# </tr>
# <tr>
# <td>XL_CELL_TEXT</td>
# <td align="center">1</td>
# <td>a Unicode string</td>
# </tr>
# <tr>
# <td>XL_CELL_NUMBER</td>
# <td align="center">2</td>
# <td>float</td>
# </tr>
# <tr>
# <td>XL_CELL_DATE</td>
# <td align="center">3</td>
# <td>float</td>
# </tr>
# <tr>
# <td>XL_CELL_BOOLEAN</td>
# <td align="center">4</td>
# <td>int; 1 means TRUE, 0 means FALSE</td>
# </tr>
# <tr>
# <td>XL_CELL_ERROR</td>
# <td align="center">5</td>
# <td>int representing internal Excel codes; for a text representation,
# refer to the supplied dictionary error_text_from_code</td>
# </tr>
# <tr>
# <td>XL_CELL_BLANK</td>
# <td align="center">6</td>
# <td>empty string u''. Note: this type will appear only when
# open_workbook(..., formatting_info=True) is used.</td>
# </tr>
# </table>
#<p></p>

class Cell(BaseObject):

    __slots__ = ['ctype', 'value', 'xf_index']

    def __init__(self, ctype, value, xf_index=None):
        self.ctype = ctype
        self.value = value
        self.xf_index = xf_index

    def __repr__(self):
        if self.xf_index is None:
            return "%s:%r" % (ctype_text[self.ctype], self.value)
        else:
            return "%s:%r (XF:%r)" % (ctype_text[self.ctype], self.value, self.xf_index)

##
# There is one and only one instance of an empty cell -- it's a singleton. This is it.
# You may use a test like "acell is empty_cell".
empty_cell = Cell(XL_CELL_EMPTY, '')

##### =============== Colinfo and Rowinfo ============================== #####

##
# Width and default formatting information that applies to one or
# more columns in a sheet. Derived from COLINFO records.
#
# <p> Here is the default hierarchy for width, according to the OOo docs:
#
# <br />"""In BIFF3, if a COLINFO record is missing for a column,
# the width specified in the record DEFCOLWIDTH is used instead.
#
# <br />In BIFF4-BIFF7, the width set in this [COLINFO] record is only used,
# if the corresponding bit for this column is cleared in the GCW
# record, otherwise the column width set in the DEFCOLWIDTH record
# is used (the STANDARDWIDTH record is always ignored in this case [see footnote!]).
#
# <br />In BIFF8, if a COLINFO record is missing for a column,
# the width specified in the record STANDARDWIDTH is used.
# If this [STANDARDWIDTH] record is also missing,
# the column width of the record DEFCOLWIDTH is used instead."""
# <br />
#
# Footnote:  The docs on the GCW record say this:
# """<br />
# If a bit is set, the corresponding column uses the width set in the STANDARDWIDTH
# record. If a bit is cleared, the corresponding column uses the width set in the
# COLINFO record for this column.
# <br />If a bit is set, and the worksheet does not contain the STANDARDWIDTH record, or if
# the bit is cleared, and the worksheet does not contain the COLINFO record, the DEFCOLWIDTH
# record of the worksheet will be used instead.
# <br />"""<br />
# At the moment (2007-01-17) xlrd is going with the GCW version of the story.
# Reference to the source may be useful: see the computed_column_width(colx) method
# of the Sheet class.
# <br />-- New in version 0.6.1
# </p>

class Colinfo(BaseObject):
    ##
    # Width of the column in 1/256 of the width of the zero character,
    # using default font (first FONT record in the file).
    width = 0
    ##
    # XF index to be used for formatting empty cells.
    xf_index = -1
    ##
    # 1 = column is hidden
    hidden = 0
    ##
    # Value of a 1-bit flag whose purpose is unknown
    # but is often seen set to 1
    bit1_flag = 0
    ##
    # Outline level of the column, in range(7).
    # (0 = no outline)
    outline_level = 0
    ##
    # 1 = column is collapsed
    collapsed = 0

_USE_SLOTS = 1

##
# <p>Height and default formatting information that applies to a row in a sheet.
# Derived from ROW records.
# <br /> -- New in version 0.6.1</p>
#
# <p><b>height</b>: Height of the row, in twips. One twip == 1/20 of a point.</p>
#
# <p><b>has_default_height</b>: 0 = Row has custom height; 1 = Row has default height.</p>
#
# <p><b>outline_level</b>: Outline level of the row (0 to 7) </p>
#
# <p><b>outline_group_starts_ends</b>: 1 = Outline group starts or ends here (depending on where the
# outline buttons are located, see WSBOOL record [TODO ??]),
# <i>and</i> is collapsed </p>
#
# <p><b>hidden</b>: 1 = Row is hidden (manually, or by a filter or outline group) </p>
#
# <p><b>height_mismatch</b>: 1 = Row height and default font height do not match </p>
#
# <p><b>has_default_xf_index</b>: 1 = the xf_index attribute is usable; 0 = ignore it </p>
#
# <p><b>xf_index</b>: Index to default XF record for empty cells in this row.
# Don't use this if has_default_xf_index == 0. </p>
#
# <p><b>additional_space_above</b>: This flag is set, if the upper border of at least one cell in this row
# or if the lower border of at least one cell in the row above is
# formatted with a thick line style. Thin and medium line styles are not
# taken into account. </p>
#
# <p><b>additional_space_below</b>: This flag is set, if the lower border of at least one cell in this row
# or if the upper border of at least one cell in the row below is
# formatted with a medium or thick line style. Thin line styles are not
# taken into account. </p>

class Rowinfo(BaseObject):

    if _USE_SLOTS:
        __slots__ = (
            "height",
            "has_default_height",
            "outline_level",
            "outline_group_starts_ends",
            "hidden",
            "height_mismatch",
            "has_default_xf_index",
            "xf_index",
            "additional_space_above",
            "additional_space_below",
            )

    def __init__(self):
        self.height = None
        self.has_default_height = None
        self.outline_level = None
        self.outline_group_starts_ends = None
        self.hidden = None
        self.height_mismatch = None
        self.has_default_xf_index = None
        self.xf_index = None
        self.additional_space_above = None
        self.additional_space_below = None

    def __getstate__(self):
        return (
            self.height,
            self.has_default_height,
            self.outline_level,
            self.outline_group_starts_ends,
            self.hidden,
            self.height_mismatch,
            self.has_default_xf_index,
            self.xf_index,
            self.additional_space_above,
            self.additional_space_below,
            )

    def __setstate__(self, state):
        (
            self.height,
            self.has_default_height,
            self.outline_level,
            self.outline_group_starts_ends,
            self.hidden,
            self.height_mismatch,
            self.has_default_xf_index,
            self.xf_index,
            self.additional_space_above,
            self.additional_space_below,
            ) = state
