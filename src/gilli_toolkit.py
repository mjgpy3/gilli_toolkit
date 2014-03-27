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
                print json.dumps(f.read(), sort_keys=True, indent=4, separators=(',', ': '))

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

class Git(object):
    def __init__(self, args):
        self.command = args[2]
        self.args = args[3:]

    def add_all(self):
        system('git add -A')

    def commit_with_message(self):
        system('git commit -m "' + self.args[0] + '"')

    def list_all_branches(self):
        system('git branch -a')

    def show_current_branch(self):
        system('git rev-parse --abbrev-ref HEAD')

    def status(self):
        system('git status')

    def execute_command(self):
        if self.command == 'a':
            self.add_all()
        elif self.command == 'c':
            self.commit_with_message()
        elif self.command == 'ac':
            self.add_all()
            self.commit_with_message()
        elif self.command == 'ba':
            self.list_all_branches()
        elif self.command == 'bc':
            self.show_current_branch()
        elif self.command == 's':
            self.status()
        else:
            print "Unknown git command '" + self.command +"'"

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
    elif argv[1:2] == ['g']:
        Git(argv).execute_command()
    else:
        print "Usage: gilli [options]"
        print "\nJSON:"
        print "    json valid? [files] - validate some json files"
        print "    json pretty [files] - pretty print some json files"
        print "\nDirectories:"
        print "    fl [dir] [extension] [text]       - recursively find line numbers containing text"
        print "    far [dir] [extension] [old] [new] - recursively find and replace"
        print "\nGit:"
        print "    g a            - git add -A"
        print "    g c [message]  - git commit -m \"[message]\""
        print "    g ac [message] - git add -A; git commit -m \"[message]\""
        print "    g ba           - git branch -a"
        print "    g bc           - git rev-parse --abbrev-ref HEAD (show current branch)"
        print "    g s            - git status"
        print

