from truffleHog import truffleHog
from json import load
from sys import argv

repoStrings = truffleHog.find_strings(argv[1] if len(argv) > 1 else input("Insert git url: "))
issues = repoStrings['foundIssues']

for issue in issues:
    with open(issue) as json_data:
        json = load(json_data)

        for s in json['stringsFound']:
            print(s)
