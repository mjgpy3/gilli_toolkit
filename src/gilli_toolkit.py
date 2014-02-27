#!/usr/bin/env python

from sys import argv
import json

class JsonTools(object):
    def are_valid(self, files):
        for file in files:
            try:
                with open(file, 'r') as f:
                    json.load(f)
                print file, "is valid"
            except IOError:
                print file, "does not exist"
            except ValueError as ex:
                print file, "has invalid json:"
                print '    ', ex

if __name__ == '__main__':
    if argv[1:3] == ['json', 'valid?']:
        print "Validating json for", str(argv[3:]), '\n'
        JsonTools().are_valid(argv[3:])
    else:
        print "Usage: gilli [options]"
        print "    json valid? [files]"
