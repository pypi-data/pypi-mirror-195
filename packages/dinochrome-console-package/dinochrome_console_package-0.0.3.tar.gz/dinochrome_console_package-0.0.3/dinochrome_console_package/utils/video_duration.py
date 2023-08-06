import subprocess
import os


def get_file_list():
    file_list = []
    tree = os.walk(os.getcwd())

    for i in tree:
        for j in i[2]:
            if j.split(".")[-1] == "mp4":
                file_list.append(os.path.join(i[0], j))
    return file_list


def get_length(filename):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return float(result.stdout)

# file_length_list = [get_length(i) for i in tqdm(get_file_list())]
# total_video_duration = (sum(file_length_list))
#
# print(str(datetime.timedelta(seconds=int(total_video_duration))))
