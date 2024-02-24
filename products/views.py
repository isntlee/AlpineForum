from django.shortcuts import render
from pytube import YouTube
from .models import Product
from django.shortcuts import get_object_or_404
import re
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile



def download(request):

    if request.method == 'POST' and request.POST['link']:
        link = request.POST['link']
        video = YouTube(link)
        stream_one = video.streams.get_audio_only()
        stream_one._monostate.title = re.sub(r'\W+', '_', stream_one._monostate.title[:20]).lower()
        file_path = stream_one.download('data\media')    
        output_path = clip_audio(file_path)
        detail_store(request, detail_url = output_path)
        return render(request, 'products/index.html')
    else:
        return render(request, 'products/index.html')
    

def clip_audio(file_path):
    
    input_audio_path = file_path
    output_audio_path = file_path[:-5] + '.mp4'
    ffmpeg_extract_subclip(input_audio_path,  0,  30, targetname=output_audio_path) 

    if default_storage.exists(input_audio_path):
        default_storage.delete(input_audio_path)

    with open(output_audio_path, 'rb') as file:
        file_content = file.read()
    
    file_name = output_audio_path.split('/')[-1]

    print("\n\n...file_name", file_name, '\n\n')

    default_storage.save(file_name, ContentFile(file_content))
    
    return output_audio_path




def find_product(request):
    if request.method == 'POST' and request.POST['product_name']:
        
        product_name = request.POST['product_name']
        product_obj = get_object_or_404(Product, slug=product_name)
        detail_store(request, detail_slug = product_obj.slug)

        return render(request, 'products/index.html')
    else:
        return render(request, 'products/index.html')
    


def detail_store(request, detail_url=None, detail_slug=None):
    
    if detail_url:
        request.session['detail_url'] = detail_url
    if detail_slug:
        request.session['detail_slug'] = str(detail_slug)

    
    if 'detail_url' in request.session and 'detail_slug' in request.session:
        print("Both results are present, performing save()...")

        session_url = request.session['detail_url']
        session_slug = request.session['detail_slug']

        product_obj = get_object_or_404(Product, slug=session_slug)

        product_obj.theme_url = session_url
        product_obj.save()
        
        try:
            del request.session['detail_url']
            del request.session['detail_slug']
        except KeyError:
            pass
