import os
import subprocess
from celery import shared_task
# from subtitle_video_finder.settings import BASE_DIR
from .models import Video
import pysrt,os,pysrt,boto3
from django.conf import settings


def extract_keywords(text):

    # Run ccextractor command and capture the output
    ccextractor_command = ['ccextractor', '-quiet', '-in=txt', '-']
    process = subprocess.Popen(ccextractor_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    stdout, stderr = process.communicate(input=text)

    # Process the extracted keywords
    keywords = []
    if process.returncode == 0:
        # Split the output by newline character to get individual keywords
        keywords = stdout.strip().split('\n')
    else:
        # Handle any error during ccextractor execution
        print(f'ccextractor error: {stderr}')

    return keywords

@shared_task
def process_video(video_id):
    # Retrieve the Video object using the video_id
    video = Video.objects.get(id=video_id)
    ccextractor_path = os.path.join(settings.BASE_DIR, 'ccextractor', 'ccextractorwinfull.exe') # Path to ccextractor binary
    video_path = os.path.join(settings.BASE_DIR, video.s3_key)  # Path to the uploaded video file
    output_path = os.path.join(settings.BASE_DIR, 'output.srt')  # Path to save the extracted subtitle file
    command = [ccextractor_path, '-out=srt', '-o', output_path, video_path]
    subprocess.run(command, check=True)

    # Store the subtitles keywords in DynamoDB
    subtitle_file_path = output_path
    subs = pysrt.open(subtitle_file_path)

    # Extract keywords and store them in DynamoDB
    for sub in subs:
        text = sub.text
        # Extract relevant keywords from the subtitle text
        keywords = extract_keywords(text)

        table_name = 'Subtitles' # Name of your DynamoDB table
        num_keywords_processed = 0

        # Store the keywords in DynamoDB
        for keyword in keywords:
            settings.dynamodb_client.put_item(
                TableName=table_name,
                Item={
                    'keyword': {'S': keyword},
                    'video_id': {'N': str(video.id)},
                    'timestamp': {'N': str(sub.start.total_seconds())},
                }
            )
            num_keywords_processed += 1

# Check if subtitles were stored in DynamoDB
    expected_num_keywords = len(subs) * len(keywords)
    if num_keywords_processed == expected_num_keywords:
        print("Subtitles were successfully stored in DynamoDB.")
    else:
        print("Some subtitles may not have been stored in DynamoDB. Please check the process_video task.")







