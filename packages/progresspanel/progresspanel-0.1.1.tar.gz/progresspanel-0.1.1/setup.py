from setuptools import setup

setup(
    name="progresspanel",
    version="0.1.1",
    description="The Progress Panel is a custom tkinter widget that displays a progress bar and buttons (Start/Resume, Pause, Terminate) to control a user-defined task that runs in a separate thread.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Xuejian Ma",
    author_email="Xuejian.Ma@gmail.com",
    url="https://github.com/xuejianma/progresspanel",
    license="MIT",
    packages=["progresspanel"],
    keywords=["tkinter", "progress panel", "progress bar", "threading"],
    test_suite="tests"
)
