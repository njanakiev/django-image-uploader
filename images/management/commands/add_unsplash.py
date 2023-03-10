from django.core.management import BaseCommand
from typing import Any, Optional
import pandas as pd
from images.models import Image
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Command to load unsplash data"
    
    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('--n_sample', type=int)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        filepath = options['filepath']
        username = options['username']
        n_samples = options.get('n_sample')
        print(f"Running for {filepath} for user {username} {n_samples}")

        User = get_user_model()
        user = User.objects.get(username__exact=username)


        df = pd.read_csv(filepath, delimiter="\t")
        if n_samples:
            df = df.sample(frac=1).head(n_samples)

        df = df[['photo_id', 'photo_description', 'ai_description', 'photo_submitted_at']]
        df = df.rename(columns={
            'photo_id': 'image',
            'photo_description': 'title',
            'ai_description': 'description',
            'photo_submitted_at': 'created_at'
        })
        df = df.dropna(subset=['title'])
        df['created_at'] = pd.to_datetime(df['created_at'], utc=True)
        df['updated_at'] = df['created_at'].copy()
        df['image'] = df['image'].apply(lambda s: f"{s}.jpg")
        df['author_id'] = user.id
        df['description'] = df['description'].fillna('')
        df['title'] = df['title'].str[:200]

        df.reset_index(drop=True, inplace=True)
        #df.index.name = 'id'
        #df = df.reset_index()

        Image.objects.all().delete()
        items = [Image(**item) for i, item in enumerate(df.to_dict(orient="records"))]
        Image.objects.bulk_create(items)
