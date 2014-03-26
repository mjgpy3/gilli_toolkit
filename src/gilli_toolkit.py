#!/usr/bin/env python

from sys import argv
from os import system, popen
import json
import re

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
    def __init__(self, args):
        self.directory = args[2]
        self.file_extension = args[3]
        self.args = args[4:]

    def find_and_replace(self):
        system(self.find_command() + ' | xargs sed -i "s/' + self.args[0] + '/' + self.args[1] + '/g"')

    def find_line_numbers(self):
        findings = [i for i in popen(self.find_command() + ' | xargs grep -Hn "' + self.args[0] + '"' ).read().split() if i]

        results = {}

        for line in findings:
            search_object = re.search('^(.+):(\d+):', line)
            if not search_object: continue

            file, number = search_object.group(1), int(search_object.group(2))

            if file in results:
                results[file].append(number)
            else:
                results[file] = [number]

        for result in results:
            print result, ':', str(results[result])

    def find_command(self):
        return 'find ' + self.directory + ' -name "*.' + self.file_extension +'"'

if __name__ == '__main__':
    if argv[1:3] == ['json', 'valid?']:
        print "Validating json for", str(argv[3:]), '\n'
        JsonTools().are_valid(argv[3:])
    elif argv[1:3] == ['json', 'pretty']:
        print "Prettying json", str(argv[3:]), '\n'
        JsonTools().pretty(argv[3:])
    elif argv[1:2] == ['far']:
        print "At '" + argv[2] + "' in files '" + argv[3] + "':", argv[4], " -> ", argv[5]
        Directory(argv).find_and_replace()
    elif argv[1:2] == ['fl']:
        print "At '" + argv[2] + "' in files '" + argv[3] + "' finding:", argv[4]
        Directory(argv).find_line_numbers()
    else:
        print "Usage: gilli [options]"
        print "\nJSON:"
        print "    json valid? [files] - validate some json files"
        print "    json pretty [files] - pretty print some json files"
        print "\nDirectories:"
        print "    fl [dir] [extension] [text]       - recursively find line numbers containing text"
        print "    far [dir] [extension] [old] [new] - recursively find and replace"

