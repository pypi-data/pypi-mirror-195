import requests

from mecord import ftp_upload
from mecord import xy_pb
from pathlib import Path

def upload(src):
    file_name = Path(src).name
    oss_path = f"ftp://192.168.3.220/1TB01/data/mecord/{file_name}"
    http_path = f"http://ftp.xinyu100.com/01/mecord/{file_name}"
    ftp_upload.upload(src)
    return http_path

def uploadUseOss(src, widgetid):
    ossurl = xy_pb.GetOssUrl(widgetid)
    headers = dict()
    # headers['Accept-Encoding'] = 'gzip'
    headers['Content-Type'] = 'application/zip'
    res = requests.put(ossurl, data=open(src, 'rb').read(), headers=headers)
    if res.status_code == 200:
        checkid = xy_pb.OssUploadEnd(widgetid)
        return ossurl, checkid
    else:
        print("upload file fail! res = " + res)
        return "", -1
