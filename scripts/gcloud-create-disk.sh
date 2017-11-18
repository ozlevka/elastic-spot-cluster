#!/bin/bash -x

if [ -z "$CLUSTER_ZONE" ]; then
    CLUSTER_ZONE="us-east1-c"
fi


gcloud compute \
    --project="ozlevka" \
    disks create "disk-for-1" \
    --zone="$CLUSTER_ZONE" \
    --type="pd-standard" \
    --size=50GB