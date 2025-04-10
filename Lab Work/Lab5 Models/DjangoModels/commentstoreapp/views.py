from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from commentstoreapp.forms import InsertNewComment
from commentstoreapp.models import Comment

cmnt_list = []


@csrf_exempt
def commentstore(request):

    if request.method == 'POST':
        form = InsertNewComment(request.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            c = form.cleaned_data["comment_str"]
            d = form.cleaned_data["visit_date"]
            t = Comment(name=n, visit_date=d, comment_str=c)
            t.save()

            cmnt_list = list(Comment.objects.all())
            # for cmnt in cmnt_list:
            #    print(cmnt.name + " : " + cmnt.visit_date.__str__() + " : " + cmnt.comment_str)

            return render(request, "commentstoreapp/home.html", {"cmnt_list": cmnt_list})
    else:
        form = InsertNewComment()

    return render(request, "commentstoreapp/comment.html", {"form": form})


def home(request):
    return render(request, "commentstoreapp/home.html", {"cmnt_list": cmnt_list})
