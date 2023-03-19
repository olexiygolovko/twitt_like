from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Post
from .serializers import *

@api_view(['GET', 'POST', 'DELETE'])
def posts(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        post = Post()
        post.text = request.data['text']
        post.save()
        return Response(status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
        return Response({'message': 'Post has been deleted'}, status=status.HTTP_204_NO_CONTENT)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def like_post(request, post_id):
   if request.method == 'GET':
    try:
        post = Post.objects.get(id = post_id)
    except:
        return Response(status = status.HTTP_400_BAD_REQUEST)

    setattr(post, 'likesCount', post.likesCount + 1)
    post.save()
    return Response(post.likesCount, status.HTTP_200_OK)
