import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.s3 import S3Path


class S3Check(BaseModel):
    path: S3Path


@pytest.mark.parametrize(
    'raw,bucket,key,last_key',
    [
        (
            's3://my-data-bucket/2023/08/29/sales-report.csv',
            'my-data-bucket',
            '2023/08/29/sales-report.csv',
            'sales-report.csv',
        ),
        (
            's3://logs-bucket/app-logs/production/2024/07/01/application-log.txt',
            'logs-bucket',
            'app-logs/production/2024/07/01/application-log.txt',
            'application-log.txt',
        ),
        (
            's3://backup-storage/user_data/john_doe/photos/photo-2024-08-15.jpg',
            'backup-storage',
            'user_data/john_doe/photos/photo-2024-08-15.jpg',
            'photo-2024-08-15.jpg',
        ),
        (
            's3://analytics-bucket/weekly-reports/Q3/2023/week-35-summary.pdf',
            'analytics-bucket',
            'weekly-reports/Q3/2023/week-35-summary.pdf',
            'week-35-summary.pdf',
        ),
        (
            's3://project-data/docs/presentations/quarterly_review.pptx',
            'project-data',
            'docs/presentations/quarterly_review.pptx',
            'quarterly_review.pptx',
        ),
        (
            's3://my-music-archive/genres/rock/2024/favorite-songs.mp3',
            'my-music-archive',
            'genres/rock/2024/favorite-songs.mp3',
            'favorite-songs.mp3',
        ),
        (
            's3://video-uploads/movies/2024/03/action/thriller/movie-trailer.mp4',
            'video-uploads',
            'movies/2024/03/action/thriller/movie-trailer.mp4',
            'movie-trailer.mp4',
        ),
        (
            's3://company-files/legal/contracts/contract-2023-09-01.pdf',
            'company-files',
            'legal/contracts/contract-2023-09-01.pdf',
            'contract-2023-09-01.pdf',
        ),
        (
            's3://dev-environment/source-code/release_v1.0.2.zip',
            'dev-environment',
            'source-code/release_v1.0.2.zip',
            'release_v1.0.2.zip',
        ),
        (
            's3://public-bucket/open-data/geojson/maps/city_boundaries.geojson',
            'public-bucket',
            'open-data/geojson/maps/city_boundaries.geojson',
            'city_boundaries.geojson',
        ),
        (
            's3://image-storage/2024/portfolio/shoots/wedding/couple_photo_12.jpg',
            'image-storage',
            '2024/portfolio/shoots/wedding/couple_photo_12.jpg',
            'couple_photo_12.jpg',
        ),
        (
            's3://finance-data/reports/2024/Q2/income_statement.xlsx',
            'finance-data',
            'reports/2024/Q2/income_statement.xlsx',
            'income_statement.xlsx',
        ),
        (
            's3://training-data/nlp/corpora/english/2023/text_corpus.txt',
            'training-data',
            'nlp/corpora/english/2023/text_corpus.txt',
            'text_corpus.txt',
        ),
        (
            's3://ecommerce-backup/2024/transactions/august/orders_2024_08_28.csv',
            'ecommerce-backup',
            '2024/transactions/august/orders_2024_08_28.csv',
            'orders_2024_08_28.csv',
        ),
        (
            's3://gaming-assets/3d_models/characters/hero/model_v5.obj',
            'gaming-assets',
            '3d_models/characters/hero/model_v5.obj',
            'model_v5.obj',
        ),
        (
            's3://iot-sensor-data/2024/temperature_sensors/sensor_42_readings.csv',
            'iot-sensor-data',
            '2024/temperature_sensors/sensor_42_readings.csv',
            'sensor_42_readings.csv',
        ),
        (
            's3://user-uploads/avatars/user123/avatar_2024_08_29.png',
            'user-uploads',
            'avatars/user123/avatar_2024_08_29.png',
            'avatar_2024_08_29.png',
        ),
        (
            's3://media-library/podcasts/2023/episode_45.mp3',
            'media-library',
            'podcasts/2023/episode_45.mp3',
            'episode_45.mp3',
        ),
        (
            's3://logs-bucket/security/firewall-logs/2024/08/failed_attempts.log',
            'logs-bucket',
            'security/firewall-logs/2024/08/failed_attempts.log',
            'failed_attempts.log',
        ),
        (
            's3://data-warehouse/financials/quarterly/2024/Q1/profit_loss.csv',
            'data-warehouse',
            'financials/quarterly/2024/Q1/profit_loss.csv',
            'profit_loss.csv',
        ),
        (
            's3://data-warehouse/financials/quarterly/2024/Q1',
            'data-warehouse',
            'financials/quarterly/2024/Q1',
            'Q1',
        ),
    ],
)
def test_s3(raw: str, bucket: str, key: str, last_key: str):
    model = S3Check(path=raw)
    assert model.path == S3Path(raw)
    assert model.path.bucket == bucket
    assert model.path.key == key
    assert model.path.last_key == last_key


def test_wrong_s3():
    with pytest.raises(ValidationError):
        S3Check(path='s3/ok')
