from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings  # Import settings

from .models import SubtitleKeyword, Video
from .tasks import process_video
import boto3

class UploadVideoView(View):
    def get(self, request):
        # Render the upload form
        return render(request, 'upload_video.html')

    def post(self, request):
        title = request.POST.get('title', '')
        video_file = request.FILES.get('video_file', None)

        if title and video_file:
            # Upload the video file to S3
            s3_key = f'videos/{video_file.name}'
            settings.S3_CLIENT.upload_fileobj(video_file, settings.AWS_STORAGE_BUCKET_NAME, s3_key)

            # Create a new Video object and save it to the database
            video = Video.objects.create(title=title, s3_key=s3_key)
            video.save()

            # Perform any additional video processing or parsing here
            process_video.delay(video.id)

            return redirect('upload')  # Redirect to the upload page or another URL
        else:
            error_message = 'Please provide a title and upload a video file.'
            return render(request, 'upload_video.html', {'error_message': error_message})

class SearchView(View):
    def get(self, request):
        return render(request, 'search.html')

    def post(self, request):
        keyword = request.POST.get('keyword', '')

        if keyword:
            # # Query the SubtitleKeyword model using DynamoDB
            # dynamodb_client = boto3.client('dynamodb', aws_access_key_id='AKIASFFY7HJZBYVHOZ4U', aws_secret_access_key='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', region_name='ap-south-1')
            response = settings.dynamodb_client.scan(
                TableName='Subtitles',
                FilterExpression='contains(#k, :v)',
                ExpressionAttributeNames={'#k': 'keyword'},
                ExpressionAttributeValues={':v': {'S': keyword}}
            )

            # Get the associated videos and timestamps
            video_segments = []
            for item in response['Items']:
                video_segments.append({
                    'video': item['video']['S'],
                    'timestamp': item['timestamp']['N'],
                })

            return render(request, 'search.html', {'video_segments': video_segments})
        else:
            error_message = 'Please enter a keyword to search.'
            return render(request, 'search.html', {'error_message': error_message})
