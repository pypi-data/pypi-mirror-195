# E620py

E620py is a python library for interacting with the e621 api designed to be simple and easy to use.

Here is an example of fetching a single post:
```python
>>> import e620py
>>> post = e620py.E6get().post_get("order:score", fetch_all=False, fetch_count=1)
>>> print(post[0].m_id)
2848682
```
Most functions have doc strings so its easy to quickly see how a function works without having to understand the spaghetti code 💀.
I will try and implement all of the main features of the e621 api and possibly implement some of the undocumented endpoints.

## Features
  Post:
  + Fetching
  + Uploading (uploading a file directly does not work)
  + Editing
  + Voting
  + Favorite and unfavorite
  + Downloading

  Pool:
  + Fetching (only one page at a time for now)
  + Creating
  + Editing
  + Downloading

 Note:
 The download functions do not have doc strings yet
