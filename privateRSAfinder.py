from truffleHog import truffleHog
from json import load
from sys import argv, path

def cleanRSA(rsa):
    #Checking if all strings start with +
    if(all([line[0] == '+' for line in rsa])):
        for i in range(len(rsa)):
            rsa[i] = rsa[i][1:]
    return rsa

git_urls = argv[1:] if len(argv) > 1 else input("\nInsert git urls (seperated with spaces): ").split(' ')

for git_url in git_urls:
    try:
        repoStrings = truffleHog.find_strings(git_url, do_regex=True)
        issues = repoStrings['foundIssues']

        for issue in issues:
            with open(issue) as json_data:
                json = load(json_data)

                if(json['reason'] == 'RSA private key'):
                    print(f'\n{110*"-"}\nRSA private key found in {git_url + ("/" if git_url[-1] != "/" else "") + json["path"]} on branch {json["branch"]}\nCommit hash: {json["commitHash"]}\nDate:{json["date"]}\n')
                    rsaKey = json['diff'].split('-----BEGIN RSA PRIVATE KEY-----')[1].split('-----END RSA PRIVATE KEY-----')[0]
                    rsaKey = cleanRSA(rsaKey.split('\n')[1:-1])
                    rsaKey = ['-----BEGIN RSA PRIVATE KEY-----'] + rsaKey + ['-----END RSA PRIVATE KEY-----']
                    for line in rsaKey:
                        print(line)
    except:
        print(f'\n{110*"-"}\n\n\nCouldn\'t seatch {git_url}.\nMake sure the url is correct and that you have the required permissions.\n')