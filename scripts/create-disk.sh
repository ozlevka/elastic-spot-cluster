#!/bin/bash -x

gcloud compute \
    --project="ozlevka" \
    disks create "disk-for-1" \
    --zone="us-central1-f" \
    --type="pd-standard" \
    --size=50GB