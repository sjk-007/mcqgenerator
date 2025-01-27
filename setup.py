from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.0.1',
    author='sjk khowsik',
    author_email='sjkagent007@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)