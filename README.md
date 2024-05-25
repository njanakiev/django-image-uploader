# django-image-uploader

A Django example application that allows users to upload images, which are then displayed on the home page with a search functionality. Users can upload images via the built-in Django admin interface.

# Run Locally

Create Python virtual environment with:

```bash
cd app
python -m venv -/venv
source venv/bin/activate
pip install -r requirements.txt
```

Run database migrations to `db.sqlite3` file with:

```bash
python manage.py migrate
```

Run development server with:

```bash
python manage.py runserver localhost:8020
```

The application should now be available at [localhost:8020](http://localhost:8020).


# Run Locally with Docker Compose

First, define the environment variables for docker-compose in `.docker.env`. Simply copy `example.docker.env` to `.docker.env` and adapt if needed.

Next, run the application using docker-compose with:

```bash
docker-compose up --build
```

The server should now be available again at [localhost:8020](http://localhost:8020).

# Deploy Using Ansible

First, define environment variables in `.prod.env`. An example configuration can be found in `example.prod.env`.

Run setup configuration with:

```bash
source .prod.env
ansible-playbook -v ansible/setup.yml --ask-become-pass
```

Finally, run deployment configuration with:

```bash
source .prod.env
ansible-playbook -v ansible/deploy.yml --ask-become-pass
```

# License

This project is licensed under the MIT license. See the [LICENSE](LICENSE) for details.
