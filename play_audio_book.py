from striprtf.striprtf import rtf_to_text
from epub_conversion.utils import open_book, convert_epub_to_lines
from multiprocessing import Process, current_process
from bs4 import BeautifulSoup
from termcolor import cprint
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

aggressive_saving = True
default_playback_speed = 1.0
default_seconds_between_lines = 0.5
extra_lines_to_backtrack_when_darkening_previous_lines = 1
maximum_line_length = 75

# CODE ------------------------------------------------------------

# pretty print
def pprint(text) -> None:
    cprint(text, "light_grey", "on_black", attrs=["bold"])

print = pprint

def darken_previous_line(printable_lines) -> None:
    # Cursor up one line

    sys.stdout.write(
        "\033[F" * (
            len(printable_lines) 
            + extra_lines_to_backtrack_when_darkening_previous_lines
        )
    )

    for printable_line in printable_lines:
        cprint(printable_line, "dark_grey", "on_black", attrs=["bold"])
    
temp_mp3_filename = tempfile.NamedTemporaryFile().name
process = None

line_index_human_readable = 1
book_location = os.path.abspath(sys.argv[1])

def graceful_exit(sig, frame):
    if current_process().name != 'MainProcess':
        return

    print(f'Exiting gracefully...')

    save_progress(book_location, line_index_human_readable)

    process.terminate()

    os.system('stty sane')

    exit()

def skip_line(sig, frame):
    process.terminate()

signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTSTP, skip_line)

def read_sentence_impl(text, language, playback_speed):
    myobj = gTTS(text=text, lang=language, slow=False)

    myobj.save(temp_mp3_filename)

    command = f'ffplay -autoexit -v quiet -nodisp -af "atempo={playback_speed}" {temp_mp3_filename}'

    subprocess.call(command, shell=True)

def call_read_sentence(text, playback_speed, seconds_between_lines):
    global process

    process = Process(target=read_sentence_impl, args=(text, language, playback_speed))
    process.start()

    while process.is_alive():
        time.sleep(.5)

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
    for arg_index, argument in enumerate(sys.argv):
        if argument == '--line':
            return int(sys.argv[arg_index + 1])

    try:
        with open(progress_filename) as f:
            progress_file_obj = json.load(f)
    except:
        progress_file_obj = {}

    return progress_file_obj.get(audio_book_filename, 1)

def get_playback_speed_multiplier():
    for arg_index, argument in enumerate(sys.argv):
        if argument == '--speed':
            return float(sys.argv[arg_index + 1])

    return default_playback_speed

def get_seconds_between_lines():
    for arg_index, argument in enumerate(sys.argv):
        if argument == '--seconds-between-lines':
            return float(sys.argv[arg_index + 1])

    return default_seconds_between_lines

def get_lines_to_print(line_index_human_readable, text, chunk_length=maximum_line_length):
    printable_lines = ['--']

    text = f'{line_index_human_readable}: {text}'

    current_line = []
    current_line_length = 0

    for word in text.split(' '):
        word_length = len(word)
        would_be_current_line_length = current_line_length + word_length + 1

        if current_line_length + word_length <= chunk_length:
            current_line_length = would_be_current_line_length
            current_line.append(word)
        else:
            printable_lines.append(' '.join(current_line))
            current_line = [word]
            current_line_length = len(word)

    if current_line:
        printable_lines.append(' '.join(current_line))

    return printable_lines

def print_lines(printable_lines):
    for printable_line in printable_lines:
        print(printable_line)

if __name__ == '__main__':
    starting_line_index_human_readable = load_progress(book_location)
    playback_speed = get_playback_speed_multiplier()
    seconds_between_lines = get_seconds_between_lines()

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

        for line in convert_epub_to_lines(book):
            lines.extend([
                sentence.strip()
                for sentence in BeautifulSoup(line, features="html.parser").get_text().split('.') 
                if sentence.strip()
            ])

    else:
        with open(book_location) as f:
            possible_lines = f.read().split('.')

            for line in possible_lines:
                line = line.strip()

                if line:
                   lines.append(line)

    lines = lines[starting_line_index_human_readable - 1:]

    opening_line = f'Reading {sys.argv[1]} starting at line {starting_line_index_human_readable}.'

    print(f'\n{opening_line}\n')
    print('Press Control + z to skip a line.')
    print('Press Control + c to exit.\n')
    print(f'{"-" * len(opening_line)}\n')

    if aggressive_saving:
        for line_index, line in enumerate(lines):
            line_index_human_readable = line_index + starting_line_index_human_readable

            printable_lines = get_lines_to_print(line_index_human_readable, line)

            print_lines(printable_lines)

            try:
                call_read_sentence(line, playback_speed, seconds_between_lines)
            except Exception as e:
                print(e)

            darken_previous_line(printable_lines)

            save_progress(book_location, line_index_human_readable)
    else:
        for line_index, line in enumerate(lines):
            line_index_human_readable = line_index + starting_line_index_human_readable

            printable_lines = get_lines_to_print(line_index_human_readable, line)

            print_lines(printable_lines)

            try:
                call_read_sentence(line, playback_speed, seconds_between_lines)
            except Exception as e:
                print(e)

            darken_previous_line(printable_lines)

    graceful_exit(None, None)
