import glob
from concurrent.futures import ThreadPoolExecutor
import m3u8
import os, math
import requests
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}


def download_ts(url, key, i, tmp='tmp'):
    r = requests.get(url, headers=headers)
    data = r.content
    data = AESDecrypt(data, key=key, iv=key)
    with open(f"{tmp}/{i:0>5d}.ts", "ab") as f:
        f.write(data)
    print(f"\r{i:0>5d}.ts Downloaded", end="  ")


def get_real_url(url):
    playlist = m3u8.load(uri=url, headers=headers)
    return playlist.playlists[0].absolute_uri if len(playlist.playlists) else url


def AESDecrypt(cipher_text, key, iv):
    if key is None:
        return cipher_text
    cipher_text = pad(data_to_pad=cipher_text, block_size=AES.block_size)
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=key)
    cipher_text = aes.decrypt(cipher_text)
    return cipher_text


def download_m3u8_video(url, tempdir='tmp', max_workers=10):
    # __TMP = os.path.join(os.getcwd(), 'tmp', tempdir)
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)

    real_url = get_real_url(url)
    playlist = m3u8.load(uri=real_url, headers=headers)
    if playlist.keys[0]:
        key = requests.get(playlist.keys[-1].uri, headers=headers).content
    else:
        key = None

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        total_duration=0
        for i, seg in enumerate(playlist.segments):
            # total_duration = total_duration + seg.duration
            pool.submit(download_ts, seg.absolute_uri, key, i, tempdir)
        # print(f"total duration is {total_duration}s")

def generate_video(save_name, tempdir, cut_count=0):
    files = glob.glob(f'{tempdir}/*.ts')
    _ = files.sort(reverse = False)
    cut_array = calculate_cut_count(files, cut_count)
    for i, element in enumerate(cut_array):
        with open(f"{save_name}_{i}.mp4", 'wb') as fw:
            for file in element:
                print(f'\rread {file}\r')
                with open(file, 'rb') as fr:
                    fw.write(fr.read())
                    # print(f'\r{file} Merged!Total:{len(files)}\r')
                # os.remove(file)

def calculate_cut_count(files, cut_count=0) -> list:
    result = []
    data_length = len(files)
    if cut_count!=0 and data_length>cut_count:
        piece = math.floor(data_length/cut_count)
        for i in range(cut_count):
            __tmp = []
            if i == cut_count-1:
                __tmp = files[i*piece:]
            else:
                __tmp = files[i*piece:piece*(i+1)]
            result.append(__tmp)
    else:
        result.append(files)
    return result

if __name__ == "__main__":
    # _ = download_m3u8_video('https://vod8.wenshibaowenbei.com/20210628/g4yNLlI7/index.m3u8')
    # _ = generate_video('Walk into the door2.mp4')

    # title
    # _ = download_m3u8_video('https://pili-vod.hsw.cn/hswzhibo_20220422113844_574.m3u8')
    tempdir="tmp/智慧城"
    # m3u8, .ts file download
    _ = download_m3u8_video('https://pili-vod.hsw.cn/hswzhibo_20220422113844_574.m3u8', tempdir=tempdir)
    # merge all *.ts to .mp4
    _ = generate_video('zhihuicheng', tempdir, cut_count=3) #合成的数据可能有问题