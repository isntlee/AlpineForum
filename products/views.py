from django.shortcuts import render
from pytube import YouTube

def download_video(request):
    if request.method == 'POST':
        link = request.POST['link']
        video = YouTube(link)
        stream_one = video.streams.get_audio_only()
        stream_one._monostate.title = stream_one._monostate.title[:20]
        stream_one.download('data/media')

        # print('\n\n... Stream one', stream_one.__dict__ ,'\n\n')
        
        return render(request, 'products/download.html')
    else:
        return render(request, 'products/download.html')
