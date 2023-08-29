# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
#hub-4.02 is the latest version supported by HELM 3.00 (JupyterHub 4.0.2) as of 2023-08-15
FROM jupyter/base-notebook:hub-4.0.2
# Previous image, used to build JupyterHub
#FROM jupyterhub/jupyterhub@sha256:08fd4f04e5448eb96834a362cef641d4337ad92e9f1a42a8e92754b28bc719d6
USER root
# Install git (for use with nbgitpuller)
RUN apt-get update -qq \
 && apt-get install -yqq --no-install-recommends git

RUN pip install nbgitpuller notebook jupyterlab_myst

USER $NB_USER