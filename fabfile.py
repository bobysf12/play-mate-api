from fabric.api import local, put, run, cd

app_name = 'playmate-api'
app_version = 'v1'
app_environment = ''


def pack():
    # build the package
    local('python setup.py sdist --formats=gztar', capture=False)


def staging():
    global app_environment
    app_environment = 'staging'


def production():
    global app_environment
    app_environment = 'production'


def deploy():
    # figure out the package name and version
    dist = local('python setup.py --fullname', capture=True).strip()
    filename = '%s.tar.gz' % dist

    # upload the package to the temporary folder on the server
    put('dist/%s' % filename, '/tmp/%s' % filename)

    # create virtualenv for new release
    with cd('/var/www/playmate-api'):
        run('virtualenv %s' % dist)

        # install the package in the application's virtualenv with pip
        run('./%s/bin/pip install six /tmp/%s --ignore-installed --process-dependency-links' % (dist, filename))

        # remove the uploaded package
        run('rm -r /tmp/%s' % filename)

        run('./%s/bin/pip install uwsgi' % dist)

        run('mkdir -p %s/var/playmate-instance' % dist)

        run('ln -sf /var/www/playmate-api/config/%s.cfg %s/var/playmate-instance/%s.cfg' % (app_environment, dist, app_environment))

        run('rm -f latest; ln -sf %s latest' % dist)

    run('supervisorctl restart PlaymateAPI')
