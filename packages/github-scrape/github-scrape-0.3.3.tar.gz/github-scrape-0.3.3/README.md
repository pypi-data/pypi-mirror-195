# github-scrape

### About

Scrapes github pages for a specified user,
displays a report about the user's current account status.

The report contains:
- [x] Number of followers
- [x] Number of users being followed
- [x] Number of users followed but not following back
- [x] Number of followers not followed
- [x] Check number of repositories
- [x] List available repositories (public)


## Installation
For first time installation:

```
pip install github-scrape
```

For recurring installation/update:

```
pip install github-scrape --upgrade
```

## Usage

To use the package, you have to import it using any of the following:

##### Step 1:

```
from akinyeleib import github_scrape
from akinyeleib import github_scrape as r
```

##### Step 2:

Create an object of "Github" class
It's constructor accepts the github username as an argument
For this example, we would use username "akinyeleib"

`user1 = reader.GitHub("akinyeleib")`

Or:

`user1 = r.GitHub("akinyeleib")`

##### Step 3:

Use the object to access several methods from the class.

Some of the available methods include:

```
print(f"Followers: {user1.getFollowers()}")
print(f"Following: {user1.getFollowing()}")
print("FollowersNotFollowing: " + user1.getFollowersNotFollowing())
print("FollowingNotFollowers: " + user1.getFollowingNotFollowers())
print(user1.getDetails())
```

Other methods include:

```
getRepos()
getDetails()
getUserName()
getFollowing()
getFollowers()
getFollowersCount()
getFollowingCount()
getFollowingNotFollowers()
getFollowersNotFollowing()
```

## Demo

```

>>> from akinyeleib import github_scrape as r
>>> user1 = r.GitHub("Akinyeleib")
Account found for user: Akinyeleib
Akinyeleib has 17 repositories
Akinyeleib has 32 followers
Akinyeleib is following 35 user(s)
Akinyeleib has 10 user(s) not following back
Akinyeleib is not following 7 user(s) back
>>> user1repo = user1.getRepos()
>>> user1repo
['Lawson-To-Do-List', 'Todo-List', 'FlutterNewsApp', 'html-tic-tac-toe', 'nike-sneakers-store-app', 'tic_tac_toe', 'quiz-stopwatch', 'StopWatch', 'Projects', 'HangMan-Java', 'Therapy', 'CBTApp', 'Pedek', 'ChamsMobile', 'Data-Structures-and-Algorithms', 'Bounce', 'learning-python-2896241']
>>> user1.getFollowers()
['1AMTEDDY', 'DJTOHBEX', 'Sammygee0110', 'Paulokla', 'Stevixent', 'AyodejiOmole', 'eni01', 'Ayomidefln', 'Tobigr03', 'Sagaciousprince', 'Goldenson23', 'codetech18', 'Chimajunior', 'Vgod0', 'Lekan128', 'SamAkiode', 'crisovas', 'sofiaunnie', 'KingJoker101', 'Opeyemi86', 'Tinkapaul', 'Chee123-proj', 'TubiOb', 'DeekerD', 'lawson1000', 'xDAREY', 'lolakin', 'ayetolusamuel', 'Joshokelola', 'Ogizzy', 'imoleBytes', 'menabaddo']
>>> user1.getFollowing()
['Tinkapaul', 'Tobigr03', 'Akinsanmi23', 'Olaitanbosun', 'Themarv77', 'Oayanfe', 'Vgod0', 'Chimajunior', 'crisovas', 'papillo1', 'sofiaunnie', 'Paulokla', 'KingJoker101', 'Abdullateef1000', 'Sammygee0110', 'Chee123-proj', 'TubiOb', 'xDAREY', 'lawson1000', 'Stevixent', 'AyodejiOmole', 'codetech18', 'ochinawata01', 'Shittu-ayomide', 'SamAkiode', 'lolakin', 'eni01', 'ayetolusamuel', 'Ogizzy', 'Joshokelola', 'Mastersam07', 'menabaddo', 'Princeadeola', 'imoleBytes', 'DeekerD']
>>>

```

### Thank you.
