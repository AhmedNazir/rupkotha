import io
import time
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from init import getService


def ocr(service, inputFile='', bookname=''):
    # Image with texts (png, jpg, bmp, gif, pdf)
    t = time.time()

    inputFilepath = 'book'+'\\' + bookname + '\\'+'input'+'\\' + inputFile
    outputFilePath = 'book'+'\\' + bookname + '\\'+'output' + '\\' +  inputFile[:-4] + '.txt'  # Text file outputted by OCR

    mime = 'application/vnd.google-apps.document'
    res = service.files().create(
        body={
            'name': inputFile,
            'mimeType': mime
        },
        media_body=MediaFileUpload(
            inputFilepath, mimetype=mime, resumable=True)
    ).execute()

    downloader = MediaIoBaseDownload(
        io.FileIO(outputFilePath, 'w'),
        service.files().export_media(fileId=res['id'], mimeType="text/plain")
    )

    done = False
    while done is False:
        _ , done = downloader.next_chunk() # _ == status

    service.files().delete(fileId=res['id']).execute()
    print(inputFile + ' ' + str(time.time() - t))

    