#!/bin/bash -x

gcloud beta compute --project "ozlevka" \
    instances create "cluster-1" \
    --zone "us-central1-f" \
    --machine-type "n1-standard-2" \
    --network "default" \
    --no-restart-on-failure \
    --maintenance-policy "TERMINATE" \
    --preemptible \
    --service-account "228176938798-compute@developer.gserviceaccount.com" \
    --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring.write","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" \
    --min-cpu-platform "Automatic" \
    --disk "name=disk-for-1,device-name=disk-for-1,mode=rw,boot=no" \
    --image "ubuntu-1604-xenial-v20171116" \
    --image-project "ubuntu-os-cloud" \
    --boot-disk-size "10" \
    --boot-disk-type "pd-standard" \
    --boot-disk-device-name "cluster-1"