import collections

import requests
import string
import slack
import os
from flask import Flask


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


def ratio(str_numerator, str_denominator):
    try:
        return int(str_numerator) / int(str_denominator)
    except TypeError:
        return 'NaN'
    except ZeroDivisionError:
        return 'NaN'


def percentage(num):
    try:
        return "{0:.0%}".format(num)
    except ValueError:
        return 'NaN'


def accumulate(accumulator, json_entry):
    accumulator['Confirmed'] += int(json_entry['Confirmed'])
    accumulator['Deaths'] += int(json_entry['Deaths'])
    accumulator['Recovered'] += int(json_entry['Recovered'])


def country_table_string(json_list, accumulator):
    fmt = PartialFormatter()
    r = "```"
    r += fmt.format("|{:>25}|{:>10}|{:>7}|{:>10}|{:>5}|{:>5}|\n", "Country", "Confirmed", "Deaths", "Recovered", "D/C"
                    , "R/C")
    r += fmt.format("|{:>25}|{:>10}|{:>7}|{:>10}|{:>5}|{:>5}|\n", "", "", "", "", "", "")
    for item in json_list:
        thing = item['attributes']
        accumulate(accumulator, thing)
        deaths_to_confirmed = ratio(thing['Deaths'], thing['Confirmed'])
        recovered_to_confirmed = ratio(thing['Recovered'], thing['Confirmed'])
        r += fmt.format("|{:>25}|{:>10}|{:>7}|{:>10}|{:>5}|{:>5}|\n", thing['Country_Region'], thing['Confirmed'],
                        thing['Deaths'], thing['Recovered'], percentage(deaths_to_confirmed),
                        percentage(recovered_to_confirmed))
    r += "```"
    return r


def summary_table_string(accumulator):
    fmt = PartialFormatter()
    deaths_to_confirmed = ratio(accumulator['Deaths'], accumulator['Confirmed'])
    recovered_to_confirmed = ratio(accumulator['Recovered'], accumulator['Confirmed'])
    r = "```\n"
    r += fmt.format("|{:>25}|{:>10}|{:>7}|{:>10}|{:>5}|{:>5}|\n", "Country", "Confirmed", "Deaths", "Recovered", "D/C"
                    , "R/C")
    r += fmt.format("|{:>25}|{:>10}|{:>7}|{:>10}|{:>5}|{:>5}|\n", "", "", "", "", "", "")
    r += fmt.format("|{:>25}|{:>10}|{:>7}|{:>10}|{:>5}|{:>5}|\n", "Worldwide", accumulator['Confirmed']
                    , accumulator['Deaths'], accumulator['Recovered'], percentage(deaths_to_confirmed)
                    , percentage(recovered_to_confirmed))
    r += "```\n"
    r += jhu_url()
    return r


def chunk(lst, size):
    return (lst[pos:pos + size] for pos in range(0, len(lst), size))


def jhu_url():
    """Returns the interactive web dashboard created/maintained by Johns Hopkins University"""
    url = "https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6"
    return "For the Johns Hopkins University interactive dashboard visit this link: {}".format(url)


app = Flask(__name__)


@app.route("/")
def corona():
    token = os.environ['SLACK_TOKEN']
    channel = os.environ['SLACK_CHANNEL_ID']
    if token is None or channel is None:
        print('both a slack token and a channel must be provided')
        exit(1)

    arcgisUrl = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=250&cacheHint=true"
    result = requests.get(arcgisUrl)
    countries = result.json()['features']
    totals = collections.Counter()
    limit = os.environ.get('LIMIT')
    client = slack.WebClient(token=token)

    if limit is not None:
        limit = int(limit)
        countries = countries[:limit]
        client.chat_postMessage(channel=channel, text='Top {} countries by confirmed cases'.format(limit))

    # push to slack
    for group in chunk(countries, 50):
        client.chat_postMessage(channel=channel, text=country_table_string(group, totals))

    client.chat_postMessage(channel=channel, text=summary_table_string(totals))
    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['PORT'])

