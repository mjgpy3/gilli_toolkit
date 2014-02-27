#!/usr/bin/env python

from sys import argv
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

if __name__ == '__main__':
    if argv[1:3] == ['json', 'valid?']:
        print "Validating json for", str(argv[3:]), '\n'
        JsonTools().are_valid(argv[3:])
    elif argv[1:3] == ['json', 'pretty']:
        print "Prettying json", str(argv[3:]), '\n'
        JsonTools().pretty(argv[3:])
    else:
        print "Usage: gilli [options]"
        print "\nJSON:"
        print "    json valid? [files] - validate some json files"
        print "    json pretty [files] - pretty print some json files"
