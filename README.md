# LiteLLM Proxy Setup Guide

This repository demonstrates how to set up and configure LiteLLM, a lightweight library for working with Large Language Models (LLMs). In addition to the basic LiteLLM setup, this guide includes configurations for Redis caching and Langfuse logging.

## Table of Contents

1. [Introduction](#introduction)
2. [Basic LiteLLM Proxy Setup](#basic-litellm-proxy-setup)
3. [Redis Caching Configuration](#redis-caching-configuration)
4. [Langfuse Logging Configuration](#langfuse-logging-configuration)
5. [Usage](#usage)
6. [Test the setup with curl](#test-the-setup-with-curl)

## Introduction

LiteLLM is a powerful library that simplifies working with various LLM providers. This repository serves as a guide to help you set up LiteLLM and enhance its functionality with caching and logging capabilities.

The additional services are based on the Docker Containers, where they are running independently.

## Basic LiteLLM proxy Setup

```bash
pip install 'litellm[proxy]'
```

## Redis Caching Configuration

https://docs.litellm.ai/docs/proxy/caching

The basic idea is that you set up a redis server and then configure litellm to use it.

### Install Redis and set up the port 

```bash
docker run -d --name redis_server -p 6379:6379 redis
```

After the first run, this container will show up in the docker desktop. You can open or terminate the container with the docker desktop. Then the same query to the same model will return the cached result.


## Langfuse Logging Configuration

https://docs.litellm.ai/docs/proxy/logging#logging-proxy-inputoutput---langfuse

```bash
pip install langfuse>=2.0.0
```

### Prerequisites: Postgres Database

Install Postgres in MAC

```bash
# Install Postgres
brew install postgresql@14

# Start the server
brew services start postgresql

# create database for langfuse
createdb langfuse_db

# find the username 
whoami 
```

After this setup, the connection string is: `postgresql://[yourusername]@host.docker.internal:5432/langfuse_db`

`host.docker.internal` is used instead of `localhost` in your DATABASE_URL. This special DNS name is used by Docker for Mac to reference the host machine.

### Set up langfuse server

```bash
docker pull langfuse/langfuse:2.93.3

docker run --name langfuse \
-e DATABASE_URL=postgresql://[yourusername]@host.docker.internal:5432/langfuse_db \
-e NEXTAUTH_URL=http://localhost:3000 \
-e NEXTAUTH_SECRET=mysecret \
-e SALT=mysalt \
-e ENCRYPTION_KEY=0000000000000000000000000000000000000000000000000000000000000000 \ # generate via: openssl rand -hex 32
-p 3000:3000 \
-a STDOUT \
langfuse/langfuse:2.93.3
```

Then you can open the browser and go to http://localhost:3000/. Register a new account and setup a new organization and project. It will show the public key and secret key, which you will need to set in the environment variables.


## config file

the config file is `llm_config.yaml`. It is used to set up the models and the corresponding parameters for the litellm proxy.

To run:
```bash
litellm --config llm_config.yaml
```

However, there are several environment variables that need to be set. You can refer to the `launch_example.sh` script.

```bash
source launch_example.sh
```

## Usage

Essentailly the litellm proxy is just a proxy to the LLM providers. So you can use the same API endpoints to interact with the models.

You can use `curl`, `openai` or `anthropic` client to interact with the models. Notice the `LiteLLM SDK` is not recommended. Because  it has duplicate logic as the proxy also uses the sdk, which might lead to unexpected errors.

Therefore, the best practice is to use litellm proxy in a separated environment. As if it is a wrapper of all kinds of LLM providers, adding caching and logging capabilities. While in the main production repo, you can interact with the models as if it is a normal OpenAI client.


## Test the setup with curl

```bash

# test the chat completion
curl --location 'http://0.0.0.0:4000/chat/completions' \
--header 'Content-Type: application/json' \
--data ' {
      "model": "fireworks-llama-v3p1-70b-instruct",
      "messages": [
        {
          "role": "user",
          "content": "what llm are you"
        }
      ]
    }
'

# test the embedding
curl --location 'http://0.0.0.0:4000/embeddings' \
--header 'Content-Type: application/json' \
--data '{"input": ["Academia.edu uses"], "model": "fireworks-nomic-embed-text-v1.5"}'
```

You can also use the `example.py` to test the setup.
