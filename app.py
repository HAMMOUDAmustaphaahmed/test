from flask import Flask,render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy import Numeric
from werkzeug.security import check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flaskadmin:Flask!1234@localhost:3306/invento'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'invento_clé_secrète'

# Initialize SQLAlchemy with the app


db = SQLAlchemy(app)


   


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('signin.html')



# Route for login
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        print(f"Username: {username}")
        print(f"Password: {password}")

        # Fetch the user from the database
        user = User.query.filter_by(username=username).first()

        # Check if user exists
        if user is None:
            flash("Nom d'utilisateur ou mot de passe incorrect !", "danger")
           
        # Check if the password matches
        if user and check_password_hash(user.password, password):
           
            session['role'] = user.role  # Store the username in the session
            return redirect(url_for("admin"))  # Redirect to the admin page
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect !", "danger")  # Provide feedback to the user
    
    return render_template("signin.html")


@app.route('/logout')
def logout():
        session.clear()  # Efface la session pour déconnecter l'utilisateur
        return redirect(url_for('login'))

 
# Route pour la page d'administration
@app.route('/admin')
def admin():
       
            return render_template('index.html')
       

    # Route pour la connexion

@app.route('/ajouter_article',methods=["GET", "POST"])
def ajouter_article():
        if 'user' in session and session['user'] == 'administrateur':
            if request.method == 'POST':
                # Retrieve form data
                article_data = {
                'code_article': request.form.get('code_article'),
                'libelle_article': request.form.get('libelle_article'),
                'prix_achat': request.form.get('prix_achat'),
                'assignation': request.form.get('assignation'),
                'quantite': request.form.get('quantite'),
                'fournisseur': request.form.get('fournisseur'),
                'quantite_min': request.form.get('quantite_min')
            }

                # Call the function to add user
                if fun_ajouter_article(article_data):
                    flash("Article ajouté avec succès", "success")
                else:
                    flash("Erreur lors de l'ajout de l'article", "danger")
            return render_template('ajouter_article.html')
        else:
            return redirect(url_for('login'))
    
    


    # routes.py

@app.route('/rechercher_article', methods=['GET', 'POST'])
def rechercher_article():
    
        if request.method == 'POST':
            code_article = request.form.get("code_article")
            article = fun_info_article(code_article)
            if article:
                return render_template('editer_article.html', article=article)
            else:
                flash("Article not found", "danger")
                
        
    

@app.route('/editer_article', methods=['POST','GET'])
def editer_article():
    
        code_article = request.form.get('code_article')
        action = request.form.get('action')  # Récupérer l'action (edit ou delete)
        article = fun_info_article(code_article)

        if action == 'edit':
            if article:
                # Mettre à jour les informations de l'article
                article.libelle_article = request.form.get('libelle_article')
                article.prix_achat = request.form.get('prix')
                article.assignation = request.form.get('assignation')
                article.quantite = request.form.get('quantite')
                article.fournisseur = request.form.get('fournisseur')
                article.quantite_min = request.form.get('quantite_min')

                

                # Valider les données et committer les mises à jour
                try:
                    db.session.commit()
                    flash("Article modifié avec succès", "success")
                    
                except :
                    db.session.rollback()
                    flash("Erreur lors de la mise à jour de l'article", "danger")
            else:
                flash("Article non trouvé", "danger")

        elif action == 'delete':
            if article:
                # Supprimer l'article de la base de données
                db.session.delete(article)
                db.session.commit()
                flash("Article supprimé avec succès", "success")
               
            else:
                flash("Article non trouvé", "danger")

        return render_template('editer_article.html')  # Rediriger si aucune action trouvée
    



@app.route('/supprimer_article')
def supprimer_article():
        
            return render_template('supprimer_article.html')
        




@app.route('/ajouter_user', methods=['GET', 'POST'])
def ajouter_user():
        
            if request.method == 'POST':
                # Retrieve form data
                user_data = {
                    'username': request.form['username'],
                    'password': request.form['password'],
                    'emplacement': request.form['emplacement'],
                    'role': request.form['role'],
                    'numero_telephone': request.form['numero_telephone']
                }

                # Call the function to add user
                if fun_ajouter_user(user_data):
                    flash("Utilisateur ajouté avec succès", "success")
                else:
                    flash("Erreur lors de l'ajout de l'utilisateur", "danger")
            return render_template('ajouter_user.html')
        

    
@app.route('/editer_user')
def editer_user():
       
            return render_template('editer_user.html')
        
    
@app.route('/supprimer_user')
def supprimer_user():
        
            return render_template('supprimer_user.html')
        
        

@app.route('/ajouter_usine',methods=['GET', 'POST'])
def ajouter_usine():
       
            if request.method == 'POST':
                # Retrieve form data
                usine_data = {
                    'nom_usine': request.form['nom_usine'],
                    'region': request.form['region'],
                    'adresse': request.form['adresse'],
                    'latitude': request.form['latitude'],
                    'longitude': request.form['longitude'],
                    'telephone': request.form['telephone'],
                    'etat': request.form['etat']
                }

                # Call the function to add user
                if fun_ajouter_usine(usine_data):
                    flash("Usine ajouté avec succès", "success")
                else:
                    flash("Erreur lors de l'ajout de l'usine", "danger")
            return render_template('ajouter_usine.html')
        


@app.route('/editer_usine')
def editer_usine():
       
            return render_template('editer_usine.html')
        
    
@app.route('/supprimer_usine')
def supprimer_usine():
        
            return render_template('editer_usine.html')
        
        
@app.route('/ajouter_fournisseur',methods=['GET', 'POST'])
def ajouter_fournisseur():
        
            if request.method == 'POST':
                # Retrieve form data
                fournisseur_data = {
                    'nom_fournisseur': request.form['nom_fournisseur'],
                    'matricule_fiscale': request.form['matricule_fiscale'],
                    'adresse': request.form['adresse'],
                    'telephone': request.form['telephone'],
                }

                # Call the function to add user
                if fun_ajouter_fournisseur(fournisseur_data):
                    flash("Fournisseur ajouté avec succès", "success")
                else:
                    flash("Erreur lors de l'ajout de fournisseur", "danger")
            return render_template('ajouter_fournisseur.html')
        
        
        
        
@app.route('/editer_fournisseur')
def editer_fournisseur():
       
            return render_template('editer_fournisseur.html')
       
        
@app.route('/supprimer_fournisseur')
def supprimer_fournisseur():
        
            return render_template('editer_fournisseur.html')
        
        





def fun_ajouter_user(data):
    try:
        # Hash the password
        password=data['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new user
        new_user = User(
            username=data['username'],
            password=hashed_password,
            emplacement=data['emplacement'],
            role=data['role'],
            numero_telephone=data['numero_telephone']
        )
        # Add and commit to the database
        db.session.add(new_user)
        db.session.commit()
        fun_history_ajouter_user(data)
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'utilisateur : {e}")
        db.session.rollback()  # Roll back changes on error
        return False

def fun_ajouter_article(data):

    try:
       
        
        # Create a new Article
        new_article = Article(
            code_article=data['code_article'],
            libelle_article=data['libelle_article'],
            prix_achat=data['prix_achat'],
            assignation=data['assignation'],
            quantite=data['quantite'],
            fournisseur=data['fournisseur'],
            date=datetime.now(timezone.utc),
            quantite_min=data['quantite_min']
        )

        # Add and commit to the database
        db.session.add(new_article)
        db.session.commit()
        fun_history_ajouter_article(data)
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'article: {e}")
        db.session.rollback()  # Roll back changes on error
        return False

def fun_ajouter_usine(data):

    try:
       
        
        # Create a new Usine
        new_usine = Usine(
            nom_usine=data['nom_usine'],
            region=data['region'],
            adresse=data['adresse'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            telephone=data['telephone'],
            etat=data['etat']
        )

        # Add and commit to the database
        db.session.add(new_usine)
        db.session.commit()
        fun_history_ajouter_usine(data)
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'usine: {e}")
        db.session.rollback()  # Roll back changes on error
        return False


def fun_ajouter_fournisseur(data):
    try:
        # Create a new Fournisseur
        new_fournisseur = Fournisseur(
            nom_fournisseur=data['nom_fournisseur'],
            matricule_fiscale=data['matricule_fiscale'],
            adresse=data['adresse'],
            telephone=data['telephone'],
        )
        # Add and commit to the database
        db.session.add(new_fournisseur)
        db.session.commit()
        fun_history_ajouter_fournisseur(data)
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout de fournisseur: {e}")
        db.session.rollback()  # Roll back changes on error
        return False

def fun_history_ajouter_fournisseur(data):
    
    new_history=History(
        fournisseur=data['nom_fournisseur'],
        action="ajout d'un nouveau fournisseur",
        details=str(' matricule fiscale : '+data['matricule_fiscale']+' addresse : '+data['adresse']+' telephone : '+data['telephone'])
        )
    db.session.add(new_history)
    db.session.commit()
    return True
    
def fun_history_ajouter_user(data):
    
    new_history=History(
        user=data['username'],
        action="ajout d'un nouveau user",
        details=str(' emplacement : '+data['emplacement']+' role : '+data['role']+' telephone : '+data['telephone'])
        )
    db.session.add(new_history)
    db.session.commit()
    return True
    
def fun_history_ajouter_article(data):
    
    new_history=History(
        code_article=data['code_article'],
        libelle_article=data['libelle_article'],
        emplacement=data['assignation'],
        prix=data['prix_achat'],
        action="ajout d'un nouveau article",
        fournisseur=data['fournisseur'],
        details=str('date : ' + datetime.now(timezone.utc) + 'quantite_min : ' + data['quantite_min'])
        )
    db.session.add(new_history)
    db.session.commit()
    return True

def fun_history_ajouter_usine(data):
    
    new_history=History(
        nom_usine=data['nom_usine'],
        emplacement=data['region'],
        action="ajout d'un nouveau usine",
        details=str('addresse : ' + data['telephone'] + 'etat : ' + data['etat']))
    db.session.add(new_history)
    db.session.commit()
    return True

def fun_info_article(code_article):
    article_data = Article.query.filter_by(code_article=code_article).first()
    return article_data
                





# User Model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    emplacement = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    numero_telephone = db.Column(db.Integer, nullable=True)

# Article Model
class Article(db.Model):
    __tablename__ = 'articles'
    id_article = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code_article = db.Column(db.String(20), nullable=False)
    libelle_article = db.Column(db.String(255), nullable=False)
    prix_achat = db.Column(db.Float, nullable=False)
    assignation = db.Column(db.String(255), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    fournisseur = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    quantite_min = db.Column(db.Integer, nullable=False)

# Supplier Model (Fournisseur)
class Fournisseur(db.Model):
    __tablename__ = 'fournisseur'
    id_fournisseur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_fournisseur = db.Column(db.String(255), nullable=False)
    matricule_fiscale = db.Column(db.String(50), nullable=True)
    adresse = db.Column(db.String(255), nullable=True)
    telephone = db.Column(db.String(50), nullable=True)

# Purchase Model (Achats)
class Achat(db.Model):
    __tablename__ = 'achats'
    code_demande = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code_article = db.Column(db.Integer, nullable=False)
    libelle_article = db.Column(db.String(255), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_achat = db.Column(db.Float, nullable=False)
    assignation = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    fournisseur = db.Column(db.String(255), nullable=False)
    lot_achat = db.Column(db.String(255), nullable=False)

# Sales Model (Ventes)
class Vente(db.Model):
    __tablename__ = 'ventes'
    id_vente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code_demande = db.Column(db.Integer, nullable=True)
    code_article = db.Column(db.Integer, nullable=True)
    libelle_article = db.Column(db.String(20), nullable=True)
    quantite = db.Column(db.Integer, nullable=True)
    prix_vente = db.Column(Numeric(6, 3), nullable=True)
    assignation = db.Column(db.String(20), nullable=True)
    vers = db.Column(db.String(20), nullable=True)
    demandeur = db.Column(db.String(20), nullable=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

# Sales Request Model (DemandeVente)
class DemandeVente(db.Model):
    __tablename__ = 'demande_vente'
    code_demande = db.Column(db.Integer, primary_key=True)
    code_article = db.Column(db.String(50), nullable=False)
    libelle_article = db.Column(db.String(20), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_vente = db.Column(Numeric(6, 3), nullable=True)
    assignation = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    demandeur = db.Column(db.String(20), nullable=True)
    vers = db.Column(db.String(20), nullable=True)
    commande = db.Column(db.String(20), nullable=True)
    etat = db.Column(db.Integer, nullable=False)
    reception = db.Column(db.Integer, nullable=False)
    commentaire = db.Column(db.String(255), nullable=True)

# Purchase Request Model (DemandeAchat)
class DemandeAchat(db.Model):
    __tablename__ = 'demande_achat'
    code_demande = db.Column(db.Integer, primary_key=True)
    code_article = db.Column(db.String(50), nullable=False)
    libelle_article = db.Column(db.String(20), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_achat = db.Column(Numeric(6, 3), nullable=True)
    assignation = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    demandeur = db.Column(db.String(20), nullable=True)
    vers = db.Column(db.String(20), nullable=True)
    commande = db.Column(db.String(20), nullable=True)
    etat = db.Column(db.Integer, nullable=False)
    reception = db.Column(db.Integer, nullable=False)
    commentaire = db.Column(db.String(255), nullable=True)

# History Model
class History(db.Model):
    __tablename__ = 'history'
    id_history = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code_demande = db.Column(db.Integer, nullable=True)
    code_article = db.Column(db.String(50), nullable=True)
    libelle_article = db.Column(db.String(255), nullable=True)
    quantite = db.Column(db.Integer, nullable=True)
    prix = db.Column(db.Float, nullable=True)
    fournisseur = db.Column(db.String(20), nullable=True)
    emplacement = db.Column(db.String(20), nullable=True)
    action = db.Column(db.String(50), nullable=True)
    user = db.Column(db.String(20), nullable=True)
    details = db.Column(db.String(255), nullable=True)
    usine = db.Column(db.String(20), nullable=True)
    date_action = db.Column(db.TIMESTAMP, nullable=True)
    date_approuver_demande = db.Column(db.TIMESTAMP, nullable=True)
    date_reception = db.Column(db.TIMESTAMP, nullable=True)

# Factory Model (Usine)
class Usine(db.Model):
    __tablename__ = 'usine'
    id_usine = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_usine = db.Column(db.String(20), nullable=False)
    region = db.Column(db.String(20), nullable=False)
    adresse = db.Column(db.String(20), nullable=True)
    latitude = db.Column(db.String(20), nullable=True)
    longitude = db.Column(db.String(20), nullable=True)
    telephone = db.Column(db.String(20), nullable=True)
    etat = db.Column(db.String(20), nullable=False)  
    


if __name__ == '__main__':
    app.run(debug=True)
