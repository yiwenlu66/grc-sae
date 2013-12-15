from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed
from grc.models import Group, Question
from mysite.settings import DEBUG
import time,random,itertools

def Portal(request):
    groups=Group.objects.filter(enabled=True)
    groups_en_ch=[(item.name_en, item.name_ch) for item in groups]
    #init groups
    if request.method=="GET":
        return render_to_response("portal.html",{"groups":[item[1] for item in groups_en_ch]}, context_instance=RequestContext(request))
        #render Chinese names of groups
    elif request.method=="POST":
        try:
            response=HttpResponseRedirect("/review")
            groups_selected = []
            for i in range(len(groups_en_ch)):
                if request.POST.get("group%d" % i):
                    groups_selected.append(groups_en_ch[i][0])
            # Get selected groups
            order = eval(request.POST["order"])
            # Get selected order (0 for random, 1 for ordered)
            response.set_cookie("groups",str(groups_selected)[1:-1].replace(", ", "|"))
            response.set_cookie("order",order)
            if order:
                response.set_cookie("gseq",0)
                response.set_cookie("qseq",0)
            # Record current gseq & qseq for ordered revision
            else:
                response.set_cookie("chosen","set()")
                response.delete_cookie("gseq")
                response.delete_cookie("qseq")
            # Record chosen (group, question) tuples for random revision
            return response
        except:
            if DEBUG:
        	    raise
            else:
                return HttpResponseRedirect("/")
    else:
        return HttpResponseNotAllowed

def Review(request):
    def get_questions(name_en):
        """Given the English name of the group
        Return a list of questions from memcache(to be implemented) or DB"""
        questions=Question.objects.filter(group__name_en=name_en).order_by("created")
        return questions

    def finish():
        """Clear cookies and render the finish page"""
        response=render_to_response("finish.html")
        response.delete_cookie("groups")
        response.delete_cookie("order")
        response.delete_cookie("gseq")
        response.delete_cookie("qseq")
        response.delete_cookie("chosen")
        return response

    try:
	    groups = eval(("[" + request.COOKIES.get("groups") + "]").replace("|", ","))
	    order = eval(request.COOKIES.get("order"))
	    if order:
	        gseq = eval(request.COOKIES.get("gseq"))
	        qseq = eval(request.COOKIES.get("qseq"))
	        questions = get_questions(groups[gseq])
	        if qseq == len(questions):
	            gseq += 1
	            qseq = 0
	            response=render_to_response("review.html",{"question":questions[qseq]})
	            response.set_cookie("gseq",gseq)
	            response.set_cookie("qseq",qseq)
	            # Advance to next group
	            if gseq == len(groups):
	                return finish()
	            return response
	        return render_to_response("review.html",{"question":questions[qseq]})
	    else:
	        all_questions = list(itertools.chain(
	            *[get_questions(group) for group in groups]))
	        chosen = eval(request.COOKIES.get("chosen").replace("|", ","))
	        if len(chosen) == len(all_questions):
	            return finish()
	        qseq_to_render = random.choice(list(set(range(len(all_questions))) - chosen))
	        chosen.add(qseq_to_render)
	        response=render_to_response("review.html",{"question":all_questions[qseq_to_render]})
	        response.set_cookie("chosen",("{" + str(chosen)[5:-2] + "}").replace(", ", "|"))
	        # Avoid cookies with [] ,space or ','
	        return response
    except:
        if DEBUG:
    	    raise
        else:
            return HttpResponseRedirect("/")

def About(request):
    return render_to_response("about.html")
