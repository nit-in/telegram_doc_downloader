# telegram_doc_downloader
Download documents from a public channel in telegram
This script will download documents from a public telegram channel
also check for files that are already downloaded and skip them

## How to use:
lets say you want to download document from a telegram channels called channel1, channel2, channel3 and so on for 10 pages

to do so
```
edit config.py
CHANNELS = ["channel1", "channel2", "channel3"]
PAGES = 10
```
To change the directory where documents will get downloaded
Lets say you want to download documents to "~/telegram/files"
```
edit config.py
DOWNLOAD_DIR = "~/telegram/files"
```

then just run the python script

```
chmod +x downloader.py
./downloader.py
```

## More Info and Credits:

This is inspired from [DL-Telegram-by-file-attachment](https://github.com/Mte90/DL-Telegram-by-file-attachment)

and credits to [xtrime](https://tg.i-c-a.su/) for telegram to json server
