#!/usr/bin/python

import requests
import json
from pathlib import Path
import subprocess
import config

channel = config.CHANNEL
pages = config.PAGES
download_dir = config.DOWNLOAD_DIR
download_dir_path = Path(download_dir).expanduser()


#check if download dir exists or not
#if it doesn't exists make it

if download_dir_path.exists():
	print(str(download_dir_path) + " already exists")
else:
	print("\nmaking" + str(download_dir_path))
	download_dir_path.mkdir(parents = True)
	print("\nmade " + str(download_dir_path) + " dir")

#check if a file already exists or not in the download dir
def check_file(name,size):
	file_name = Path(download_dir_path,name)
	#check bpth file name and size
	if file_name.exists() and int(file_name.lstat().st_size) == int(size):
		return True
	else:
		return False

#download the document using wget
def download(channel,name,msg_id):
	download_url = config.MEDIA_URL + str(channel) +"/" + str(msg_id)
	file_name = Path(download_dir_path,name)
	program = "wget"
	arg1 = "--show-progress"
	arg2 = "--server-response"
	arg3 = "--continue"
	arg4 = "-O"
	print(f"\nDownloading: {name}")
	print(f"\nlink: {download_url}")
	subprocess.call([program,arg1,arg2,arg3,str(download_url),arg4,str(file_name)])


#parse json that was returned and get name, size and id for document and download it
def parse_json(json_data):
	for msg in json_data['messages']:
		if 'media' in msg:
			media_msg = msg['media']
			if 'document' in media_msg:
				document_media_msg = media_msg['document']
				if 'attributes' in document_media_msg and 'size' in document_media_msg:
					attr_document_media_msg = document_media_msg['attributes'][0]
					if 'file_name' in attr_document_media_msg and 'size' in document_media_msg:
						filename = attr_document_media_msg['file_name']
						size = document_media_msg['size']
						msg_id = msg['id']
						name = str(filename.replace(" ","_"))
						if check_file(name,size):
							print(f"\nalready downloaded:\nname:\t{name}\nsize:\t{size}")
						else:
							print(f"\ndownload:\nname:\t{name}\nsize:\t{size}")
							download(channel,name,msg_id)

#iterate 
for page in range(1,pages):
	print(f"\nchannel:	{channel}")
	print(f"\nPage:	{page}")

	url = config.JSON_URL + str(channel) + "/" + str(page) + "?limit=100"
	re = requests.get(url)
	data = json.loads(re.text)
	parse_json(data)