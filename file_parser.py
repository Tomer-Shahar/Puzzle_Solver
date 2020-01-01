import pandas
import os.path
from puzzle_piece import PuzzlePiece

class FileParser:
    """
    Python Class for parsing files for the puzzle solver to solve.

    """
    @staticmethod
    def parse_pieces_file(filepath):
        if not os.path.exists(filepath):
            raise FileExistsError('Incorrect filepath: no puzzle pieces to be found here')

        file_type = filepath.split('.')[-1]
        if file_type == 'xlsx' or file_type == 'xls':
            pieces = FileParser.parse_excel_file(filepath)
        else:
            raise TypeError('This function currently only supports excel files')
        return pieces

    @staticmethod
    def parse_excel_file(filepath):
        xls = pandas.ExcelFile(filepath)
        sheets = [name for name in xls.sheet_names]
        sheets = pandas.read_excel(io=xls, sheet_name=sheets, header=None)
        pieces = []
        i = 1
        for sheet, data in sheets.items():
            shape = FileParser.crop_piece(data.values.tolist())
            piece = PuzzlePiece(shape, i)
            pieces.append(piece)
            i += 1

        return pieces

    @staticmethod
    def crop_piece(uncropped_list):
        """
        Receives a 2d list that contains somewhere a piece. We will crop the list so it contains only the piece itself
        and the necessary empty tiles so that the list will still be a rectangle so we can maintain the dimensions.
        :param uncropped_list: The 2d list that has a puzzle piece in it.
        :return: A cropped list
        """

        cropped_list = FileParser.crop_bottom(uncropped_list)
        transposed_cropped = list(map(list, zip(*cropped_list)))  # transpose the list

        cropped_list = FileParser.crop_bottom(transposed_cropped)  # crop the right side
        cropped_list = list(map(list, zip(*cropped_list)))  # rotate it back

        return cropped_list

    @staticmethod
    def crop_bottom(uncropped_list):
        cropped_list = []
        idx_list = list(enumerate(uncropped_list))  # add indices

        for idx, row in reversed(idx_list):  # cut rows from bottom by beginnings at last row
            if 1 in row:  # The beginning of a piece
                cropped_list = uncropped_list[:idx + 1]
                break

        return cropped_list
