from rest_framework.decorators import api_view
from rest_framework.response import Response

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def authenticate_with_credentials_file(credentials_file):
    # Создание объекта GoogleAuth
    gauth = GoogleAuth()
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = 'api/client_secrets.json'

    # Загрузка учетных данных из файла
    if gauth.LoadCredentialsFile(credentials_file) is None:
        gauth.LocalWebserverAuth()

    # Обновление учетных данных (если требуется)
    if gauth.credentials.refresh_token is None:
        gauth.LocalWebserverAuth()
    elif gauth.credentials.access_token_expired:
        gauth.Refresh()

    # Сохранение обновленных учетных данных
    gauth.SaveCredentialsFile("api/credentials.json")
    return gauth

def create_and_upload_file(file_name, file_content, credentials_file):
    gauth = authenticate_with_credentials_file(credentials_file)

    # Загружаем файл
    try:
        drive = GoogleDrive(gauth)
        my_file = drive.CreateFile(
            {
            'title': f'{file_name}'
        })
        my_file.SetContentString(file_content)
        my_file.Upload()

    except Exception as e:
        print(f'Error: {e}')


@api_view(['POST'])
def create_document(request):
    data = request.data
    filename = data['name']
    filedata = data['data']
    if filename and filedata:
        create_and_upload_file(file_name=filename, file_content=filedata, credentials_file='api/credentials.json')
        return Response(f'filename: {filename} was created')
    else:
        return Response('Incorrect request')


