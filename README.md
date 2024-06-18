
# MKV Subtitle Management Tool

This tool provides functionalities for managing subtitles in MKV (Matroska) video files. It allows you to:

- Generate an MKV file with SRT subtitles extracted and converted from ASS subtitles.
- Convert ASS subtitle files to SRT format.
- Translate SRT subtitle files using Google Translate.
- Merge SRT subtitles into an MKV file.

# Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
  1. [Generate MKV with SRT](#generate-mkv-with-srt)
  2. [Convert ASS to SRT](#convert-ass-to-srt)
  3. [Translate SRT](#translate-srt)
  4. [Merge SRT into MKV](#merge-srt-into-mkv)


## Installation <a name="installation"></a>
To use this tool, you need to have the following dependencies installed:

- [mkvtoolnix](https://mkvtoolnix.download/downloads.html) (includes mkvmerge, mkvextract, mkvpropedit)
- Python (>= 3.6)
- [asstosrt](https://pypi.org/project/asstosrt/) Python package
- [deep_translator](https://pypi.org/project/deep-translator/) Python package
  
You can install the Python dependencies using pip:

```sh
pip install -r requirements.txt
```

Ensure mkvmerge, mkvextract, and mkvpropedit are available in your system's PATH. You can download mkvtoolnix from [MkvToolnix](https://mkvtoolnix.download/downloads.html).

## Usage <a name="usage"></a>
The tool is executed from the command line. Below are the different modes of operation:

### Generate MKV with SRT <a name="generate-mkv-with-srt"></a>
Extracts and converts ASS subtitles to SRT, and then merges them into the MKV file.

```sh
python script.py --mode 1 --mkv_file /path/to/your/file.mkv
```

### Convert ASS to SRT <a name="convert-ass-to-srt"></a>
Converts a standalone ASS file to SRT format.

``` sh
python script.py --mode 2 --ass_file /path/to/your/file.ass --ass_file_language <language_code>
```

### Translate SRT <a name="translate-srt"></a>
Translates the content of an SRT file from one language to another.

```sh
python script.py --mode 3 --srt_file /path/to/your/file.srt --source_language <source_lang> --target_language <target_lang>
```

### Merge SRT into MKV <a name="merge-srt-into-mkv"></a>
Merges an SRT file into an MKV file.

```sh
python script.py --mode 4 --mkv_file /path/to/your/file.mkv --srt_file /path/to/your/file.srt
```

### Arguments
- **--mode (int):** The mode of operation. (1: Generate MKV with SRT, 2: Convert ASS to SRT, 3: Translate SRT, 4: Merge SRT into MKV)
- **--mkv_file (str):** The path to the MKV file.
- **--ass_file (str):** The path to the ASS subtitle file.
- **--ass_file_language (str):** The language code of the ASS subtitle file.
- **--srt_file (str):** The path to the SRT subtitle file.
- **--source_language (str):** The source language code for translation.
- **--target_language (str):** The target language code for translation.


By following this README, you should be able to use the provided script effectively for managing subtitles in your MKV files. 

If you encounter any issues or have questions, feel free to open an issue.
