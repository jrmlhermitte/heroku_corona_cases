#!/bin/bash
# Scripts used to install necessary tools from scratch.
# Useful for CI environments.
# Keep idempotent if possible, avoid reinstalls.


function install_poetry_if_needed(){
  echo "Checking for the existence of poetry..."
  if ! type "poetry" > /dev/null; then
    echo "Poetry not found. Installing"
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  else
    echo "Poetry already installed. Nothing to do."
  fi

  # configure poetry venvs to save locally
  poetry config --local virtualenvs.in-project true
}


# List functions to install here.
function bootstrap(){
  install_poetry_if_needed
}


bootstrap
