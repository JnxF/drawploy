<img width=300 align="right"  src="https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/000/792/055/datas/gallery.jpg">

# Drawploy (draw & deploy)

When we are setting up cloud environments, the normal procedure is discussing the architecture with our coworkers, drawing a sketch of the different services and filling templates manually in order to create and deploy those services. And there is where we came in! We keep you from doing the automatic part so that you can just focus on the important point: drawing a good sketch!

## How to deploy it
### Backend
Needs: Python 3.X, virtualenv

- `git clone https://github.com/JnxF/drawploy.git && cd backend`
- `virtualenv env --python=python3`
- `source ./env/bin/activate`
- `pip install -r requirements.txt`

And, to run the server:

- `python manage.py runserver`

### Frontend
Needs npm

- `npm install`
- `npm run start`
