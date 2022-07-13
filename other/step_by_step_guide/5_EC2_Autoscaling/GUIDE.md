# Guide to the configuration of EC2

1. Go to the EC2 Dashboard
2. From the menu on the left select _Security Group_
3. Create new Security Group following the [configurations](security_group.pdf)
4. From the menu on the left select _Launch Templates_
5. Create new Launch template following the [configurations](Launch%20template%20configuration.pdf)
    1. remember to add the [user data](user-data.sh)
6. From the menu on the left select _Autoscaling group_
7. Create a new [Autoscaling](Autoscaling%20group.pdf) group using the template preconfigured
8. Wait for the EC2 instances specified to be up and running
9. From the menu on the left select _Load Balancers_
10. Add Listener for port 80 and redirect to the Autoscaling group just created
11. Add Listener for port 5000 and redirect to the Autoscaling group just created
12. Save Load Balancer DNS name and search it (IT'S HTTP, NOT HTTPS.
    es http://autoscaling-version2-1-1872856581.us-east-1.elb.amazonaws.com/)


