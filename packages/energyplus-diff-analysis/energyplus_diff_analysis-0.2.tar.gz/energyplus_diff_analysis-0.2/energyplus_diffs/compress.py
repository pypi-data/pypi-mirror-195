import os
import shutil
import sys


def make_archive(source, destination):
    """https://stackoverflow.com/a/50381223"""

    base = os.path.basename(destination)
    name = base.split('.')[0]
    archive_format = base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    shutil.make_archive(name, archive_format, archive_from, archive_to)
    shutil.move('%s.%s' % (name, archive_format), destination)


if __name__ == "__main__":
    make_archive(sys.argv[1], sys.argv[2])
