import os
from pydub import AudioSegment


def convert_mp3_to_ogg(input_file):
    # Check if the input file is an MP3 file
    if not input_file.lower().endswith('.mp3'):
        print("Input file is not an MP3 file.")
        return None

    # Define output file path with OGG extension
    name, _ = os.path.splitext(input_file)
    output_file = f"{name}.ogg"

    # Load the audio file
    sound = AudioSegment.from_file(input_file)

    # Export the audio in OGG format
    sound.export(output_file, format='ogg')

    os.remove(input_file)

    return output_file

# Example usage:
converted_file_path = convert_mp3_to_ogg("minor-progress_(uzhits.net).mp3")
print(f'Converted file path: {converted_file_path}')
