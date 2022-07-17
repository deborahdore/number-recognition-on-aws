Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo systemctl enable docker
sudo gpasswd -a ec2-user docker
sudo grpck
sudo grpconv
newgrp docker
groups
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 883218126663.dkr.ecr.us-east-1.amazonaws.com
docker pull 883218126663.dkr.ecr.us-east-1.amazonaws.com/number-recognition-application:latest
docker run -d --restart on-failure:3 -p 5000:5000 883218126663.dkr.ecr.us-east-1.amazonaws.com/number-recognition-application:latest
--//--