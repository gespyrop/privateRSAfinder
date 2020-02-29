from truffleHog import truffleHog
from json import load
from requests import get
from random import randint

# Gets 100 random repositories from GitHub API
def getRandomRepositories():
    repos = []
    url = f'https://api.github.com/repositories?since={randint(1,244000000)}'
    data = get(url).json()
    for repo in data:
        repos.append(repo['html_url'])

    return repos

# Checks if all lines of the key start with '+' or '-' and removes it
def cleanRSA(rsa):
    if(all([ (line[0] == '+' or line[0] == '-') for line in rsa ])):
        for i in range(len(rsa)):
            rsa[i] = rsa[i][1:]
    return rsa

# Checks all the repositories in a list for private RSA keys
def checkRepositories(git_urls):
    for git_url in git_urls:
        try:
            print(f'\n{110*"-"}\n\nChecking {git_url}\n')
            repoStrings = truffleHog.find_strings(git_url, do_regex=True)
            issues = repoStrings['foundIssues']

            keysFound = 0

            for issue in issues:
                with open(issue) as json_data:
                    json = load(json_data)

                    if(json['reason'] == 'RSA private key'):
                        keysFound += 1
                        print(f'\nRSA private key found in {git_url + ("/" if git_url[-1] != "/" else "") + json["path"]} on branch {json["branch"]}\nCommit hash: {json["commitHash"]}\nDate:{json["date"]}\n')
                        rsaKey = json['diff'].split('-----BEGIN RSA PRIVATE KEY-----')[1].split('-----END RSA PRIVATE KEY-----')[0]
                        rsaKey = cleanRSA(rsaKey.split('\n')[1:-1])
                        rsaKey = ['-----BEGIN RSA PRIVATE KEY-----'] + rsaKey + ['-----END RSA PRIVATE KEY-----']
                        
                        # Printing the key to the console
                        for line in rsaKey:
                            print(line)
                        
                        # Saving the key to a file
                        repositoryName = git_url.split('/')[-1]
                        with open(f'keys/{repositoryName}_private_RSA_{keysFound}.txt', 'a') as file:
                            file.write('\n'.join(rsaKey))

            if not keysFound:
                print('\nNo private RSA keys found.\n')

        except:
            print(f'\n{110*"-"}\n\n\nCouldn\'t seatch {git_url}.\nMake sure the url is correct and that you have the required permissions.\n')



if __name__=='__main__':
    print('\nGetting random repositories...\n')
    checkRepositories(getRandomRepositories())