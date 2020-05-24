from django.shortcuts import render,HttpResponse,redirect
from blog.models import Post,BlogComment
from django.contrib import messages
from blog.templatetags import get_dict

# Create your views here.

def blogHome(request):
     allPosts = Post.objects.all()
     context = {'allPosts' : allPosts}
     # print(allPosts)

     return render(request,'blog/blogHome.html',context)

def blogPost(request,slug):
     post = Post.objects.filter(slug = slug).first()
     post.views += 1
     post.save()
     comments = BlogComment.objects.filter(post = post,parent=None)
     # != can't be used directly
     replies = BlogComment.objects.filter(post = post).exclude(parent=None)
     repDict = {}
     for reply in replies:
          if reply.parent.sno not in repDict.keys():
               repDict[reply.parent.sno] = [reply]
          else:
               repDict[reply.parent.sno].append(reply)
     # print(repDict)
     # print(post)
     context = {"post" : post, 'comments':comments, 'replies':replies, 'comment_counts' : len(comments),'replyDict':repDict}
     return render(request,'blog/blogPost.html',context)

def postComment(request):
     if request.method == "POST":
          comment = request.POST['comment']
          user = request.user
          postSno = request.POST['postSno']
          parentSno = request.POST['parentSno']
          post = Post.objects.get(sno = postSno)

          if parentSno == "":
               comment = BlogComment(comment = comment,user=user,post=post)
               messages.success(request,"Your comment has been added successfully")
               comment.save()
          else:
               parent = BlogComment.objects.get(sno = parentSno)
               comment = BlogComment(comment = comment,user=user,post=post,parent = parent)
               messages.success(request,"Your reply has been added successfully")
               comment.save()

     return redirect(f'/blog/{post.slug}')