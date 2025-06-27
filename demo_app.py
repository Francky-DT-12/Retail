from flask import Flask, render_template

app = Flask(__name__)

# Données de test fictives
sample_products = [
    {
        'id': 1,
        'pName': 'T-shirt avec Détails en Tape',
        'category': 'tshirt',
        'picture': 'tshirt1.jpg',
        'price': 120
    },
    {
        'id': 2,
        'pName': 'Jean Skinny Fit',
        'category': 'tshirt',
        'picture': 'jean1.jpg',
        'price': 240
    },
    {
        'id': 3,
        'pName': 'Chemise à Carreaux',
        'category': 'tshirt',
        'picture': 'shirt1.jpg',
        'price': 180
    },
    {
        'id': 4,
        'pName': 'T-shirt à Manches Longues',
        'category': 'tshirt',
        'picture': 'tshirt2.jpg',
        'price': 130
    }
]

sample_wallets = [
    {
        'id': 5,
        'pName': 'Portefeuille en Cuir Vertical',
        'category': 'wallet',
        'picture': 'wallet1.jpg',
        'price': 212
    },
    {
        'id': 6,
        'pName': 'T-shirt Graphique Courage',
        'category': 'wallet',
        'picture': 'wallet2.jpg',
        'price': 145
    },
    {
        'id': 7,
        'pName': 'Short Loose Fit Bermuda',
        'category': 'wallet',
        'picture': 'wallet3.jpg',
        'price': 80
    },
    {
        'id': 8,
        'pName': 'Jean Skinny Délavé',
        'category': 'wallet',
        'picture': 'wallet4.jpg',
        'price': 210
    }
]

@app.route('/')
def index():
    return render_template('modern_home.html', 
                         tshirt=sample_products, 
                         wallet=sample_wallets, 
                         belt=[], 
                         shoes=[], 
                         form=None, 
                         db_error=False)

@app.route('/old')
def old_index():
    return render_template('home.html', 
                         tshirt=sample_products, 
                         wallet=sample_wallets, 
                         belt=[], 
                         shoes=[], 
                         form=None, 
                         db_error=False)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
