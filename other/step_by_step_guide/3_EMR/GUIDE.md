# Guide for the creation of the EMR cluster

1. Go to AWS Emr
2. Select _create cluster_
3. Follow the [configuration](m5.xlarge/conf) instructions
5. Wait for the cluster to be in _Waiting mode_ (it may take up to 15 minutes)
6. Change Master's node security rules:
    1. Go to the _Summary_ page of the cluster
    2. Go down until you find _Security and access_
    3. Click on the security group of the master node
    4. Click on the _Security group ID_ of the master node
    5. Edit _inbound rules_
    6. Add a rule for the connection through SSH from _Anywhere IPv4_
    7. Save
7. Connect to the cluster via SSH with the pre-generated key using the following command:
    1. `ssh -i lab-key.pem <master-public-DNS>`
    2. The DNS of the master node is shown in the summary page of the cluster
8. Copy the [main.py](../../../spark-job/main.py) file from the s3 storage:
    1. `aws s3 cp s3://<s3-BUCKET-NAME>/main.py .`
    2. `spark-submit main.py`
