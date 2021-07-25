FROM selenium/node-chrome:4.0.0-beta-1-20210215 as selenium
LABEL authors=SeleniumHQ

USER 1200

#====================================
# Scripts to run Selenium Standalone
#====================================
COPY start-selenium-standalone.sh /opt/bin/start-selenium-standalone.sh

#==============================
# Supervisor configuration file
#==============================
COPY selenium.conf /etc/supervisor/conf.d/

EXPOSE 4444

# Base image
FROM python:3.8

RUN apt-get update && \
      apt-get -y install sudo
RUN apt-get install -y wget \
			gnupg2

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - &&\
sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' &&\
sudo apt-get update --fix-missing
RUN sudo apt-get install -y google-chrome-stable

RUN apt-get update && apt-get install -yq \
    chromium \
    git-core \
    xvfb \
    unzip \
    libgconf-2-4 \
    libncurses5 \
    libxml2-dev \
    libxslt-dev \
    libz-dev \
    xclip \
		vim

# chromeDriver v2.35
#RUN wget -q "https://chromedriver.storage.googleapis.com/2.5/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
RUN wget -q "https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /usr/bin/ \
    && rm /tmp/chromedriver.zip

# xvfb - X server display
ADD xvfb-chromium /usr/bin/xvfb-chromium
#RUN ln -s /usr/bin/xvfb-chromium /usr/bin/google-chrome \
#    && chmod 777 /usr/bin/xvfb-chromium

# create symlinks to chromedriver and geckodriver (to the PATH)
#RUN ln -s /usr/bin/chromium-browser \
#    && chmod 777 /usr/bin/chromium-browser

#COPY --from=selenium /usr/bin/chromedriver /usr/bin/chromedriver

# Working directory
WORKDIR /CatchTheWave
ENV PATH="/usr/bin/chromedriver:${PATH}" 


# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy content of the local src directory to the working directory
COPY data/ data/
COPY plots/ plots/
COPY src/ src/

# Command to run on container start
RUN [ "python", "./src/stocks__evaluation.py" ]
#RUN ["bash" ]
