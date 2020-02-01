# CoronaBot ![Language Badge](https://img.shields.io/badge/Language-Python-blue.svg) ![License Badge](https://img.shields.io/badge/License-MIT-blue.svg) 

## What is CoronaBot?
CoronaBot is a simple python slack bot for informing users about the corona virus. It's based on a Go lang bot created by [Diego Siqueira](https://github.com/DiSiqueira/coronabot). I found his initial version had some limitations that I wanted to address but I'm not a Go programmer so I created a simple version in Python. Large parts of this readme are copied from his.

## Where does the data come from?
Data comes from ArcGIS REST API.

# How to use this image
Start an instance 

```bash 
$ docker run -e SLACK_TOKEN=xoxp-1111111-22222-3333-444 -e SLACK_CHANNEL_ID=C5P11AABB22 ryyaan2004/coronabot
```

## Environment Variables

*SLACK_TOKEN*

Slack token with permissions to post on a channel. Hot to generate a Slack Token: https://slack.com/help/articles/215770388

*SLACK_CHANNEL_ID*

Slack channel id can be found as the last argument on the channel url. Example channel url: https://app.slack.com/client/T0LC9999F/C5P111QZB5 Example channel id: C5P111QZB5

## License

The MIT License (MIT)

Copyright (c) 2020 ryyaan2004

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.