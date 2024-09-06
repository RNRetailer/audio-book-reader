from gtts import gTTS
from striprtf.striprtf import rtf_to_text
import time
import os
import json
import sys
import signal
import subprocess
import tempfile

# CONFIG ---------------------------------------------------------

language = 'en'
temp_mp3_filename = tempfile.NamedTemporaryFile().name
progress_filename = 'audio_book_progress.json'

aggressive_saving = True
seconds_between_lines = 0.5

# CODE ------------------------------------------------------------

line_index_human_readable = 1
book_location = os.path.abspath(sys.argv[1])

def signal_handler(sig, frame):
    print('Exiting gracefully...')
    save_progress(book_location, line_index_human_readable)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def read_sentence(text):
    myobj = gTTS(text=text, lang=language, slow=False)

    myobj.save(temp_mp3_filename)

    subprocess.call(['mpg123', '-q', temp_mp3_filename])

    time.sleep(seconds_between_lines)

def save_progress(audio_book_filename, line_index_human_readable):
    try:
        with open(progress_filename) as f:
            progress_file_obj = json.load(f)
    except:
        progress_file_obj = {}
    
    progress_file_obj[audio_book_filename] = line_index_human_readable

    with open(progress_filename, 'w') as f:
        json.dump(progress_file_obj, f)
        f.flush()

def load_progress(audio_book_filename):
    try:
        with open(progress_filename) as f:
            progress_file_obj = json.load(f)
    except:
        progress_file_obj = {}

    return progress_file_obj.get(audio_book_filename, 1)

if __name__ == '__main__':
    starting_line_index_human_readable = load_progress(book_location)

    lines = []

    if book_location.endswith('.rtf'):
        with open(book_location) as f:
            possible_lines = f.read().split('.')

            for line in possible_lines:
                line = rtf_to_text(line).strip()

                if line:
                   lines.append(line)
    else:
        with open(book_location) as f:
            possible_lines = f.read().split('.')

            for line in possible_lines:
                line = line.strip()

                if line:
                   lines.append(line)

    lines = lines[starting_line_index_human_readable - 1:]

    if aggressive_saving:
        for line_index, line in enumerate(lines):
            line_index_human_readable = line_index + starting_line_index_human_readable

            print(f'{line_index_human_readable}: {line}')

            try:
                read_sentence(line)
            except Exception as e:
                print(e)

            save_progress(book_location, line_index_human_readable)
    else:
        for line_index, line in enumerate(lines):
            line_index_human_readable = line_index + starting_line_index_human_readable

            print(f'{line_index_human_readable}: {line}')

            try:
                read_sentence(line)
            except Exception as e:
                print(e)
