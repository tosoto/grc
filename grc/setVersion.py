import time
import argparse
import os


class ReleaseNumber:

    primary = 0
    secondary = 0

    def __init__(self):
        self.auto_release = str(time.time()).split('.')[0]

    def __str__(self):
        return "%s.%s.%s" % (self.primary, self.secondary, self.auto_release)


parser = argparse.ArgumentParser(description="Creates release file basing on provided numbers and current time")
parser.add_argument('-p', '--path', type=str, help='Path from current directory to version file destination')

args = parser.parse_args()

if args.path is not None:
    version_dir = args.path
else:
    version_dir = ''


release = ReleaseNumber()

try:
    f = open(os.path.join(version_dir, 'VERSION'), 'w')
    print(release)
    f.write(str(release))
    f.close()
except IOError as e:
    print("ERROR: could not write version file\nDetails: %s" % e)