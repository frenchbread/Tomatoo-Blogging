from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, RequestContext, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from models import Post, Save
from django.contrib.auth.models import User
from forms import PostForm, SettingsForm
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import Http404
import urllib, hashlib

hello_world = TemplateView.as_view(template_name='hello-world.html')


def givemealinkforpic(email):
    email = email
    default = "http://www.genengnews.com/app_themes/genconnect/images/default_profile.jpg"
    size = 100

    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})

    return gravatar_url

@login_required
def feed(request):

    args = {}
    args.update(csrf(request))

    p = Post.objects.all().order_by('-timestamp')

    #pagination----------------------------------------------------------
    paginator = Paginator(p, 5)
    page = request.GET.get('page')
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)

    args.update({'p': p})
    template = 'feed.html'
    context = RequestContext(request)

    return render_to_response(template, args, context_instance=context)

@login_required
def saved(request):

    args = {}
    args.update(csrf(request))

    u = get_object_or_404(User, username=request.user.username)
    p = Post.with_saved.filter(id__in=Save.objects.filter(user=u).values_list('post__id'))

    #pagination----------------------------------------------------------
    paginator = Paginator(p, 5)
    page = request.GET.get('page')
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)


    args.update({'p': p})
    template = 'saved.html'
    context = RequestContext(request)

    return render_to_response(template, args, context_instance=context)

@login_required
def newpost(request):

    args = {}
    args.update(csrf(request))

    #making some fun stuff-----------------------------------------------
    if request.POST:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()

            return HttpResponseRedirect(reverse('feed'))
    else:
        form = PostForm()

    #packing bags and fly--------------------------------------------------
    args.update({'form': form})
    template = 'newpost.html'
    context = RequestContext(request)
    return render_to_response(template, args, context_instance=context)


def post(request, post_id):

    args = {}
    args.update(csrf(request))

    #info gathering------------------------------------------------------
    p = get_object_or_404(Post, id=post_id)

    if request.user.is_authenticated():
        try:
            saved = Save.objects.get(user=request.user, post=p)
        except:
            saved = None
        if not saved:
            l = 'save'
        else:
            l = 'remove'
    else:
        l = None


    #packing bags and fly--------------------------------------------------
    args.update({'p': p, 'l': l})
    template = 'post.html'
    context = RequestContext(request)
    return render_to_response(template, args, context_instance=context)


@login_required
def editpost(request, post_id):

    args = {}
    args.update(csrf(request))

    #info gathering--------------------------------------------------------
    p = get_object_or_404(Post, id=post_id, user=request.user)

    #making some fun stuff-----------------------------------------------
    if request.user == p.user:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=p)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('post', kwargs={"post_id": post_id}))
        else:
            form = PostForm(instance=p)
    else:
        raise Http404

    #packing bags and fly--------------------------------------------------
    args.update({'form': form})
    template = 'editpost.html'
    context = RequestContext(request)
    return render_to_response(template, args, context_instance=context)

@login_required
def deletepost(request, post_id):
    args = {}
    args.update(csrf(request))

    p = get_object_or_404(Post, id=post_id, user=request.user)
    p.delete()

    return HttpResponseRedirect(reverse('feed'))


@login_required
def profile(request, username):

    args = {}
    args.update(csrf(request))

    #info gathering------------------------------------------------------
    thisUser = get_object_or_404(User, username=username)
    p = Post.objects.filter(user=thisUser).order_by('-timestamp')

    #pagination----------------------------------------------------------
    paginator = Paginator(p, 5)
    page = request.GET.get('page')
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)

    pic = givemealinkforpic(thisUser.email)

    #packing bags and fly--------------------------------------------------
    args.update({'thisuser': thisUser, 'p': p, 'pic': pic})
    context = RequestContext(request)
    template = "profile.html"
    return render_to_response(template, args, context_instance=context)


@login_required
def save(request, target_id):
    target = get_object_or_404(Post, id=target_id)
    if target:
        u = get_object_or_404(User, username=request.user.username)
        prev_saved = Save.objects.filter(user=u, post=target)
        has_saved = (len(prev_saved) > 0)
        if not has_saved:
            Save.objects.create(user=u, post=target)
        else:
            prev_saved[0].delete()

    response = HttpResponse(mimetype="text/html")
    response['content-type'] = "text/html; charset=UTF-8"
    response.write('You saved post "%s"' % target.title)
    return response


@login_required
def remove(request, target_id):
    target = get_object_or_404(Post, id=target_id)
    if target:
        u = get_object_or_404(User, username=request.user.username)
        prev_saved = Save.objects.filter(user=u, post=target)
        has_saved = (len(prev_saved) > 0)
        if not has_saved:
            Save.objects.create(user=u, post=target)
        else:
            prev_saved[0].delete()

    response = HttpResponse(mimetype="text/html")
    response['content-type'] = "text/html; charset=UTF-8"
    response.write('You removed post "%s"' % target.title)
    return response

@login_required
def settings(request):

    context_vars = {}
    context_vars.update(csrf(request))

    pic=givemealinkforpic(request.user.emai)

    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile', kwargs={"username": request.user.username}))
    else:
        form = SettingsForm(instance=request.user)

    context_vars.update({'form': form, 'pic': pic})
    template = 'settings.html'
    context = RequestContext(request)
    return render_to_response(template, context_vars, context_instance=context)