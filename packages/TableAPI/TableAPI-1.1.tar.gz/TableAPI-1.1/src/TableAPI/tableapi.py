class InvalidArgSizeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidIndexException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class FieldNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Util:
    def build_space(string: str, max: int, char: str = ' ') -> str:
        return string + char*(max-len(string))

class Row:
    def __init__(self, content: list) -> None:
        self.content = content
    
    def __repr__(self) -> str:
        return '<Row: [\'' + '\', \''.join(self.content) + '\']>'

class Table:
    def __init__(self, *args: str) -> None:
        '''One integer to define the column size without any headers.\n
        Multiple strings to define the column size and the headers at once.
        '''
        self.header = []
        self.rows = []
        self.max_column_lengths = []
        if len(args) == 0: raise InvalidArgSizeException('__init__(int [positive]) or __init__(*string)')
        elif type(args[0]) == int:
            if not len(args) == 1: raise InvalidArgSizeException('__init__(int [positive]) or __init__(*string)')
            if args[0] <= 0: raise InvalidArgSizeException('__init__(int [positive]) or __init__(*string)')
            self.columns = args[0]
            for i in range(self.columns):
                self.max_column_lengths.append(0)
        else:
            self.columns = len(args)
            for i in range(self.columns):
                self.max_column_lengths.append(0)
            self.set_header(*args)
    
    def set_header(self, *args: str) -> None:
        '''Set the header of the table.\n
        NOTE: Argument length and column size must match!
        '''
        if len(args) != self.columns: raise InvalidArgSizeException(f'Args given: {len(args)}, Column Size: {self.columns} => They must match')
        temp = []
        for i in range(len(args)):
            item = args[i]
            l = len(str(item))
            if self.max_column_lengths[i] < l: self.max_column_lengths[i] = l
            temp.append(str(item))
        self.header = temp.copy()
    
    def add_row(self, *args: str) -> None:
        '''Append a row to the table.\n
        NOTE: Argument length and column size must match!
        '''
        if len(args) != self.columns: raise InvalidArgSizeException(f'Args given: {len(args)}, Column Size: {self.columns} => They must match')
        temp = []
        for i in range(len(args)):
            item = args[i]
            l = len(str(item))
            if self.max_column_lengths[i] < l: self.max_column_lengths[i] = l
            temp.append(str(item))
        self.rows.append(Row(temp))
    
    def get_row(self, index: int) -> Row:
        '''Get the row of the <index>.\n
        NOTE: Index must be smaller than row size, else it will be none!
        '''
        if index >= len(self.rows) or index < 0: return None
        else: return self.rows[index]
    
    def remove_row(self, index: int) -> None:
        '''Remove the row of the <index>.\n
        NOTE: Index must be smaller than row size!
        '''
        if index >= len(self.rows) or index < 0: raise InvalidIndexException('Index not found')
        else: del self.rows[index]
    
    def edit_field(self, row_index: int, column_index: int, value: str) -> None:
        '''Edit the filed on row <row_index> and on column <column_index>.\n
        NOTE: Row_Index must be smaller than row size!\n
        NOTE: Column_Index must be smaller than column size!
        '''
        if row_index >= len(self.rows) or row_index < 0 or column_index < 0 or column_index >= self.columns: raise FieldNotFoundException('Row_Index or Column_Index invalid')
        self.rows[row_index].content[column_index] = value
        if self.max_column_lengths[column_index] < len(value): self.max_column_lengths[column_index] = len(value)
    
    def __build_line(self) -> str:
        final = '+'
        for i in range(self.columns):
            final += f'{Util.build_space("", self.max_column_lengths[i] + 2, "-")}+'
        final += '\n'
        return final
    
    def build(self) -> str:
        '''Build the table to a string.
        '''
        final = self.__build_line()

        if len(self.header) == self.columns:
            final += '|'
            for i in range(self.columns):
                final += f' {Util.build_space(self.header[i], self.max_column_lengths[i])} |'
            final += '\n'

            final += self.__build_line()

        for row in self.rows:
            final += '|'
            for i in range(self.columns):
                final += f' {Util.build_space(row.content[i], self.max_column_lengths[i])} |'
            final += '\n'

        final += self.__build_line()

        return final