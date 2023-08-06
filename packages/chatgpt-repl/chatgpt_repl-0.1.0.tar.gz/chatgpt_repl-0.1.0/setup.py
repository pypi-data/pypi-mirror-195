from setuptools import setup

setup(
    name='chatgpt_repl',
    version='0.1.0',
    packages=['chatgpt_repl'],
    install_requires=[
        'openai',
        'termcolor',
        'halo'
    ],
    entry_points={
        'console_scripts': [
            'chatgpt_repl=chatgpt_repl.__main__:main'
        ]
    },
    author='Evgeny Rodionov',
    author_email='opensource@erodionov.ru',
    description='A chatbot powered by OpenAI\'s ChatGPT API',
    license='MIT',
    keywords='chatgpt',
    url='https://github.com/evgenyrodionov/chatgpt_repl',
    project_urls={
        'Source Code': 'https://github.com/evgenyrodionov/chatgpt_repl',
        'Bug Tracker': 'https://github.com/evgenyrodionov/chatgpt_repl/issues',
    }
)
