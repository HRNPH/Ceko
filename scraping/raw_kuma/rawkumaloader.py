import requests, zipfile, io
import glob
# https://dl.rawkuma.com?id=236678

def download(url:str, save_path:str) -> bool:
    req = requests.get(url)
    existed = 200
    if req.status_code != existed:
        return False
    try:
        zip = zipfile.ZipFile(io.BytesIO(req.content))
    except zipfile.BadZipFile:
        return False
    
    glob.os.makedirs(save_path, exist_ok=True)
    zip.extractall(save_path)
    return True

def files_rename(id, save_path:str) -> bool:
    for file in glob.glob(save_path + '/*.jpg'):
        file_name = file.split('\\')[-1]
        new_file_name = file_name.replace('rawkuma.com', str(id))
        print(new_file_name)
        glob.os.rename(file, save_path + '/' + new_file_name)
    return True

def log_record(id) -> bool:
    with open('last_id.txt', 'w') as f:
        f.write(str(id))

def main(startfrom_id=236678):
    current_id = startfrom_id
    while True:
        url = 'https://dl.rawkuma.com?id=' + str(current_id)
        current_id = current_id - 1

        root = './data'
        save_at = f'{root}/{current_id}'
        if download(url, save_path=save_at):
            files_rename(current_id, save_at)
            glob.os.system('cls') # clear screen
            # show status
            print('Downloaded: ' + str(current_id))
            count_folder =  len(glob.glob(f'{root}/*'))
            print('Total folder: ' + str(count_folder))

        log_record(current_id - 1)


if __name__ == '__main__':
    with open('last_id.txt', 'r') as f:
        try:
            last_id = int(f.read())
        except:
            last_id = None

    if last_id != None:
        main(last_id)

    else:
        main()