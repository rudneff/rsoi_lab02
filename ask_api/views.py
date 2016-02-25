from uuid import uuid4
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from django.views.generic.edit import ProcessFormView
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from hashlib import sha256
from ask_api.forms import CustomUserCreateForm, CustomUserAuthForm
from ask_api.models import Question, Answer, CustomUser, Client, Authorization, Access, TIME_DELTA
from ask_api.permissions import IsAuthOrReadOnly, IsOwnerOrReadOnly
from ask_api.serializers import QuestionSerializer, AnswerSerializer


class QuestionListView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthOrReadOnly,)

    def post(self, request, *args, **kwargs):
        return super(QuestionListView, self).post(request, *args, **kwargs)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class AnswerListView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthOrReadOnly,)


class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class CustomUserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreateForm
    template_name = 'ask_api/signup.html'
    success_url = reverse_lazy('ask_api:status')


class CustomUserAuthenticationView(ProcessFormView):
    def get(self, request, *args, **kwargs):
        client_id = request.GET.get('client_id', '')
        response_type = request.GET.get('response_type', '')
        state = request.GET.get('state', '')

        try:
            client_id = int(client_id)
        except:
            client_id = None

        if not client_id or response_type not in 'code':
            return render(request, 'ask_api/fail.html', context={'message_error': 'wrong parameters'},
                          status=400)
        client = get_object_or_404(Client, pk=client_id)

        form = CustomUserAuthForm(initial={'state': state if state else None,
                                           'client_id': client_id})
        return render(request, 'ask_api/signin.html', {'form': form})

    def post(self, request, *args, **kwargs):

        form = CustomUserAuthForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()

            # username = request.POST.get('username', None)
            # password = request.POST.get('password', None)
            #
            # user = auth.authenticate(username=username, password=password)
            if user is not None:
                try:
                    client = Client.objects.get(pk=request.POST.get('client_id', None))
                except ObjectDoesNotExist:
                    return render(request, 'ask_api/fail.html', {'message_error': 'client doesn\'t  exist.'})
                code = sha256(str(uuid4()).encode('UTF-8')).hexdigest()
                authorization = Authorization(user=user, code=code)
                authorization.save()
                redirect_uri = ''.join([client.redirect_uri, '?code=', code, '&state=', request.POST.get('state', '')])
                return redirect(redirect_uri)
            form.add_error(field=None, error='asdasds')
        return render(request, 'ask_api/signin.html', {'form': form})


def signup(request):
    if request.method in 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        phone_number = request.POST.get('phone_number', '')
        password = request.POST.get('passwd1', '')
        new_user = CustomUser(username=username, email=email, phone_number=phone_number,
                              password=password)
        try:
            new_user.save()
        except:
            return render(request, "ask_api/signup.html", {'message_error': 'Something wrong!'})
    return render(request, "ask_api/signup.html")


@api_view(['GET'])
def status(request):
    return Response({"status": "OK"})


@csrf_exempt
@api_view(['POST'])
def token(request):
    client_id = request.POST.get('client_id', None)
    client_secret = request.POST.get('client_secret', None)
    grant_type = request.POST.get('grant_type', None)

    if grant_type in 'authorization_code':
        code = request.POST.get('code', None)
        try:
            client = Client.objects.get(pk=client_id, secret=client_secret)
            auth_info = Authorization.objects.get(code=code)
        except ObjectDoesNotExist:
            return Response({'status': 400, 'error': 'invalid_request'}, status=400)
        user = auth_info.user
        access_token = sha256(str(uuid4()).encode('UTF-8')).hexdigest()
        refresh_token = sha256(str(uuid4()).encode('UTF-8')).hexdigest()
        access = Access(user=user, token=access_token, refresh_token=refresh_token)
        access.save()
        auth_info.delete()
    elif grant_type in 'refresh_token':
        refresh_token = request.POST.get('refresh_token', None)
        try:
            client = Client.objects.get(pk=client_id, secret=client_secret)
            access_info = Access.objects.filter(refresh_token=refresh_token)[0]
        except (ObjectDoesNotExist, IndexError):
            return Response({'status': 400, 'error': 'invalid_request'}, status=400)
        access = Access.objects.filter(refresh_token=refresh_token).first()
        if access:
            access.token = sha256(str(uuid4()).encode('UTF-8')).hexdigest()
            access.update_time_to_expire()
            access.save()
    else:
        return Response({'status': 400, 'error': 'invalid_request'}, status=400)

    return Response(data={'access_token': access.token, 'refresh_token': access.refresh_token,
                          'token_type': 'bearer', 'expires_in': TIME_DELTA},
                    headers={'Cache-Control': 'no-store',
                             'Pragma': 'no-cache'})


def some_client_page(request):
    auth_code = request.GET.get('authorization_code', '')
    state = request.GET.get('state', '')
    return render(request, 'ask_api/some_client_page.html', context={'auth_code': auth_code, 'state': state})
