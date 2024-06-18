from enum import Enum
import shutil
import subprocess
import sys
import asstosrt
import json
import os
import argparse
from pathlib import Path
from deep_translator import GoogleTranslator

parser = argparse.ArgumentParser()
parser.add_argument('--mode', type=int)
parser.add_argument('--mkv_file', type=str)
parser.add_argument('--ass_file', type=str)
parser.add_argument('--ass_file_language', type=str)
args = parser.parse_args()

class Modes(Enum):
    GENERATE_MKV_WITH_SRT = 1
    CONVERT_ASS_TO_SRT = 2
    TRANSLATE_SRT = 3
    MERGE_SRT_INTO_MKV = 4
    

def get_mkv_file_info(file_name):
    result = subprocess.run(['mkvmerge', '--identification-format', 'json', '--identify', file_name], capture_output=True, text=True)
    return json.loads(result.stdout)

def generate_mkv_temp_file(file_name):
    print("---------- GENERATING .MKV TEMP ----------")
    shutil.move(file_name, "input.mkv")

def merge_subtitles_in_mkv(file_name, new_subtitle_files):
    print("---------- GENERATING NEW .MKV FILE WITH SRT SUBTITLES ----------")
    create_new_mkv_command = f"mkvmerge -o '{file_name}' input.mkv {new_subtitle_files}"
    subprocess.check_call(create_new_mkv_command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)

def delete_temp_mkv_file():
    temp_mkv_path = Path('input.mkv')
    if temp_mkv_path.exists():
        temp_mkv_path.unlink()        

def update_mkv_subtitle_tracks_info(file_name, track_language, language_track_id):
    print(f"---------- UPDATING '{track_language} - {language_track_id}' SRT TRACK ----------")

    language_track_name = language_track_id.split("-")[1] if len(language_track_id.split("-")) > 1 else "" 
    language_track_id = language_track_id.split("-")[0]        
    language_track_number = int(language_track_id) + 1
    set_language_command = f"mkvpropedit '{file_name}' --edit track:{language_track_number} --set language={track_language}"
    subprocess.check_call(set_language_command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)
    set_track_name = f"mkvpropedit '{file_name}' --edit track:{language_track_number} --set name='{language_track_name}'"
    subprocess.check_call(set_track_name, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)
    
    srt_path = Path(f'{track_language}-{language_track_id}.srt')
    ass_path = Path(f'{track_language}-{language_track_id}.ass')
    
    if srt_path.exists():
        srt_path.unlink()
    if ass_path.exists():
        ass_path.unlink()

def extract_mkv_ass_track(file_name, track_id, track_language):
    extract_command = f"mkvextract tracks '{file_name}' {track_id}:{track_language}-{track_id}.ass"
    subprocess.check_call(extract_command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)

def convert_ass_to_srt(ass_file_name, track_language, latest_track_number):
    ass_file = open(ass_file_name)
    srt_str = asstosrt.convert(ass_file)
    
    language_track_id = int(latest_track_number) + 1
    str_file = open(f'{track_language}-{language_track_id}.srt', 'w')
    str_file.write(srt_str)
    str_file.close()

def translate_srt(file_name, original_language, new_language):
    '''
    if Path('eng.srt').exists() and not (Path('spa.srt').exists()):
        print("---------- GENERATING 'ESP' SUBTITLES ----------")
        generate_new_mkv = True
        with open('eng.srt', encoding="utf-8") as f:
            content = f.read()
            print("Reading eng.srt file")
            lines = content.split("\n")
            f.close()

        translated_content = str(content)
        counter = 1

        lines_to_translate = list(filter(lambda line: ((line.isdigit() == False) and ("-->" not in line) and "" != line), lines))

        for line in lines_to_translate:
            print(f"Translating... [{counter}/{len(lines_to_translate)}]")
            translation = GoogleTranslator(source='english', target='spanish').translate(line)
            safe_translation = "" if translation is None else translation
            translated_content = translated_content.replace(line, safe_translation)
            counter += 1
                
        output_srt = open("spa.srt", "w", encoding="utf-8")

        output_srt.write(translated_content)
        output_srt.close()
        if not("spa" in track_language_dict.keys()):
            last_key = list(track_language_dict)[-1]
            last_value = track_language_dict[last_key]
            track_language_dict["spa"] = str(int(last_value) + 1)
        new_subtitle_files = new_subtitle_files + ' spa.srt'
        print(json.dumps(track_language_dict))
    '''

def update_new_subtitles_files(new_subtitle_files, track_language, language_track_id):
    return new_subtitle_files + f' {track_language}-{language_track_id}.srt' 

def parse_mkv_subtitle_track(track, file_name, latest_track_number, language_track_id, track_language_dict):
    track_id = track["id"]
    if "SubStationAlpha" in track["codec"]:
        track_language = track["properties"]["language"]
        track_name = track["properties"]["track_name"] if "track_name" in track["properties"].keys() else track_language
        
        extract_mkv_ass_track(file_name, track_id, track_language)
        convert_ass_to_srt(f'{track_language}-{track_id}.ass', track_language, latest_track_number)

        language_entry = f"{language_track_id} - {track_name}"
        if track_language in track_language_dict.keys():
            track_language_dict[track_language].append(language_entry)
        else:
            track_language_dict[track_language] = [language_entry] 
    
    #TODO
    if "SubRip/SRT" in track["codec"]:
        track_language = track["properties"]["language"]
        extract_command = f"mkvextract tracks '{file_name}' {track_id}:{track_language}.srt"
        subprocess.check_call(extract_command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)
        language_track_id = int(track_id) + 1
        track_language_dict[track_language] = str(language_track_id)

    return track_language_dict



mode = Modes[args.mode] if args.mode is not None else Modes.GENERATE_MKV_WITH_SRT
full_path = args.mkv_file
file_name = Path(full_path).name
folder_path = os.path.dirname(full_path)
os.chdir(folder_path)

mkv_json_info = get_mkv_file_info(file_name)

new_subtitle_files = ""
track_language_dict = {}


if mode == Modes.GENERATE_MKV_WITH_SRT:
    print("---------- PARSING CURRENT .MKV FILE ----------")
    latest_track_number = mkv_json_info["tracks"][-1]["id"]
    for track in mkv_json_info["tracks"]:
        if "SubStationAlpha" in track["codec"] or "SubRip/SRT" in track["codec"]:
            language_track_id = int(latest_track_number) + 1
            track_language_dict = parse_mkv_subtitle_track(track, file_name, latest_track_number, language_track_id, track_language_dict)
            new_subtitle_files = update_new_subtitles_files(new_subtitle_files, track["properties"]["language"], language_track_id)
            latest_track_number += 1
        
    print(json.dumps(track_language_dict))

    generate_mkv_temp_file(file_name)
    merge_subtitles_in_mkv(file_name, new_subtitle_files)
    delete_temp_mkv_file()

    print(json.dumps(track_language_dict))

    for track_language,language_track_id_list in track_language_dict.items():
        for language_track_id in language_track_id_list:
            update_mkv_subtitle_tracks_info(file_name, track_language, language_track_id)

if mode == Modes.CONVERT_ASS_TO_SRT:
    convert_ass_to_srt(args.ass_file, args.ass_file_language, "1")

if mode == Modes.TRANSLATE_SRT:
    translate_srt("a", "en", "es")

if mode == Modes.MERGE_SRT_INTO_MKV:
    raise Exception("Mode not supported yet.")