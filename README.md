# MKV Subtitle Management Tool

This tool provides functionalities for managing subtitles in MKV (Matroska) video files. It allows you to:

- Generate an MKV file with SRT subtitles extracted and converted from ASS subtitles.
- Convert ASS subtitle files to SRT format.
- Translate SRT subtitle files using Google Translate.
- Merge SRT subtitles into an MKV file.

Table of Contents
Installation
Usage
Generate MKV with SRT
Convert ASS to SRT
Translate SRT
Merge SRT into MKV
Arguments
Dependencies

## Installation
To use this tool, you need to have the following dependencies installed:

mkvtoolnix (includes mkvmerge, mkvextract, mkvpropedit)
python (>= 3.6)
asstosrt Python package
deep_translator Python package
You can install the Python dependencies using pip:

```sh
pip install asstosrt deep_translator
```

Ensure mkvmerge, mkvextract, and mkvpropedit are available in your system's PATH. You can download mkvtoolnix from MKVToolNix.

## Usage
The tool is executed from the command line. Below are the different modes of operation:

### Generate MKV with SRT
Extracts and converts ASS subtitles to SRT, and then merges them into the MKV file.

```sh
python script.py --mode 1 --mkv_file /path/to/your/file.mkv
```

## Convert ASS to SRT
Converts a standalone ASS file to SRT format.

``` sh
python script.py --mode 2 --ass_file /path/to/your/file.ass --ass_file_language <language_code>
```

## Translate SRT
Translates the content of an SRT file from one language to another.

```sh
python script.py --mode 3 --srt_file /path/to/your/file.srt --source_language <source_lang> --target_language <target_lang>
```

## Merge SRT into MKV
Merges an SRT file into an MKV file.

```sh
python script.py --mode 4 --mkv_file /path/to/your/file.mkv --srt_file /path/to/your/file.srt
```

### Arguments
- --mode (int): The mode of operation. (1: Generate MKV with SRT, 2: Convert ASS to SRT, 3: Translate SRT, 4: Merge SRT into MKV)
- --mkv_file (str): The path to the MKV file.
- --ass_file (str): The path to the ASS subtitle file.
- --ass_file_language (str): The language code of the ASS subtitle file.
- --srt_file (str): The path to the SRT subtitle file.
- --source_language (str): The source language code for translation.
- --target_language (str): The target language code for translation.


### Dependencies
enum
subprocess
sys
asstosrt
json
os
argparse
pathlib
deep_translator
Example
To generate an MKV file with SRT subtitles from an MKV file containing ASS subtitles:

```sh
python script.py --mode 1 --mkv_file /path/to/your/file.mkv
```

This will extract the ASS subtitles, convert them to SRT, and merge them back into the MKV file, updating the track information accordingly.

By following this README, you should be able to use the provided script effectively for managing subtitles in your MKV files. If you encounter any issues or have questions, feel free to open an issue or contact the maintainer.
