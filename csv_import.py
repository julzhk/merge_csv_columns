import csv
from collections import defaultdict

SOURCE_FILENAME = 'data/sample.csv'
TARGET_FILENAME = 'results.csv'
BLANK_DATA = '.'
MERGED_COLUMN_IF_TITLES_INCLUDES = ['your_name', 'country', 'details', 'hospital']
CELL_SEPARATOR = ';'
CONVERT_CSV_SEPARATOR = '_'

fieldnames = set()


def main(data_source_fn=SOURCE_FILENAME):
    column_titles = set()
    column_titles, rows = read_file_make_list_of_dicts(column_titles, data_source_fn)
    for row in rows:
        for cell in dict(row):
            # merge cells together
            convert_list_to_string(cell, row)
    write_data(column_titles, rows)


def write_data(column_titles, rows, fn=TARGET_FILENAME):
    """
    Given a list of dicts & a set of column headings, write them out to a file
    :param column_titles: set of column headings: made up of de-duplicates of the rows dict keys
    :param rows: list of dicts
    :param fn: filename of target
    :return: None
    """
    with open(fn, 'wb') as filehandler:
        csv_writer = csv.DictWriter(filehandler, fieldnames=column_titles)
        csv_writer.writeheader()
        csv_writer.writerows(rows)


def read_file_make_list_of_dicts(column_titles, data_source_fn):
    """

    :param column_titles: list of terms to find in column titles that should be merged into one resulting column
     So if column_titles includes 'car', the data & columns 'red_car', 'blue_car' will be merged, but 'green_bus' will
     be unchanged
    :param data_source_fn: filename of data source csv
    :return: the titles (keys) & data : list of  dicts)
    """
    results_rows = []
    with open(data_source_fn) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            current_results_row = defaultdict(list)
            for column_title in row.copy():
                result_column = column_title
                for mergable_column_title in MERGED_COLUMN_IF_TITLES_INCLUDES:
                    if mergable_column_title in column_title:
                        result_column = mergable_column_title
                        break
                append_to_results_cell(result_column, column_title, current_results_row, row)
            # get column titles (ignore duplicates)
            column_titles |= set(current_results_row.keys())
            results_rows.append(current_results_row)
    return column_titles, results_rows


def append_to_results_cell(results_column_title, source_column_title, current_row, row):
    current_row[results_column_title.replace(BLANK_DATA, CONVERT_CSV_SEPARATOR)].append(row[source_column_title])


def convert_list_to_string(ele, row):
    if type(row[ele]) == list:
        row[ele] = CELL_SEPARATOR.join(row[ele])

if __name__ == '__main__':
    main()

