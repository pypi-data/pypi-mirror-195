from sabia_utils.utils.parquet_utils import concatenate_parquet_files, delete_duplicate_rows, take_files_from_path

import os
import glob

parquet_files = glob.glob(os.path.join(os.path.dirname(__file__), "data", "*.parquet"))
TEST_PARQUET_PATH = 'test/data'

def test_concatene_parquet_files():
    parquet_files.sort()
    df = concatenate_parquet_files(parquet_files)
    expectation = {
        "processo_numero":
        {
            0: "A0",
            1: "A1",
            2: "A2",
            3: "A3",
            4: "A4",
            5: "A5",
            6: "A6",
            7: "A7",
            8: "A8",
            9: "A9",
            10: "A10",
            11: "A11",
            12: "A0",
            13: "A1",
            14: "A12",
            15: "A13"
        },
        "B":
        {
            0: "B0",
            1: "B1",
            2: "B2",
            3: "B3",
            4: "B4",
            5: "B5",
            6: "B6",
            7: "B7",
            8: "B8",
            9: "B9",
            10: "B10",
            11: "B11",
            12: "A0",
            13: "A1",
            14: "B12",
            15: "B13"
        },
        "C":
        {
            0: "C0",
            1: "C1",
            2: "C2",
            3: "C3",
            4: "C4",
            5: "C5",
            6: "C6",
            7: "C7",
            8: "C8",
            9: "C9",
            10: "C10",
            11: "C11",
            12: "A0",
            13: "A1",
            14: "C12",
            15: "C13"
        },
        "D":
        {
            0: "D0",
            1: "D1",
            2: "D2",
            3: "D3",
            4: "D4",
            5: "D5",
            6: "D6",
            7: "D7",
            8: "D8",
            9: "D9",
            10: "D10",
            11: "D11",
            12: "A0",
            13: "A1",
            14: "D12",
            15: "D13"
        },
    }
    assert df.to_dict() == expectation


def test_delete_duplicate_rows():
    parquet_files.sort()
    df = concatenate_parquet_files(parquet_files)
    df = delete_duplicate_rows(df)
    expectation = {
        "processo_numero":
        {
            2: "A2",
            3: "A3",
            4: "A4",
            5: "A5",
            6: "A6",
            7: "A7",
            8: "A8",
            9: "A9",
            10: "A10",
            11: "A11",
            12: "A0",
            13: "A1",
            14: "A12",
            15: "A13"
        },
        "B":
        {
            2: "B2",
            3: "B3",
            4: "B4",
            5: "B5",
            6: "B6",
            7: "B7",
            8: "B8",
            9: "B9",
            10: "B10",
            11: "B11",
            12: "A0",
            13: "A1",
            14: "B12",
            15: "B13"
        },
        "C":
        {
            2: "C2",
            3: "C3",
            4: "C4",
            5: "C5",
            6: "C6",
            7: "C7",
            8: "C8",
            9: "C9",
            10: "C10",
            11: "C11",
            12: "A0",
            13: "A1",
            14: "C12",
            15: "C13"
        },
        "D":
        {
            2: "D2",
            3: "D3",
            4: "D4",
            5: "D5",
            6: "D6",
            7: "D7",
            8: "D8",
            9: "D9",
            10: "D10",
            11: "D11",
            12: "A0",
            13: "A1",
            14: "D12",
            15: "D13"
        }
    }
    assert df.to_dict() == expectation


def test_take_files_from_path():
    files = take_files_from_path(TEST_PARQUET_PATH)
    files.sort()
    assert files == [
        'test/data\\df1_test.parquet',
        'test/data\\df2_test.parquet',
        'test/data\\df3_test.parquet',
        'test/data\\df4_test.parquet'
        ]


def test_concatene_parquet_files_exception():
    df = concatenate_parquet_files(str)
    assert df is None


def test_delete_duplicate_rows_exception():
    df = delete_duplicate_rows(str)
    assert df is None


def test_take_files_from_path_exception():
    files = take_files_from_path(str)
    assert files is None

