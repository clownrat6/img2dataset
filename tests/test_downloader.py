import shutil
from fixtures import setup_fixtures
from img2dataset.resizer import Resizer
from img2dataset.writer import FilesSampleWriter
from img2dataset.downloader import Downloader

import os
import pandas as pd


def test_downloader(tmp_path):
    test_folder = str(tmp_path)
    test_list = setup_fixtures(count=5)
    image_folder_name = os.path.join(test_folder, "images")

    os.mkdir(image_folder_name)

    resizer = Resizer(256, "border", False)
    writer = FilesSampleWriter

    downloader = Downloader(
        writer,
        resizer,
        thread_count=32,
        save_caption=True,
        extract_exif=True,
        output_folder=image_folder_name,
        column_list=["caption", "url"],
        timeout=10,
        number_sample_per_shard=10,
        oom_shard_count=5,
        compute_md5=True,
    )

    tmp_file = os.path.join(test_folder, "test_list.feather")
    df = pd.DataFrame(test_list, columns=["caption", "url"])
    df.to_feather(tmp_file)

    downloader((0, tmp_file))

    assert len(os.listdir(image_folder_name + "/00000")) == 3 * len(test_list)
