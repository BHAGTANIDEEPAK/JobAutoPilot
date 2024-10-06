import requests
import pandas as pd
from bs4 import BeautifulSoup

web_address = str(input("Enter the URL: "))

# request server to get access
path = requests.get(web_address)

soup = BeautifulSoup(path.content, 'html.parser')

data = []
ignore_tags = ['script', 'metadata', 'link', 'style', 'svg', 'path']
# Loop through all tags in the HTML
for tag in soup.find_all(True):  # True gets all tags
    if tag.name in ignore_tags:
        continue

    # Get class and id attribute (or None)
    class_attr = tag.get('class', None)  
    id_attr = tag.get('id', None)

    # Check if both class and id are not None
    if class_attr is not None and id_attr is not None:
        text = tag.get_text(strip=True)  # Get the text of the tag
        data.append({
            'tag': tag.name,
            'class': ' '.join(class_attr) if class_attr else None,
            'id': id_attr,
            'text': text
        })

df = pd.DataFrame(data)
df.to_csv('output.csv')