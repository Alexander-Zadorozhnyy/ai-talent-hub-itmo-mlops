FROM clearml/clearml-serving-inference:latest

COPY requirements.txt .

# Force the upgrade to the version you need
RUN pip install --upgrade --force-reinstall -r ./requirements.txt