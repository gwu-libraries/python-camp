FROM jupyterhub/jupyterhub@sha256:08fd4f04e5448eb96834a362cef641d4337ad92e9f1a42a8e92754b28bc719d6

# Install git (for use with nbgitpuller)
RUN apt-get update -qq \
 && apt-get install -yqq --no-install-recommends git

RUN pip install nbgitpuller notebook jupytext>=1.6 jupyter_contrib_nbextensions 

RUN jupyter contrib nbextension install --sys-prefix && jupyter nbextension enable rubberband/main --sys-prefix && jupyter nbextension enable exercise2/main --sys-prefix 

CMD ["./jh-startup.sh"]