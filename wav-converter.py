import os
from pydub import AudioSegment
from pydub.exceptions import PydubException

EXTENSIONS = ["mp3", "m4a"]


def get_ext(file: str) -> str:
    return file[file.rfind(".") + 1:]


def without_ext(file: str) -> str:
    return file[:file.rfind(".")]


def filter_ext(files: str, ext: str) -> set[str]:
    if not ext.startswith("."):
        ext = "." + ext

    return set(filter(lambda f: f.endswith(ext), files))


if __name__ == "__main__":
    cwd = os.getcwd()
    dir_files = os.listdir(cwd)
    wav_files = wav_files = filter_ext(dir_files, "wav")
    files = set()

    for ext in EXTENSIONS:
        files.update(filter_ext(dir_files, ext))

    wav_files_no_ext = set(map(lambda f: without_ext(f), wav_files))
    to_convert = set(filter(lambda f: without_ext(f)
                     not in wav_files_no_ext, files))

    if len(to_convert) == 0:
        print("\033[91m\nNo files to convert, exiting...\n")
        exit()

    print("\nFiles to convert:")
    for file in files:
        print(f"  {file}")

    if input(f"\nConvert {len(to_convert)} files? (y/n): ") != "y":
        print("\nExiting...\n")
        exit()

    print()

    failed = []
    for i, file in enumerate(to_convert):
        try:
            print(
                f"\033[0;32m({i + 1}/{len(to_convert)})\033[0m Converting: {file}")
            ext = get_ext(file)
            sound = AudioSegment.from_file(file, format=ext)
            sound.export(without_ext(file) + ".wav", format="wav")
        except PydubException:
            print("\033[91mConversion failed")
            failed.append(file)

    if len(failed) != 0:
        print(f"\033[91m\n{len(failed)} files failed:")
        for file in failed:
            print(f"\033[91m  {file}")

    print("\033[0m\nDone! Exiting...\n")
