import os, re, dropbox, requests

from django.shortcuts import render, get_object_or_404
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pytube import YouTube
from dotenv import load_dotenv
from pathlib import Path 

from .models import Product

from core.settings import DROPBOX_ACCESS_KEY, DROPBOX_OAUTH2_REFRESH_TOKEN, DROPBOX_APP_KEY, DROPBOX_APP_SECRET



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


def refresh_access_token(refresh_token, app_key, app_secret):
    token_url = "https://api.dropboxapi.com/oauth2/token"
    params = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": app_key,
        "client_secret": app_secret
    }
    response = requests.post(token_url, params=params)
    if response.status_code ==  200:
        new_access_token = response.json().get('access_token')
        print("New access token:", new_access_token)
    else:
        print("Failed to refresh access token:", response.text)
    return new_access_token


def clip_audio(file_path):
    
    input_audio_path = file_path
    output_audio_path = file_path[:-5] + '.mp4'

    ffmpeg_extract_subclip(input_audio_path,  0,  30, targetname=output_audio_path) 

    with open(output_audio_path, 'rb') as file:
        file_content = file.read()
    
    file_name = output_audio_path.split('/')[-1]
    last_slash_index = input_audio_path.rfind("\\") + 1
    file_name = '/' + input_audio_path[last_slash_index:]

    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_KEY)
        url_name = dbx.files_upload(file_content, file_name, mode=dropbox.files.WriteMode('overwrite'))
        
    except dropbox.exceptions.AuthError:
        new_access_token = refresh_access_token(DROPBOX_OAUTH2_REFRESH_TOKEN, DROPBOX_APP_KEY, DROPBOX_APP_SECRET)
        env_path = Path('.') / '.env'

        try:
            load_dotenv(dotenv_path=env_path) 
        except Exception as e:
            print(f"Failed to load .env file: {e}")

        try:
            with open('.env', 'a') as env_file:
                env_file.write(f'\nDROPBOX_ACCESS_KEY= {new_access_token}')
        except Exception as e:
            print(f"Failed to append to .env file: {e}")

        dbx = dropbox.Dropbox(new_access_token)
        url_name = dbx.files_upload(file_content, file_name, mode=dropbox.files.WriteMode('overwrite'))
        print('\n\n', url_name)
        
    for path in [input_audio_path, output_audio_path]:
        if os.path.isfile(path):
            os.remove(path)



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
