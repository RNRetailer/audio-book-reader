from striprtf.striprtf import rtf_to_text
from epub_conversion.utils import open_book, convert_epub_to_lines
from multiprocessing import Process
from bs4 import BeautifulSoup
from gtts import gTTS
import time
import os
import json
import sys
import signal
import tempfile
import subprocess

# CONFIG ---------------------------------------------------------

language = 'en'
progress_filename = 'audio_book_progress.json'
temp_mp3_filename = tempfile.NamedTemporaryFile().name

aggressive_saving = True
seconds_between_lines = 0.5

process = None

# CODE ------------------------------------------------------------

line_index_human_readable = 1
book_location = os.path.abspath(sys.argv[1])

def graceful_exit(sig, frame):
    print('Exiting gracefully...')
    save_progress(book_location, line_index_human_readable)
    sys.exit(0)

def skip_line(sig, frame):
    process.terminate()

signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTSTP, skip_line)

def read_sentence_impl(text, language):
    myobj = gTTS(text=text, lang=language, slow=False)

    myobj.save(temp_mp3_filename)

    subprocess.call(['mpg123', '-q', temp_mp3_filename])

def call_read_sentence(text):
    global process
    process = Process(target=read_sentence_impl, args=(text, language))
    process.start()

    while process.is_alive():
        pass

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
    elif book_location.endswith('.epub'):
        book = open_book(book_location)

        lines = [
            BeautifulSoup(line, features="html.parser").get_text()
            for line in convert_epub_to_lines(book)
        ]
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
                call_read_sentence(line)
            except Exception as e:
                print(e)

            save_progress(book_location, line_index_human_readable)
    else:
        for line_index, line in enumerate(lines):
            line_index_human_readable = line_index + starting_line_index_human_readable

            print(f'{line_index_human_readable}: {line}')

            try:
                call_read_sentence(line)
            except Exception as e:
                print(e)