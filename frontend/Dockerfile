FROM node:lts
# RUN mkdir /app && /app
# RUN mkdir /app/node_modules && chown node:node /app/node_modules
WORKDIR /app
RUN npm install -g @angular/cli

# USER node
COPY package.json package-lock.json* ./
RUN npm install 
#ci --quiet
COPY . .

# EXPOSE 4200



# FROM node:20 as builder 
# # bullseye-slim

# WORKDIR /usr/src/app

# # RUN npm install -g @angular/cli@13

# COPY package.json /usr/src/app
# RUN npm install

# COPY . .
# EXPOSE 4200
# CMD ["ng", "serve", "--host", "0.0.0.0"]

# FROM builder as dev-envs

# RUN <<EOF
# apt-get update
# apt-get install -y --no-install-recommends git
# EOF

# RUN <<EOF
# useradd -s /bin/bash -m vscode
# groupadd docker
# usermod -aG docker vscode
# EOF
# # install Docker tools (cli, buildx, compose)
# COPY --from=gloursdocker/docker / /

# CMD ["ng", "serve", "--host", "0.0.0.0"]