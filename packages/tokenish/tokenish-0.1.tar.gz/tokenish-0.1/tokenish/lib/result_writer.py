import os


class ResultWriter:

    def __init__(self, directory_path, max_row_per_file):
        self.directory_path = directory_path
        self.max_row_per_file = max_row_per_file
        self.current_file = None
        self.file_counter = -1
        self.row_counter = 0

    def write_row(self, row):
        if self.current_file is None or self.max_row_per_file <= self.row_counter:
            self.close_file()
            self.file_counter += 1
            self.row_counter = 0
            self.current_file = open(os.path.join(self.directory_path, "part_{}.txt".format(self.file_counter)), "w+")
        self.current_file.write(row + "\n")
        self.row_counter += 1

    def close_file(self):
        if self.current_file is not None:
            self.current_file.close()
