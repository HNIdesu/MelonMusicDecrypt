# Melon-Music-Decrypt

## Introduction
**Melon-Music-Decrypt** is a Python script designed to decrypt encrypted cache files downloaded from [Melon Music](https://www.melon.com/). This tool allows you to retrieve the original music files from the cache, making them accessible for offline use.

## Usage
To run the script, use the following command in your terminal:
```bash
python melon-music-decrypt.py <directory> [-o <output_directory>]
```
- `<directory>`: The path to the directory containing the encrypted cache files.
- `[-o <output_directory>]`: (Optional) Specify an output directory where the decrypted files will be saved. If not provided, the decrypted files will be saved in the same directory as the input files.

## Dependencies
Before running the script, make sure to install the following Python libraries:
* [`pycryptodome`](https://pypi.org/project/pycryptodome/): A self-contained Python package of low-level cryptographic primitives.
* [`filetype`](https://pypi.org/project/filetype/): A library to infer file types and MIME types from binary data.

You can install the dependencies using `pip`:
```bash
pip install pycryptodome filetype
```