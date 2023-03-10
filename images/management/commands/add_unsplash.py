from django.core.management import BaseCommand
from typing import Any, Optional
import pandas as pd
from images.models import Image
from django.conf import settings
from sqlalchemy import create_engine
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

        postgres_user     = settings.DATABASES['default']['USER']
        postgres_password = settings.DATABASES['default']['PASSWORD']
        postgres_host     = settings.DATABASES['default']['HOST']
        postgres_port     = settings.DATABASES['default']['PORT']
        postgres_db       = settings.DATABASES['default']['NAME']
        engine = create_engine(
            f'postgresql://{postgres_user}:{postgres_password}@' \
            f'{postgres_host}:{postgres_port}/{postgres_db}')

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
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['updated_at'] = df['created_at'].copy()
        df['image'] = df['image'].apply(lambda s: f"{s}.jpg")
        df['author_id'] = user.id
        df['id'] = df.index

        df.head(200).to_sql(
            Image._meta.db_table,
            if_exists='replace',
            con=engine,
            index=False
        )
