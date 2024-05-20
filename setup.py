from setuptools import setup

setup(
    name='AiMe',
    version='0.1',
    description='A world-class AI Assistant for Chromebooks.',
    url='https://github.com/zipp86/AiMe',
    author='Solomon',
    author_email='solomonsremodeling9@gmail.com',
    license='MIT',
    packages=['AiMe'],
    zip_safe=False,
    install_requires=[
        'Click',
        'pyttsx3',
        'SpeechRecognition',
        'pydub',
        'wget',
        'beautifulsoup4',
        'lxml',
        'gTTS',
        'youtube_dl',
        'psutil',
        'sqlite3',
        'inspect',
        'ast',
    ],
    entry_points='''
        [console_scripts]
        AiMe=AiMe.AiMe:AiMe
    ''',
)
