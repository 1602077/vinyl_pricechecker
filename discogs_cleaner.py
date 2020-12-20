import pandas as pd
from datetime import datetime

pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.expand_frame_repr', False)

df = pd.read_csv('discogs_collection_download.csv')
to_drop = ['Catalog#', 'Label', 'Format', 'Rating', 'Released', 'release_id', 'CollectionFolder', 'Collection Media Condition', 'Collection Sleeve Condition', 'Collection Notes']
df.drop(to_drop, inplace=True, axis=1)
df['Date Added'] = df['Date Added'].str.split(' ').str[0]
df['Date Added'] = df['Date Added'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d'))
df['Date Added'] = df['Date Added'].apply(lambda x: datetime.strftime(x,'%d/%m/%Y'))
df.to_csv('discogs_collection_output.csv', index=False, encoding='utf-8')

