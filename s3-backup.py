import rclone
import os
def main():

    cfg_path = r'.rclone.conf'

    with open(cfg_path) as f:
        cfg = f.read()

    result = rclone.with_config(cfg).copy("minio:pelican-local-env", "minio:123/test2", flags=["--transfers=256"])

if __name__ == '__main__':

    main()