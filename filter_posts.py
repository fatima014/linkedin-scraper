import json
import re

with open('results.json', encoding='utf-8') as f:
    posts = json.load(f)

# convert to seconds
def convert_timeframe(timeframe):
    unit = re.sub(r"\d+", "", timeframe)
    value = int(re.findall(r"\d", timeframe)[0]) # get the value without the unit
    if unit == 'h':
        return value * 60 * 60 # convert hours to seconds
    elif unit == 'm':
        return value * 60 
    elif unit == 'd':
        return value * 60 * 60 * 24
    elif unit == 'w':
        return value * 60 * 60 * 24 * 7
    elif unit == 'mo':
        return value * 60 * 60 * 24 * 30
    elif unit == 's':
        return value
    else:
        return None # handle unsupported units
    

def is_within_duration(timeframe, duration):
    duration_in_seconds = convert_timeframe(timeframe)
    if duration_in_seconds is None:
        return False # handle unsupported units
    return duration_in_seconds <= duration

duration = 1 * 7 * 24 * 60 * 60 # weeks in seconds
recent_data = [item for item in posts if is_within_duration(item, duration)]

filtered_posts = {}
with open("filtered_posts.json", 'w', encoding='utf-8') as f:
    for item in recent_data:
        filtered_posts[item] = posts[item]
    json.dump(filtered_posts, f, ensure_ascii=False)
