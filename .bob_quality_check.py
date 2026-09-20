import json, sys

resources = json.load(open('data/resources.json', encoding='utf-8'))
channels = json.load(open('data/youtube_channels.json', encoding='utf-8'))

# Check data integrity
urls = [r['url'] for r in resources]
url_dupes = [u for u in set(urls) if urls.count(u) > 1]
ids = [r['id'] for r in resources]
id_dupes = [i for i in set(ids) if ids.count(i) > 1]

# Valid tags/types
VALID_TAGS = ["Free","Paid","Government","Certificate","YouTube","Practice","Projects",
              "Beginner","Intermediate","Advanced","India","Global","Official"]
VALID_TYPES = ["Video","Course","Article","Practice","Project","Platform","Channel",
               "Tool","Notes","Lab","Reference","Website"]

bad_tags = [(r['id'], t) for r in resources for t in r.get('tags',[]) if t not in VALID_TAGS]
bad_types = [(r['id'], r.get('type')) for r in resources if r.get('type') not in VALID_TYPES]

# Channel integrity
ch_urls = [c['url'] for c in channels]
ch_url_dupes = [u for u in set(ch_urls) if ch_urls.count(u) > 1]
ch_ids = [c['id'] for c in channels]
ch_id_dupes = [i for i in set(ch_ids) if ch_ids.count(i) > 1]

required_res = {'id','title','url','type','tags','description'}
missing_fields = [r.get('id','?') for r in resources if not required_res.issubset(r.keys())]

required_ch = {'id','name','url','category','tags','type','description','skills'}
missing_ch_fields = [c.get('id','?') for c in channels if not required_ch.issubset(c.keys())]

print('=== DATA QUALITY REPORT ===')
print(f'Resources: {len(resources)}')
print(f'Channels: {len(channels)}')
print(f'URL dupes (resources): {len(url_dupes)}')
print(f'ID dupes (resources): {len(id_dupes)}')
print(f'Channel URL dupes: {len(ch_url_dupes)}')
print(f'Channel ID dupes: {len(ch_id_dupes)}')
print(f'Bad tags: {len(bad_tags)}')
print(f'Bad types: {len(bad_types)}')
print(f'Resources missing required fields: {missing_fields}')
print(f'Channels missing required fields: {missing_ch_fields}')

if url_dupes: print('URL DUPES:', url_dupes)
if id_dupes: print('ID DUPES:', id_dupes)
if bad_tags: print('BAD TAGS:', bad_tags[:5])
if bad_types: print('BAD TYPES:', bad_types[:5])

print()
print('All checks passed:', not any([url_dupes, id_dupes, ch_url_dupes, ch_id_dupes,
                                      bad_tags, bad_types, missing_fields, missing_ch_fields]))
