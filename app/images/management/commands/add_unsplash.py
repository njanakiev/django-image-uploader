import os
import pandas as pd
import urllib.request
from django.core.management import BaseCommand
from typing import Any, Optional
from images.models import Image
from django.contrib.auth import get_user_model
from tqdm import tqdm


class Command(BaseCommand):
    help = "Command to load unsplash data"

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('mediapath', type=str)
        parser.add_argument('--n_sample', type=int)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        filepath = options['filepath']
        username = options['username']
        mediapath = options['mediapath']
        n_samples = options.get('n_sample')
        print(f"Running for {filepath} for user {username} {n_samples}")

        User = get_user_model()
        user = User.objects.get(username__exact=username)

        df = pd.read_csv(filepath, delimiter="\t")
        if n_samples:
            df = df.sample(frac=1).head(n_samples)

        # Download images
        df['image_url'] = df['photo_image_url'].apply(
            lambda url: url + "?w=500&fm=jpg")
        df['image'] = df['photo_id'].apply(lambda s: f"{s}.jpg")
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            image_url = row['image_url']
            image_filepath = os.path.join(mediapath, row['image'])
            if not os.path.exists(image_filepath):
                urllib.request.urlretrieve(image_url, image_filepath)

        df = df[['image', 'photo_description',
                 'ai_description', 'photo_submitted_at']]
        df = df.rename(columns={
            'photo_description': 'title',
            'ai_description': 'description',
            'photo_submitted_at': 'created_at'
        })
        df['title'] = df['title'] \
            .fillna('Untitled') \
            .apply(lambda s: s if len(s) < 50 else s[:50] + "...")
        df['created_at'] = pd.to_datetime(
            df['created_at'].str[:19],
            utc=True,
            format="%Y-%m-%d %H:%M:%S")
        df['updated_at'] = df['created_at'].copy()
        df['author_id'] = user.id
        df['description'] = df['description'].fillna('')

        df.reset_index(drop=True, inplace=True)
        # df.index.name = 'id'
        # df = df.reset_index()

        # Image.objects.all().delete()
        items = [Image(**item)
                 for i, item in enumerate(df.to_dict(orient="records"))]
        Image.objects.bulk_create(items)
