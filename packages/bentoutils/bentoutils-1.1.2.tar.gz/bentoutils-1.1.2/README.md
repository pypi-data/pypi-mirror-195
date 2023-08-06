# bentoutils

## Contents

Console scripts for:

1. bentopack - package an existing pretrained model and save to the Model Registry

```
Usage: bentopack [OPTIONS]

Options:
  --module TEXT  fully qualified module name containing service to package
  --clz TEXT     class name of service to package
  --name TEXT    model name
  --path TEXT    directory path of pretrained model
  --help         Show this message and exit.
```

Example:
```
bentopack \
    --module TopicBentoService \        # python module containing service class
    --clz TopicBentoService \           # service class
    --name tm_train3_roberta_l_weigh \  # pretrained model name
    --path /srv/models/multilabel-topic # local path to pretrained model (excluding name)
```

2. deploy_to_knative - WIP


Uses Kaniko

kaniko is a tool to build container images from a Dockerfile, inside a container or Kubernetes cluster.

kaniko solves two problems with using the Docker-in-Docker build method:

* Docker-in-Docker requires privileged mode to function, which is a significant security concern.
* Docker-in-Docker generally incurs a performance penalty and can be quite slow.

The setting `--isdockerconfig` is required when using a private registry such as Harbor.

We can build a Docker image with kaniko and push it to Docker Hub or any other standard Docker registry.

To push to DockerHub or any other username and password Docker registries we need to mount the Docker config.json file that contains the credentials. Caching will not work for DockerHub as it does not support repositories with more than 2 path sections (acme/myimage/cache), but it will work in Artifactory and maybe other registry implementations.

    DOCKER_USERNAME=[...]
    DOCKER_PASSWORD=[...]
    AUTH=$(echo -n "${DOCKER_USERNAME}:${DOCKER_PASSWORD}" | base64)
    cat << EOF > config.json
    {
        "auths": {
            "https://index.docker.io/v1/": {
                "auth": "${AUTH}"
            }
        }
    }
    EOF

Alternatively, to create a secret to authenticate to Google Cloud Registry, follow these steps:

1. Create a service account in the Google Cloud Console project you want to push the final image to with Storage Admin permissions.
2. Download a JSON key for this service account
3. Rename the key to kaniko-secret.json
4. To create the secret, run:

    kubectl create secret generic kaniko-secret --from-file=<path to kaniko-secret.json>

Note: If using a GCS bucket in the same GCP project as a build context, this service account should now also have permissions to read from that bucket.

See https://github.com/GoogleContainerTools/kaniko

