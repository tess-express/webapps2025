from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from commentstoreapp.commentstore import CommentStore
from datetime import datetime

store = CommentStore()


@csrf_exempt
def commentstore(request):
    # raise Http404()
    # html = "<html><body>Hello, Student. You're at the Comment Store Application.</body></html>"
    # return HttpResponse(html)
    if request.method == 'GET':
        for header in request.headers.keys():
            print(header + ":" + request.headers.get(header))
        # get the django.http.response.HttpResponse object
        response = render(request, 'commentstore/index.html')
        # set http response header and value.
        response['Vary'] = 'Accept-Encoding'
        # return the HttpResponse object.
        return response

    if request.method == 'POST':
        date_object = datetime.strptime(request.POST.get('date'), '%d/%m/%Y').date()
        store.insertcomment(request.POST.get('name'),
                            date_object,
                            request.POST.get('comment'))
        htmltable = "<table>\n"\
                    + "  <tr>\n"\
                    + "    <th>Name</th>\n"\
                    + "    <th>Date</th>\n"\
                    + "    <th>Comment</th>\n"\
                    + "  </tr>\n"
        for cmnt in list(store.commentlist.queue):
            htmltable = htmltable + "  <tr>\n"\
                        + "    <td>" + cmnt.name + "</td>\n"\
                        + "    <td>" + str(cmnt.visitdate) + "</td>\n"\
                        + "    <td>" + cmnt.commentstr + "</td>\n"\
                        + "  </tr>\n";
        html = "<html><body> " + htmltable + "</body></html>"
        return HttpResponse(html)
