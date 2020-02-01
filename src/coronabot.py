import requests
import string
import slack
import os


class PartialFormatter(string.Formatter):
    def __init__(self, missing='         0', bad_fmt='0'):
        self.missing, self.bad_fmt = missing, bad_fmt

    def get_field(self, field_name, args, kwargs):
        # Handle a key not found
        try:
            val = super(PartialFormatter, self).get_field(field_name, args, kwargs)
            # Python 3, 'super().get_field(field_name, args, kwargs)' works
        except (KeyError, AttributeError):
            val = None, field_name
        return val

    def format_field(self, value, spec):
        # handle an invalid format
        if value is None:
            return self.missing
        try:
            return super(PartialFormatter, self).format_field(value, spec)
        except ValueError:
            if self.bad_fmt is not None:
                return self.bad_fmt
            else:
                raise


def pretty_printed_string(json_list):
    fmt = PartialFormatter()
    r = "```"
    r += fmt.format("|{:>20}|{:>10}|{:>10}|{:>10}|\n", "Country", "Confirmed", "Deaths", "Recovered")
    r += fmt.format("|{:>20}|{:>10}|{:>10}|{:>10}|\n", "", "", "", "")
    for item in json_list:
        thing = item['attributes']
        r += fmt.format("|{:>20}|{:>10}|{:>10}|{:>10}|\n", thing['Country_Region'], thing['Confirmed'],
                        thing['Deaths'], thing['Recovered'])
    r += "```"
    return r


token = os.environ['SLACK_TOKEN']
channel = os.environ['SLACK_CHANNEL_ID']
if token is None or channel is None:
    print('both a slack token and a channel must be provided')
    exit(1)


arcgisUrl = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=250&cacheHint=true"
result = requests.get(arcgisUrl)
countries = result.json()['features']

# push to slack
client = slack.WebClient(token=token)
client.chat_postMessage(channel=channel, text=pretty_printed_string(countries))

