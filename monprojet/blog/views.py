from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .form import InscriptionForm  # Importer le formulaire d'inscription
from .models import Article, Library, CustomUser3
import os
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
import tempfile
from rest_framework.permissions import IsAuthenticated
from xhtml2pdf import pisa
import io


def inscription(request):

    if request.method == "POST":

        form = InscriptionForm(request.POST)  # save dans la BDD
        if form.is_valid():
            user = form.save()  # Sauvegarder l'utilisateur
            request.session["email"] = user.email
            request.session.set_expiry(300)
            login(
                request, user
            )  # Connecter l'utilisateur immédiatement après l'inscription
            return redirect("liste_bib")  # Rediriger vers le dashboard
    else:

        form = InscriptionForm()

        return render(request, "blog/Inscription.html")


def connexion(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user:
            request.session["email"] = user.email
            request.session.set_expiry(300)
            login(request, user)
            return redirect("liste_bib")
        else:
            return render(
                request,
                "blog/connexion.html",
                {"error": "Email ou mot de passe incorrect."},
            )

    return render(request, "blog/connexion.html")


def deconnexion(request):
    logout(request)
    request.session.flush()  # supprimer toutes les sessions
    return redirect("connexion")


def HTML_To_PDF(request,id):
    html_template="pdf_template.html"
    articles = Article.objects.filter(library=id)
    context={"title":'Les articles de la bibliotheques',"articles":articles}

    html= render(request, html_template, context).content.decode("utf-8")

    # Générer le PDF
    result = io.BytesIO()
    pdf = pisa.CreatePDF(io.StringIO(html), dest=result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = "inline; filename=mon_document.pdf"
        return response

    return HttpResponse("Erreur lors de la génération du PDF", status=500)


     

def dashboard(request):
    return render(request, "blog/dashboard.html")


def liste_articles(request,id):
    
    if "email" in request.session:
         
        articles = Article.objects.filter(library=id)
        return render(request, "blog/liste_articles.html", {"articles": articles,"id_lib":id})
    else:
        return redirect("connexion")
    


def liste_bib(request):
    if "email" in request.session:
        libes= Library.objects.all()
        
        print(libes)
        return render(request, "blog/liste_bib.html", {"libes":libes})
    else:
        return redirect("connexion")


def create_bib(request):
    if "email" in request.session:
        if request.method == "POST":
            nom = request.POST["nom"]
            Library.objects.create(Name=nom)
            return redirect("liste_bib")
        
        else:

            return render(
                request, "blog/create_bib.html", {"message": "Ajouter une bib"}
            )
    else:
        return redirect("connexion")


def create_article_id(request,id):
    
    if "email" in request.session:
        if request.method == "POST":
            
            titre = request.POST["titre"]
            contenu = request.POST["contenu"]
            library = request.POST["id_lib"]
            pdf = request.FILES.get("pdf")
            if pdf:
                upload_dir = os.path.join(settings.MEDIA_ROOT, "pdfs")
                os.makedirs(
                    upload_dir, exist_ok=True
                )  # créer le dossier s'il nexiste pas
                pdf_path = os.path.join(upload_dir, pdf.name)

                # Enregistrement du chemin du fichier dans /blog/pdf
                with open(pdf_path, "wb+") as destination:
                    for chunk in pdf.chunks():
                        destination.write(chunk)
                library_instance = Library.objects.get(id_lib=library)
                Article.objects.create(titre=titre, contenu=contenu, pdf_path=pdf_path, library=library_instance)
                
                return redirect(reverse('liste_articles', kwargs={'id':library}))
            else:
                return render(
                    request,
                    "blog/create_article.html",
                    {"message": "pdf is not uploaded"},
                )
            
        else:
            return render(
                    request, "blog/create_article.html", {"id_lib":id}
                )

       
    else:
        return redirect("connexion")

     

def create_article(request):
    if "email" in request.session:
        if request.method == "POST":
            
            titre = request.POST["titre"]
            contenu = request.POST["contenu"]
            library = request.POST["id"]
            pdf = request.FILES.get("pdf")
            if pdf:
                upload_dir = os.path.join(settings.MEDIA_ROOT, "pdfs")
                os.makedirs(
                    upload_dir, exist_ok=True
                )  # créer le dossier s'il nexiste pas
                pdf_path = os.path.join(upload_dir, pdf.name)

                # Enregistrement du chemin du fichier dans /blog/pdf
                with open(pdf_path, "wb+") as destination:
                    for chunk in pdf.chunks():
                        destination.write(chunk)

                Article.objects.create(titre=titre, contenu=contenu, pdf_path=pdf_path, library=library)
                return redirect("liste_articles")
            else:
                return render(
                    request,
                    "blog/create_article.html",
                    {"message": "pdf is not uploaded"},
                )

        else:

            return render(
                request, "blog/create_article.html", {"message": "créer un article",}
            )
    else:
        return redirect("connexion")


def update_article(request, id):
   
    if "email" in request.session:
        article = get_object_or_404(Article, id=id)
      
        if request.method == "POST":

            pdf = request.FILES.get("pdf_update")

            if os.path.exists(article.pdf_path):
                os.remove(article.pdf_path)

            if pdf:
                upload_dir = os.path.join(
                    settings.MEDIA_ROOT, "pdfs"
                )  # création du chemin
                os.makedirs(
                    upload_dir, exist_ok=True
                )  # créer le dossier s'il nexiste pas
                pdf_path = os.path.join(upload_dir, pdf.name)
                with open(pdf_path, "wb+") as destination:
                    for chunk in pdf.chunks():
                        destination.write(chunk)

                article.titre = request.POST["titre"]
                article.contenu = request.POST["contenu"]
                article.pdf_path = pdf_path
                 
                article.save()
                
                return redirect(reverse('liste_articles', kwargs={'id': article.library.id_lib}))
            

            else:
                return render(
                    request,
                    "blog/update_article.html",
                    {"message": "file not uploaded", "article": article},
                )

        else:
         
            return render(
                request,
                "blog/update_article.html",
                {"message": "Modifier un article", "article": article},
            )
    else:
        return redirect("connexion")


def delete_article(request, id, id_lib):
    if "email" in request.session:
        article = get_object_or_404(Article, id=id)
        print(article.pdf_path)
        if request.method == "GET":
            if os.path.exists(article.pdf_path):
                os.remove(article.pdf_path)
            article.delete()
           
            return redirect(reverse('liste_articles', kwargs={'id':id_lib}))
        
        else:
            return render(
                request,
                "blog/delete_article.html",
                {"article": article, "message": " you have to delete page"},
            )
    else:
        return redirect("connexion")


def afficher_pdf(request, id):
    # pdf_path = os.path.join(settings.MEDIA_URL, 'pdfs', pdf_filename)
    # return render(request, 'blog/afficher_pdf.html', {'pdf_path': pdf_path})
    if "email" in request.session:
        article = get_object_or_404(Article, id=id)
        pdf_path = article.pdf_path

        print(pdf_path)
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type="application/pdf")
                response["Content-Disposition"] = (
                    f'inline; filename="{os.path.basename(pdf_path)}"'
                )
                return response



# API DRF
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .serializers import ArticleSerializer, CustomUserSerializer
from django.contrib.auth.hashers import make_password

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def get_articles(request):
    articles=Article.objects.all()
    serializer= ArticleSerializer(articles,many=True) # transformer l'objet en type de données JSON
    permission_classes = [IsAuthenticated] 
    return Response(serializer.data) # retourner la réponse JSON
    




@api_view(['POST'])
def add_article(request):
    serializer = ArticleSerializer(data=request.data) # trasformer JSON en Objet 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT'])
def put_article(request, id_article):
    try:
        article = Article.objects.get(id=id_article)  # rechercher l'article par son id
    except Article.DoesNotExist:
        return Response({'error': 'Article not found'}, status=404)

    serializer = ArticleSerializer(article, data=request.data) # MAG les données et les transformer en objets
    if serializer.is_valid():
        serializer.save() # enregistrer les modifications (les changements)
        return Response(serializer.data)
    
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def sup_article(request, id_article):
    try:
        article = Article.objects.get(id=id_article) # recherche article by id
    except Article.DoesNotExist:
        return Response({'error': 'Article not found'}, status=404)

    article.delete()
    return Response({'message': 'Article deleted successfully'}, status=204)


# JWT
@api_view(['POST'])
def register_user(request):
    data=request.data
    
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return Response({'error': 'Username, email, and password are required'}, status=400)
    
    if CustomUser3.objects.filter(email=data['email']).exists():
        return Response({'error': 'Email already exists'}, status=400)
    
    user = CustomUser3.objects.create(
        username=data['username'],
        email=data['email'],
        password=make_password(data['password']),
    )
    return Response({'message': 'User registered successfully', 'user': CustomUserSerializer(user).data}, status=201)


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email  # Ajouter l'email au token JWT
        
        return token
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer