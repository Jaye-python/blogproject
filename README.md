# Blog Application
This is a Blog app that allows for posting, editing, deleting, filtering and searching of blog posts. It is built using Django for the backend and HTML, TailwindCSS, and jQuery for the frontend.
Tailwind CSS was added using CDN for faster development.

Commands below use `Linux OS`.

### Implementations:

1. Blog Posts can be Created, Updated or deleted 
2. Blog Posts can be searched, filtered from the dashboard
3. Django Admin page also implemented to be able to manage the app

### To launch this app on your system:

1. Navigate to your desktop (or any folder of your choice)
```
cd Desktop
```
2. Create a new folder/directory called `blog`
```
mkdir blog
```
3. Navigate into this new folder
```
cd blog
```
4. Create a new Python Virtual environment in the `blog` folder.
```
python3 -m venv ./blogvenv
```
5. Activate this new virtual environment
```
source blogvenv/bin/activate
```
6. Clone this git repo
```
git clone https://github.com/Jaye-python/blogproject.git
```
7. Move into the `blogproject` folder which is included in the downloaded repo
```
cd blogproject
```
8. Install dependencies; DB uses Django inbuilt SQLite; no need to run migration
```
pip install -r requirements.txt
```
9. Create `superuser` account. There is an existing Admin account with email: `bb@bb.com` and password `lagoslagos`
```
python manage.py createsuperuser
```
10. Launch application. You may also open the repo in VS Code by running `code .`
```
python manage.py runserver
```
11. You may view your Profile page by clicking on `Your Profile` button on your top right
12. You may view details of each blog post by clicking the `eye` icon (from where you'd see a form to add a comment anonymously); delete by clicking the `trash` icon and edit by clicking the `pencil` icon. You can only edit and delete posts created by you
13. You can view all Categories by clicking the `View all categories` button on your right
14. You can sign up using the navigation on the right. The app uses `email` as `username`. To login, provide your `email` as `username`
15. You can upload your profile picture from your Profile Page. By selecting the `Update Profile` button on your top right after sign up
16. From the homepage Blog Dashboard, you can `Create Blog Post`, `Create Category`, `View Blog Post Details`, `Delete Blog Posts`
17. From the homepage Blog Dashboard, you may `Search Blog Posts` by their titles and content by typing any text in the provided input field and it will search all blog posts that contain this text (after clicking `Search`)
18. Filter Blog Posts by their Category by selecting your preferred Category in the provided input field and select `Filter by Category` button. ALL categories are dynamically loaded via JavaScript (even newly-created categories)
19. You can also run all created tests by running:
```
python manage.py test
```
