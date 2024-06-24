# FROM python:3.9-slim as compiler
# ENV PYTHONUNBUFFERED 1

# WORKDIR /framework/ 

# RUN python -m venv /opt/venv
# # Enable venv
# ENV PATH="/opt/venv/bin:$PATH"

# COPY ./requirements.txt /framework/requirements.txt
# RUN pip install -r requirements.txt

# FROM python:3.9-slim as runner
# WORKDIR /framework/
# COPY --from=compiler /opt/venv /opt/venv

# # Enable venv
# ENV PATH="/opt/venv/bin:$PATH"
# COPY . /framework/
# CMD ["python", "sampledata_new.py"]

FROM python:3.12 as compiler
COPY /data_sample .