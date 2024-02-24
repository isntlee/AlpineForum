from django.http import HttpResponse
from pydub import AudioSegment

def clip_audio(file_path):

    print('\n\n... file_path:', file_path, '\n\n')

    str_path = str(file_path)
    
    print('\n\n... str_path:', str_path, '\n\n')

    audio = AudioSegment.from_file(str_path, format="mp4")

    # Clip the first  30 seconds of the audio
    clipped_audio = audio[:30000]  # pydub works in milliseconds
    # Save the clipped audio to a new file

    print('\n\n... file_path:', file_path, '\n\n')
    print('\n\n... clipped_audio:', clipped_audio, '\n\n')

    clipped_audio.export("path/to/save/clipped_audio.mp3", format="mp3")
    # Return a response indicating the operation was successful
    return HttpResponse('Audio clipped successfully.')