# utils.py
from config import ALLOWED_EXTENSIONS
import argparse

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_args():
    """parse the command line args

    Returns:
        args: a namespace object including args
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--mysql_pwd',
        help='the mysql root password',
        default="11235813"
    )
    parser.add_argument(
        '--db_name',
        help='which database to use',
        default="appDB"
    )

    args = parser.parse_args()
    return args