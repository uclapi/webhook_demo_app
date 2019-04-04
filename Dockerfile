# Start with a base Node.js 9 image
FROM node:9-alpine

# Update package lists
RUN apk update

# Install Python 3
RUN apk add --no-cache python python-dev python3 python3-dev \
    linux-headers build-base bash git ca-certificates && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    rm -r /root/.cache

# Set the timezone to Europe/London
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/Europe/London /etc/localtime && \
    echo "Europe/London" > /etc/timezone

# Copy everything to the image
COPY . .

# Install the frontend build components
RUN npm install

# Build webpack frontend code
ENV NODE_ENV production
RUN npm run docker-build

# Get required PostgreSQL Libraries
RUN apk add postgresql-libs && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev

# Install the requirements components
RUN pip install -r requirements.txt

# Run migrations and start channels layer and backend worker in parallel
CMD /bin/bash -c "python3 manage.py migrate && daphne webhook_demo_app.asgi:channel_layer --bind 0.0.0.0 -p 80 & python3 manage.py runworker"
