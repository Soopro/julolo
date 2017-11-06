# coding=utf-8
from __future__ import absolute_import

import xlrd
import datetime


def get_columns(sheet):
    size = sheet.row_len(0)
    values = sheet.row_values(0, 0, size)
    columns = []
    for value in values:
        value = value.split('(')[0]  # remove all `(...)`
        columns.append(value)
    return columns


def get_row_data(row, columns):
    row_data = {}
    counter = 0

    for cell in row:
        # check if it is of date type print in iso format
        if cell.ctype == xlrd.XL_CELL_DATE:
            cell_key = columns[counter].lower().replace(' ', '_')
            row_data[cell_key] = datetime.datetime(
                *xlrd.xldate_as_tuple(cell.value, 0)).isoformat()
        else:
            cell_key = columns[counter].lower().replace(' ', '_')
            row_data[cell_key] = cell.value

        counter += 1
    return row_data


def get_sheet_data(sheet, columns):
    nrows = sheet.nrows
    sheet_data = []

    for idx in range(1, nrows):
        row = sheet.row(idx)
        row_data = get_row_data(row, columns)
        sheet_data.append(row_data)

    return sheet_data


def get_doc_data(workbook):
    nsheets = workbook.nsheets
    workbookdata = {}

    for idx in range(0, nsheets):
        worksheet = workbook.sheet_by_index(idx)
        columns = get_columns(worksheet)
        sheetdata = get_sheet_data(worksheet, columns)
        workbookdata[worksheet.name.lower().replace(' ', '_')] = sheetdata

    return workbookdata


def load_xls(file_path):
    workbook = xlrd.open_workbook(file_path)
    worksheet = workbook.sheet_by_index(0)
    columns = get_columns(worksheet)
    sheetdata = get_sheet_data(worksheet, columns)
    return sheetdata
