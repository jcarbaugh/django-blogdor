from distutils.core import setup

long_description = open('README.md').read()
 
setup(
    name='django-blogdor',
    version="2.0.0",
    packages=['blogdor','blogdor.templatetags'],
    package_dir={'blogdor': 'blogdor'},
    package_data={'blogdor': ['templates/admin/blogdor/post/*.html',
                              'templates/blogdor/*.html',
                              'templates/blogdor/feeds/*.html',
                              'templates/comments/*.html']},
    description='Django blogging application',
    author='Jeremy Carbaugh',
    author_email='jcarbaugh@gmail.com',
    license='BSD License',
    url='https://github.com/sunlightlabs/django-blogdor/',
    long_description=long_description,
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
    ],
)
