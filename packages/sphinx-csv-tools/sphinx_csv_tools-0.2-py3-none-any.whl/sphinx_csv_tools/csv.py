# -*- coding: utf-8; -*-

import ast
import re
from copy import deepcopy

from docutils.parsers.rst.directives.tables import CSVTable
from docutils.utils import SystemMessagePropagation



def non_negative_int(argument):
    """
    Converts the argument into an integer.
    Raises ValueError for negative or non-integer values.
    
    :param argument: Contains the value that should be checked for being a non negative integer
    :type argument: mixed
    :return: integerized value if int() was successful
    :rtype: int
    """

    value = int(argument)
    if value >= 0:
        return value
    else:
        raise ValueError('negative value defined; must be non-negative')

def make_list (argument):
    """
    Makes a list out of argument. 
    Will always return a list, even if only one element is given
    
    :param argument: String with list-elements seperated by ,
    :type argument: str
    :return: List of elements.
    :rtype: list
    """

    if ',' in argument:
        entries = argument.split(',')
    else:
        entries = argument.split()
    return entries


class CSVToolsDirective(CSVTable):
    """ The CSV Filter directive renders csv defined in config
        and filter rows that contains a specified regex pattern
    """
    CSVTable.option_spec['include'] = ast.literal_eval
    CSVTable.option_spec['exclude'] = ast.literal_eval
    CSVTable.option_spec['included_cols'] = make_list
    CSVTable.option_spec['unique'] = make_list
    CSVTable.option_spec['summarize'] = ast.literal_eval
    CSVTable.option_spec['format'] = ast.literal_eval
    CSVTable.option_spec['header-beautify'] = make_list
    CSVTable.option_spec['order'] = make_list
    CSVTable.option_spec['limit'] = make_list
    header_rows = list()


    def get_header_rows(self,rows):
        """
        Extracts the header out of the rows and creates the dictionary for the name to index lookup.
        The headers will be saved in self.header_rows so they can be prepended at the end

        :param rows: Rows of the table
        :type rows: list
        :return: Nothing is returned
        :rtype: None
        """

        header_rows_count = self.options.get('header-rows', 0)
        # Always include header rows, if any
        header_rows = rows[:header_rows_count]

        headers = dict()
        
        for row in header_rows:
            col_num = 0
            for col in row:
                headers[col[3][0]] = col_num
                col_num += 1
        
        if len(headers) > 0:
            self.header_map = headers
        else:
            #Set header-map to false if no headers are present to prevent lookup
            self.header_map = False
    

    def hidx (self,header_name):
        """
        Looks up the name of the header in the header-map created by get_header_rows() and returns the index

        :param header_name: Name of the header
        :type header_name: str
        :return: Index of the header
        :rtype: int
        """

        if isinstance(header_name,int):
            return header_name
        else:
            if self.header_map:
                if header_name in self.header_map.keys():
                    return self.header_map[header_name]
                else:
                    print(f"Can't lookup header {header_name}. It does not exist.")
                    return header_name
            else:
                #self.errorqueue.append(SystemMessagePropagation(self.state_machine.reporter.error(
                #    f"You can't reference cols by name without having headers defined"
                #    )))
                print("You can't reference cols by name without having headers defined")
                return header_name

    
    def parse_csv_data_into_rows(self, csv_data, dialect, source):
        """
        Monkey-patch for the function that is getting called for csv-data ito the rows
        See `https://docs.python.org/3/library/csv.html#csv.reader` for more information

        :param csv_data: CSV-data for csv-reader
        :type csv_data: object
        :param dialect: Dialect to use
        :type dialect: str
        :param source: Source
        :type source: object
        :return: Tuple of table_rows and max_cols
        :rtype: tuple
        """

        rows, max_cols = super(
            CSVToolsDirective, self
        ).parse_csv_data_into_rows(csv_data, dialect, source)
        include_filters = list()
        exclude_filters = list()

        ######### Prework #########
        #Empty out variables as they carry over between tables
        self.header_rows = list()
        self.header_map = False
        self.get_header_rows(rows)
        
        #Add header-rows to table-rows 
        header_rows = self.options.get('header-rows', 0)
        self.header_rows.extend(rows[:header_rows])

        ######### Include #########
        #Process include-filters
        if 'include' in self.options:
            for k, v in self.options['include'].items():
                if isinstance(v,list):
                    for vl in v:
                        include_filters.append({
                            k: re.compile(vl)
                        })
                elif isinstance(v,str):
                    include_filters.append({
                        k: re.compile(v)
                    })
                else:
                    error = self.state_machine.reporter.error(
                    f'Value of include index {k} is not string or list of strings'
                    )
                    raise SystemMessagePropagation(error)
        
        ######### Exclude #########
        #Process exclude-filters
        if 'exclude' in self.options:
            for k, v in self.options['exclude'].items():
                if isinstance(v,list):
                    for vl in v:
                        exclude_filters.append({
                            k: re.compile(vl)
                        })
                elif isinstance(v,str):
                    exclude_filters.append({
                        k: re.compile(v)
                    })
                else:
                    error = self.state_machine.reporter.error(
                    f'Value of exclude index {k} is not string or list of strings'
                    )
                    raise SystemMessagePropagation(error)
        
        
        ######### Apply the filters #########
        rows = self._apply_filters(rows, max_cols, include_filters, exclude_filters)
        
        
        ######### Unique #########
        if 'unique' in self.options:
            rows, max_cols = self._unique(rows)

        ######### Summarize cols #########
        if 'summarize' in self.options:
            rows += self._summarize_cols(rows, max_cols)

        ######### Format numbers #########
        if 'format' in self.options:
            rows = self._format(rows)
        
        ######### Process included cols #########
        if 'included_cols' in self.options:
            #self.options['included_cols'] = self.non_negative_int_list
            rows, max_cols = self._process_included_cols(
                rows, self.options['included_cols']
            )
        
        ######### Beautify headers #########
        if 'header-beautify' in self.options:
            self._header_beautify(rows)
        
        ######### Order the rows #########
        if 'order' in self.options:
            rows = self._order(rows)
        
        ######### Limit the rows #########
        if 'limit' in self.options:
            rows = self._limit(rows)

        
        ######### Stitch together and return #########
        table_rows = self.header_rows + rows
        return table_rows, max_cols

    
    def _apply_filters(self, rows, max_cols, include_filters, exclude_filters):
        """
        Apply the include and exclude filters
        Leftover from the modified `https://github.com/Nefti-sama/sphinx_csv_filter-jm` (original `https://github.com/crate/sphinx_csv_filter`)

        :param rows: Rows of the table
        :type rows: list
        :param max_cols: Max number of columns
        :type max_cols: int
        :param include_filters: List of compiled regexes for include-filtering the rows
        :type include_filters: list
        :param exclude_filters: List of compiled regexes for exclude-filtering the rows
        :type exclude_filters: list
        :return: Rows that matched the include and did not match the exclude filter
        :rtype: list
        """
        result = []

        header_rows = self.options.get('header-rows', 0)
        # Always include header rows, if any
        #result.extend(rows[:header_rows])
        

        for row in rows[header_rows:]:
            # We generally include a row, ...
            include = True
            if len(include_filters) > 0:
                # ... unless include filters are defined, then we generally
                # exclude them, ...
                include = False
                for inc_filters in include_filters:
                    for col_idx, pattern in inc_filters.items():
                        # cell data value is located at hardcoded index pos. 3
                        # data type is always a string literal
                        if max_cols - 1 >= self.hidx(col_idx):
                            if len(row[self.hidx(col_idx)][3]) > 0 and pattern.search(row[self.hidx(col_idx)][3][0]):
                                # ... unless at least one of the defined filters
                                # matches its cell ...
                                include = True
                                break
                       
            # ... unless exclude filters are defined (as well) ...
            if include and len(exclude_filters) > 0:
                for exc_filters in exclude_filters:
                    for col_idx, pattern in exc_filters.items():
                        # cell data value is located at hardcoded index pos. 3
                        # data type is always a string literal
                        if max_cols - 1 >= self.hidx(col_idx):
                            if len(row[self.hidx(col_idx)][3]) > 0 and pattern.search(row[self.hidx(col_idx)][3][0]):
                                # ... then we exclude a row if any of the defined
                                # exclude filters matches its cell.
                                include = False
                                break
                        
            
            if include:
                result.append(row)

        return result


    def _process_included_cols(self, rows, included_cols):
        """
        Returns only the columns that shall be included in the resulting table

        :param rows: Rows of the table
        :type rows: list
        :param included_cols: List of columns
        :type included_cols: list
        :return: Tuple of table_rows and max_cols
        :rtype: tuple
        """

        prepared_rows = []
        included_cols_list = []
        for icol in included_cols:
            included_cols_list.append(self.hidx(icol))
        for row in rows:
            try:
                idx_row = [row[i] for i in included_cols_list]
                prepared_rows.append(idx_row)
            except IndexError:
                error = self.state_machine.reporter.error(
                    'One or more indexes of included_cols are not valid. '
                    'The CSV data does not contain that many columns.')
                raise SystemMessagePropagation(error)
        
        #Do the same for headers
        header_rows = list()
        for header_row in self.header_rows:
            idx_row = [header_row[i] for i in included_cols_list]
            header_rows.append(idx_row)
        
        #Rewrite the header
        self.header_rows = header_rows

        return prepared_rows, len(included_cols_list)
    
    
    def _unique(self,rows):
        """
        "Uniques" the rows and calculates the count of every unique row
        Will completely rebuild the table leaving only 2 columns behind
        (Unique names and the count)

        :param rows: Rows of the table
        :type rows: list
        :return: Tuple of table_rows and max_cols (2)
        :rtype: tuple
        """

        ucol = self.hidx(self.options['unique'][0])
        #print(ucol)
        new_rows = list()
        val_only = dict()

        #Make unique dict with only the values from unique-col and their counts
        for row in rows:
            row_val = row[ucol][3][0]
            if row_val in val_only.keys():
                val_only[row_val] += 1
            else:
                val_only[row_val] = 1
        
        header_rows = self.options.get('header-rows', 0)
        
        #We need to copy a row as template for the rest
        tmp_cell = deepcopy(rows[0][0])
        trow = [deepcopy(tmp_cell),deepcopy(tmp_cell)]

        #Generate new header if there was one
        if header_rows > 0:
            new_header_row = deepcopy(trow)
            
            #If for unique there was passed an integer, we need to reverse the header_mapping process to get the header name
            if isinstance(self.options['unique'][0],int):
                new_header_row[0][3][0] = self.get_key_from_value(self.header_map,self.options['unique'][0])
                new_header_row[1][3][0] = "Count"

            else:
                new_header_row[0][3][0] = self.options['unique'][0]
                new_header_row[1][3][0] = "Count"
            
            self.header_rows = [new_header_row]
                
        #Build the new rows
        new_rows = list()
        for k,v in val_only.items():
            new_row = deepcopy(trow)
            new_row[0][3][0] = k
            new_row[1][3][0] = str(v)
            new_rows.append(new_row)

        #Return new_rows with col-length of 2
        return new_rows, 2
        

    def _summarize_cols(self,rows,max_cols):
        """
        Summarizes certain columns given via the summarize option

        :param rows: Rows of the table
        :type rows: list
        :param max_cols: Max number of columns
        :type max_cols: int
        :return: One row containing the summaries
        :rtype: list
        """

        col_sum = dict()

        for k,v in self.options['summarize'].items():
            col_sum[self.hidx(k)] = v


        #We need to copy a cell as template for the rest
        tmp_cell = deepcopy(rows[0][0])
        tmp_cell[3][0] = ""

        col_count = max_cols
        
        sum_row = list()
        for i in range(0,col_count):
            sum_row.append(deepcopy(tmp_cell))
            if i in col_sum.keys():
                cur_sum = 0
                for row in rows:
                    #As cells are mostly strings, a typecast into float or int is necessary for doing math
                    if col_sum[i] == 'int': 
                        try:
                            cur_sum += int(row[i][3][0])
                        except:
                            pass
                    
                    elif col_sum[i] == 'float': 
                        try:
                            cur_sum += float(row[i][3][0])
                        except:
                            pass
                
                sum_row[i][3][0] = str(cur_sum)

        return [sum_row]


    def _format(self,rows):
        """
        Alters given columns (via format option) with the format() function

        :param rows: Rows of the table
        :type rows: list
        :return: Formatted rows
        :rtype: list
        """

        new_rows = list()
        for row in rows:
            for col,fstring in self.options['format'].items():
                try:
                    row[self.hidx(col)][3][0] = fstring.format(row[self.hidx(col)][3][0])
                except ValueError:
                    try:
                        row[self.hidx(col)][3][0] = fstring.format(float(row[self.hidx(col)][3][0]))
                    except:
                        pass
            
            new_rows.append(row)
        
        return new_rows


    def _header_beautify(self,rows):
        """
        Beautifies (replaces) the header

        :param rows: Rows of the table
        :type rows: list
        :return: None
        :rtype: None
        """

        #We need to copy a cell as template for the rest
        tmp_cell = deepcopy(rows[0][0])
        tmp_cell[3][0] = ""

        self.header_rows = list()
        header_row = list()
        for header in self.options['header-beautify']:
            cur_cell = deepcopy(tmp_cell)
            cur_cell[3][0] = header
            header_row.append(cur_cell)
        
        self.header_rows = [header_row]


    def _order(self,rows):
        """
        Orders the rows ASC or DESC by a given columns (via option)

        :param rows: Rows of the table
        :type rows: list
        :return: Ordered rows
        :rtype: list
        """

        order_col = self.hidx(self.options['order'][0])
        
        kvpair = dict()
        cur_iter = 0
        for row in rows:
            kvpair[cur_iter] = row[order_col][3][0]
            cur_iter += 1
        
        #Strip off the last line (sum line) if a summarization was done
        if 'summarize' in self.options:
            sum_row = kvpair.popitem()

        #order the kvpair using the value (col content) ASC or DESC
        if len(self.options['order']) > 1 and self.options['order'][1].upper() == "DESC":
            new_order = {k: v for k, v in sorted(kvpair.items(), reverse=True, key=lambda item: item[1])}
        else:
            new_order = {k: v for k, v in sorted(kvpair.items(), key=lambda item: item[1])}
        
        new_rows = list()

        for k in new_order.keys():
            new_rows.append(rows[k])

        #append the sum-line again
        if 'summarize' in self.options:
            new_rows.append(rows[sum_row[0]])
        
        return new_rows
    
    
    def _limit(self,rows):
        """
        Limits the entries
        option allows for "LIMIT 3" or "LIMIT 1,3", etc.

        :param rows: Rows of the table
        :type rows: list
        :return: Limited rows
        :rtype: list
        """
        new_rows = []
        #Only one limit given, starting with 0
        if len(self.options['limit']) == 1:
            limit_start = 0
            limit_end = int(self.options['limit'][0])
        #Start and end limit given
        elif len(self.options['limit']) > 1:
            limit_start = int(self.options['limit'][0])
            limit_end = limit_start + int(self.options['limit'][1])
        #Nothing given for some strange reason, default to displaying all
        else:
            limit_start = 0
            limit_end = len(rows) + 1
        
        #Iterate through rowns and apply the limit
        i = 0
        for row in rows:
            if i >= limit_start and i < limit_end:
                new_rows.append(row)
            elif i > limit_end:
                #Save CPU by ending after the end-limit was reached
                break
            
            i += 1
        
        return new_rows
    

    def get_key_from_value(self,d,val):
        """
        Returns the key for a value
        If mutliple values match the first one is returned

        :param rows: Dictionary to search
        :type rows: dict
        :param val: Value to look for
        :type val: str
        :return: Key that represents the value. None if no key was found
        :rtype: str
        """

        keys = [k for k, v in d.items() if v == val]
        if keys:
            return keys[0]
        return None
    

    def non_negative_int_list(self,argument):
        """
        Converts a space- or comma-separated list of values into a Python list
        of integers.
        Raises ValueError for negative integer values.

        :param argument: String with list-elements seperated by ,
        :type argument: str
        :return: List of elements.
        :rtype: list
        """

        if ',' in argument:
            entries = argument.split(',')
        else:
            entries = argument.split()
        return [non_negative_int(self.hidx(entry)) for entry in entries]


#def setup(sphinx):
#    sphinx.add_directive('csv-tools', CSVToolsDirective)
