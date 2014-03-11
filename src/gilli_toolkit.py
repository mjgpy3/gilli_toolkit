#!/usr/bin/env python

from sys import argv
from os import system
import json

class JsonTools(object):
    def are_valid(self, files):
        for file in files:
            self.validate_file(file)

    def validate_file(self, file):
        try:
            with open(file, 'r') as f:
                json.load(f)
            print file, "is valid"
            return True
        except IOError:
            print file, "does not exist"
        except ValueError as ex:
            print file, "has invalid json:"
            print '    ', ex
        return False

    def pretty(self, files):
        for file in files:
            if not self.validate_file(file):
                continue

            with open(file, 'r') as f:
                print eval(json.dumps(f.read(), sort_keys=True, indent=4, separators=(',', ': ')))

class Directory(object):
    def find_and_replace(self, args):
        directory = args[2]
        file_extension = args[3]
        to_replace = args[4]
        replacement = args[5]

        system('find ' + directory + ' -name "*.' + file_extension +'" | xargs sed -i "s/' + to_replace + '/' + replacement + '/g"')

if __name__ == '__main__':
    if argv[1:3] == ['json', 'valid?']:
        print "Validating json for", str(argv[3:]), '\n'
        JsonTools().are_valid(argv[3:])
    elif argv[1:3] == ['json', 'pretty']:
        print "Prettying json", str(argv[3:]), '\n'
        JsonTools().pretty(argv[3:])
    elif argv[1] == 'far':
        print "At '" + argv[2] + "' in files '" + argv[3] + "':", argv[4], " -> ", argv[5]
        Directory().find_and_replace(argv)
    else:
        print "Usage: gilli [options]"
        print "\nJSON:"
        print "    json valid? [files] - validate some json files"
        print "    json pretty [files] - pretty print some json files"
        print "\nDirectories"
        print "    far [dir] [extension] [old] [new] - recursively find and replace"
