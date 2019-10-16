FROM registry.vis.ethz.ch/public/base:charlie

COPY cinit.yml /etc/cinit.d/demo.yml
COPY package.json yarn.lock ./
COPY requirements.txt /requirements.txt

RUN apt install -y python3 python3-pip

RUN pip3 install -r /requirements.txt

RUN apt install -y curl
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt update

RUN apt install -y nodejs

#RUN python3 /app/manage.py makemigrations
#RUN python3 /app/manage.py migrate

RUN npm install -g yarn 
RUN yarn install # --cwd /app

RUN npm install

ADD . /app

RUN yarn build

EXPOSE 80

