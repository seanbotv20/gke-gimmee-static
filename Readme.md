# GKE Gimmee Static

A script and docker image to add a specific static IP to a GCP compute instance, especially in a GKE cluster context.

Me save money on load balancers by abusing this and nodePort exposed services.

### Prerequisites

### Installing

This project comes with a Pipfile suitable for use with `pipenv`:

```bash
pipenv install
```

You must also provide a [valid form of google authentication](https://cloud.google.com/docs/authentication/getting-started).

## Running

This script is configured using the following environment variables:
|Environment Variable | Description                                                                          |
|:-------------------- | :------------------------------------------------------------------------------------ |
| IP_ADDRESS           | A valid static ip address you in the same project and region as the compute instance |
| INSTANCE_ID          | _(optional)_ ID of the compute instance to which you wish to attach the static IP    |
| PROJECT              | _(optional)_ Name of the project where the compute instance exists                   |
| ZONE                 | _(optional)_ Name of the zone where the compute instance exists                      |

If any of the optional variables are missing, the values will be obtained from the [compute metadata server](https://cloud.google.com/compute/docs/storing-retrieving-metadata).

## Deployment

This script is already built and packaged as a [docker image](https://hub.docker.com/repository/docker/seanbot/gke-gimmee-static) on dockerhub.

If deploying on a compute instance in GCP, ensure the instance has the metadata server enabled, and has write access to the Compute API.

## License

This project is unlicensed and for the most part unsupported.