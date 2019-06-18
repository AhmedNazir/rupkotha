import io
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

def ocr(service,inputFile = 'sample.png',projectName =''):
    # Image with texts (png, jpg, bmp, gif, pdf)

    inputFilepath =projectName +'\\'+'input'+'\\' + inputFile
    outputFilePath = projectName + '//'+'output' + '//'+ inputFile[:-4] +'.txt'  # Text file outputted by OCR

    mime = 'application/vnd.google-apps.document'
    res = service.files().create(
        body={
            'name': inputFile,
            'mimeType': mime
        },
        media_body=MediaFileUpload(inputFilepath, mimetype=mime, resumable=True)
    ).execute()

    downloader = MediaIoBaseDownload(
        io.FileIO(outputFilePath, 'w'),
        service.files().export_media(fileId=res['id'], mimeType="text/plain")
    )

    done = False
    while done is False:
        status, done = downloader.next_chunk()

    service.files().delete(fileId=res['id']).execute()
    print(inputFile +' '+ str(status))
