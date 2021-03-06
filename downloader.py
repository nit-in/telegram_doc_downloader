#!/usr/bin/python

import requests
import json
from pathlib import Path
import subprocess
import config
import time

channels = config.CHANNELS
pages = config.PAGES
download_dir = config.DOWNLOAD_DIR
download_dir_path = Path(download_dir).expanduser()

fails = "failed.txt"
cwd = Path.cwd()
failed_file = Path(cwd, fails)
# check if download dir exists or not
# if it doesn't exists make it


def check_path(dir_path):
    path_dir = Path(dir_path)
    if path_dir.exists():
        print("\n\t------------------------\t\n")
        print(str(download_dir_path) + " already exists")
    else:
        print("\n\t------------------------\t\n")
        print("\nmaking" + str(path_dir))
        path_dir.mkdir(parents=True)
        print("\n\t------------------------\t\n")
        print("\nmade " + str(path_dir) + " dir")


if failed_file.exists():
    failed_file.unlink()

# check if a file already exists or not in the download dir
def check_file(channel, name, size):
    channel_path = Path(download_dir_path, channel)
    file_name = Path(channel_path, name)
    # check bpth file name and size
    if file_name.exists() and int(file_name.lstat().st_size) == int(size):
        return True
    else:
        return False


# download the document using wget
def download(channel, name, msg_id):
    download_url = config.MEDIA_URL + str(channel) + "/" + str(msg_id)
    channel_path = Path(download_dir_path, channel)
    check_path(channel_path)
    pdf_name = Path(channel_path, name)
    file_name = Path(download_dir_path, pdf_name)
    program = "wget"
    arg1 = "--show-progress"
    arg2 = "--server-response"
    arg3 = "--continue"
    arg4 = "-O"
    print("\n\t------------------------\t\n")
    print(f"\nDownloading: {name}")
    print(f"\nlink: {download_url}")
    subprocess.call(
        [program, arg1, arg2, arg3, str(download_url), arg4, str(file_name)]
    )


def fail(txt):
    with open(failed_file, "a") as f:
        f.writelines(txt)


# parse json that was returned and get name, size and id for document and download it
def parse_json(json_data, channel, initial_prompt):
    for msg in json_data["messages"]:
        if "media" in msg:
            media_msg = msg["media"]
            if "document" in media_msg:
                document_media_msg = media_msg["document"]
                if "attributes" in document_media_msg and "size" in document_media_msg:
                    attr_document_media_msg = document_media_msg["attributes"][0]
                    if (
                        "file_name" in attr_document_media_msg
                        and "size" in document_media_msg
                    ):
                        filename = attr_document_media_msg["file_name"]
                        size = document_media_msg["size"]
                        msg_id = msg["id"]
                        name = str(filename.replace(" ", "_"))
                        file_size = "{:.1f}".format(size / (1024 * 1024))
                        channel = str(channel)
                        if check_file(channel, name, size):
                            print(
                                f"\nalready downloaded:\nname:\t{name}\nsize:\t{file_size} MB\nchannel:\t{channel}"
                            )
                        else:
                            if size <= 31457280:  # only 30 mb file size is allowed
                                print(
                                    f"\ndownload:\nname:\t{name}\nsize:\t{file_size} MB\nchannel:\t{channel}"
                                )
                                if initial_prompt == "y" or initial_prompt == "Y":
                                    download_prompt = str(
                                        input(
                                            f"Do you want to download the file:\t{name}\t"
                                        )
                                    )

                                    if download_prompt == "y" or download_prompt == "Y":
                                        download(channel, name, msg_id)
                                        time.sleep(10)
                                    else:
                                        pass
                                else:
                                    download(channel, name, msg_id)
                                    time.sleep(10)

                            else:
                                print(
                                    f"\nFile size is high, skipping it:\nname:\t{name}\nsize:\t{file_size} MB"
                                )
                                txt = f"\nchannel:\t{channel}\nname:\t{name}\nsize:\t{file_size} MB\n"
                                txt = txt + f"\n\t------------------------\t\n"
                                fail(txt)


check_path(download_dir_path)
# print list of channels
print("\n\t------------------------\t\n")
print(channels)

print("\n\t------------------------\t\n")
initial_prompt = str(
    input(
        f"Do you want download prompt for every file (y/Y for prompt OR any other key for No prompt)?\t"
    )
)

# iterate
for page in range(1, pages):
    for channel in channels:
        print("\n\t------------------------\t\n")
        print(f"\nchannel:	{channel}")
        print(f"\nPage:	{page}")
        url = config.JSON_URL + str(channel) + "/" + str(page) + "?limit=100"
        time.sleep(10)
        re = requests.get(url)
        data = json.loads(re.text)
        # check for errors, in case of any error
        # print out response from server and quit
        if "errors" in data:
            print("\n" + data["errors"][0])
            print("\nmessage\t" + data["errors"][1]["message"])
            print("\nfor url\t" + data["errors"][1]["url"])
            exit()
        else:
            parse_json(data, channel, initial_prompt)
