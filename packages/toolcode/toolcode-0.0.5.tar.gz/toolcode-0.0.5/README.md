# toolcode

**toolcode** is a simple, toolcode supporting facebook

```python
>>> from toolcode import toolcode
>>> getprofile=toolcode.checkfb(cookie)
>>>getprofile.idfb
>>> getprofile.namefb
nguyen van ky deptrai
1000383493047
>>> like = toolcode.fblike(idpost,cookie)
>>> like.url
https://mbasic.facebook.com/*****
>>> follow=toolcode.fbfollow(idprofile,cookie)
>>> follow.mess
https://mbasic.facebook.com/*****
>>> react=toolcode.fbreact(idpost,cookie,type)
...
```
type can be love , haha ​​, sad , care , angry , wow
except fbreact, other functions stop like fblike and follow

it helps you like photos uploaded to facebook and some other functions like react, follow, group, like page, create fake name, countdown

and it depends on the required module, the usage of the request is still the same, if you have not installed the required module, the tool code
will automatically install it, the toolcode is quite suitable for those of you who make software and tools on facebook



## Installing toolcode and Supported Versions

toolcode is available on PyPI:

```console
$ python -m pip install toolcode
```

Requests officially supports Python 3.7+.

## features in tool code
- toolcode.fbfriend(idprofile,cookie)
- toolcode.fblike(idpost,cookie)
- toolcode.fbreact(idpost,cookie,type)
- toolcode.fbpage(idpage,cookie)
- toocode.fbgroup(idgroup,cookie)
- toolcode.fbfollow(idprofile,cookie)
- toolcode.checkfb(cookie)
- toolcode.fakename(2)
- toolcode.wait('',10,'')

## group toolcode
https://t.me/+BfXb55fR3sZjNGNl
