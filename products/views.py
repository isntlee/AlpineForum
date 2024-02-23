from django.shortcuts import render
from pytube import YouTube
from .models import Product
from django.shortcuts import get_object_or_404
import re
from django.contrib.sessions.models import Session


def download(request):
    if request.method == 'POST' and request.POST['link']:
        link = request.POST['link']
        video = YouTube(link)
        stream_one = video.streams.get_audio_only()
        stream_one._monostate.title = re.sub(r'\W+', '_', stream_one._monostate.title[:20]).lower()
        file_path = stream_one.download('data\media')

        print('\n\n... to_print:', file_path, '\n\n')
        detail_store(request, detail_url = file_path)

        return render(request, 'products/index.html')
    else:
        return render(request, 'products/index.html')
    


def find_product(request):
    if request.method == 'POST' and request.POST['product_name']:
        
        product_name = request.POST['product_name']
        product_obj = get_object_or_404(Product, slug=product_name)

        print('\n\n... product_obj:', product_obj.__dict__ , '\n\n')
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
        print("Both results are present, performing action...")

        session_url = request.session['detail_url']
        session_slug = request.session['detail_slug']

        product_obj = get_object_or_404(Product, slug=session_slug)

        print('\n\n###Testing#1:', product_obj.__dict__, '\n\n')
        print('\n\n###Testing#2:', session_url, '\n\n')
        
        product_obj.theme_url = session_url 
        # print('\n\n###Testing#3:', product_obj, '\n\n')
        product_obj.save()
        # print('\n\n###Testing#4:', product_obj, '\n\n')
        

        try:
            del request.session['detail_url']
            del request.session['detail_slug']
        except KeyError:
            pass 

    print('\n\n... request.session:', request.session, '\n\n')
