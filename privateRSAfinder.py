from truffleHog import truffleHog
from json import load
from sys import argv, path

git_url = argv[1] if len(argv) > 1 else input("\nInsert git url: ")
repoStrings = truffleHog.find_strings(git_url, do_regex=True)
issues = repoStrings['foundIssues']

def cleanRSA(rsa):
    #Checking if all strings start with +
    if(all([line[0] == '+' for line in rsa])):
        for i in range(len(rsa)):
            rsa[i] = rsa[i][1:]
    return rsa

for issue in issues:
    with open(issue) as json_data:
        json = load(json_data)

        if(json['reason'] == 'RSA private key'):
            print(f'\n{110*"-"}\nRSA private key found in {git_url + ("/" if git_url[-1] != "/" else "") + json["path"]} on branch {json["branch"]}\nCommit hash: {json["commitHash"]}\nDate:{json["date"]}\n')
            for line in cleanRSA(json['diff'].split("\n")[1:-1]):
                print(line)
