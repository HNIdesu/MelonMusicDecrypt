import re
import os.path as Path
import filetype
import json as JSON
import base64 as Base64
import pathlib
import os
from Crypto.Cipher import ARC4
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from urllib.request import urlopen,Request
from argparse import ArgumentParser

def write_data_to_file(data:bytes, filepath:str):
    if os.path.exists(filepath):
        dir_name, file_name = Path.split(filepath)
        base_name, extension = Path.splitext(file_name)
        counter = 1
        new_filepath = filepath
        while os.path.exists(new_filepath):
            new_filepath = os.path.join(dir_name, f"{base_name}_{counter}{extension}")
            counter += 1
        filepath = new_filepath
    with open(filepath, "wb") as file:
        file.write(data)

def to_path_safe_name(s:str)->str:
    return s.strip().replace('\\', '＼').replace('/', '／').replace(':', '：').replace('*', '⋆').replace('?', '？').replace('"','″').replace('<','＜').replace('>','＞').replace('|','❘').replace('.','')

parser=ArgumentParser()

parser.add_argument("directory")
parser.add_argument("-o","--output_directory",required=False)
args=parser.parse_args()
directory:str=args.directory
if not Path.exists(directory):
    print("directory not exists")
    exit(0)
output_directory=args.output_directory
if not output_directory:
    output_directory=os.curdir
if not Path.exists(output_directory):
    os.makedirs(output_directory)
for curdir,_,filenames in os.walk(directory):
    for filename in filenames:
        if re.match("\d+_\d+_[a-z]+_s\.melon",filename):
            filepath=Path.join(curdir,filename)
            cid,bitrate,metaType,_=filename.split("_")
            request=Request(url=f"https://play.melon.com/cds/delivery/android/streaming_path.json?cpId=AS40&cpKey=14LNC3&v=4.0&resolution=3&appVer=6.10.6.1&cType=1&cId={cid}&metaType={metaType}&sessionId=&bitrate={bitrate}",headers={
                "User-Agent":"AS40; Android 10; 6.10.6.1;",
                "Cookie":"POC=AS40;PCID=def39603-ae0d-4309-9da3-0e36d7c32c98;"
            })
            json=JSON.loads(urlopen(request).read().decode("utf-8"))
            title=json["response"]["CONTENTSINFO"][0]["CNAME"]
            artist=json["response"]["CONTENTSINFO"][0]["ARTISTS"][0]["ARTISTNAME"]
            encrypted_drmkey=json["response"]["GETPATHINFO"]["C"]
            aes=AES.new(bytes.fromhex("CA9BA6A9B2B8B7DE96A691B2A38BE995"),AES.MODE_CBC,bytes.fromhex("0A630365591C7315650D4143625A5F41"))
            drm_key=unpad(aes.decrypt(Base64.b64decode(encrypted_drmkey)),AES.block_size)+b"melondrmkey!@#"
            with open(filepath,"rb") as br:
                data=ARC4.new(drm_key).decrypt(br.read())
            suffix=filetype.guess_extension(data)
            if suffix:
                suffix="."+suffix
            else:
                suffix=".unknown"
            output_filepath=str(pathlib.Path(Path.join(output_directory,to_path_safe_name(f"{artist} - {title}"))).with_suffix(suffix))
            write_data_to_file(data,output_filepath)

