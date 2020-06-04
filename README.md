# Playstore version tracker

## Deploy to AWS Lambda

TBD. For now, follow this guide: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

## Usage

With no package (use default):

```
$ python3 play.py
No package provided. Fall back to default.
Target package: co.riiid.vida
Current Version: 1.29.10
```

With package:

```
$ python3 play.py --package com.frograms.wplay
Target package: com.frograms.wplay
Current Version: 1.8.59
```
