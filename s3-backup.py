import rclone
import os
import shutil
from datetime import datetime


def main():

    cfg_path = r'.rclone.conf'

    with open(cfg_path) as f:
        cfg = f.read()
    
    # s3-1:pelican-local-env is source
    rclone.with_config(cfg).copy("s3-1:pelican-local-env", "/tmp/s3-backup", flags=["--transfers=256"])

    archive_name = "s3-backup" + '_' + datetime.now().strftime("%Y.%m.%d.%H-%M") + 'UTC'

    shutil.make_archive(archive_name, 'zip', "/tmp/s3-backup")

    # s3-2:backup is destination
    rclone.with_config(cfg).copy(archive_name + ".zip", "s3-2:backup", flags=["--transfers=256"])


if __name__ == '__main__':

    main()