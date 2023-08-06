# github-scrape

### About

Scrapes github pages for a specified user,
displays a report about the user's current account status.

The report contains:
- [x] Number of followers
- [x] Number of users being followed
- [x] Number of users following but not following back
- [x] Opposite of '3.'
- [x] Check number of repositories
- [x] List repositories


## Installation
For first time installation:
'''
pip install github-scrape
'''

For recurring installation/update:
'''
pip install github-scrape --upgrade
'''

## Usage

To use the package, you have to import using any of the following:

##### Step 1:

```
from akinyeleib import reader
from akinyeleib import reader as r
```

##### Step 2:

Create an object of "Github" class
It's constructor accepts the github username as an argument
For this example, we would use username "akinyeleib"
`user1 = reader.GitHub("akinyeleib")`

Or:

`user1 = r.GitHub("akinyeleib")`

##### Step 3:

Use the object to access several methods from the class
Some of the available methods include:

```
print(f"Followers: {user1.getFollowers()}")
print(f"Following: {user1.getFollowing()}")
print("FollowersNotFollowing: " + user1.getFollowersNotFollowing())
print("FollowingNotFollowers: " + user1.getFollowingNotFollowers())
print(user1.getDetails())
```
Other methods include:
getFollowing, getFollowers, getRepos

### Thank you.
