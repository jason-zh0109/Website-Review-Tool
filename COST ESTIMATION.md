# Cost Estimation Plan for Project Deployment on AWS

## Cost Breakdown

### 1. AWS Deployment Costs
For the first 12 months, many AWS services are covered under the **AWS Free Usage Tier**, significantly reducing initial costs:

- **Elastic Load Balancing**: 750 hours per month for 12 months (Global-LoadBalancerUsage)
- **Amazon Elastic Compute Cloud (EC2)**: 750 hours per month for 12 months (Global-BoxUsage:freetier.micro)
- **Amazon Virtual Private Cloud (VPC)**: 750 hours per month for 12 months for public IPv4 usage (Global-PublicIPv4:InUseAddress)
- **Amazon Relational Database Service (RDS)**: 750 hours per month for 12 months (Global-InstanceUsage:db.t1.micro)
- **AWS CodePipeline**: 100 minutes always free per month (Global-actionExecutionMinute)
- **AWS Data Transfer**: 1 GB always free per month (Global-DataTransfer-Regional-Bytes)
- **Amazon CloudWatch**: 10 alarms always free per month (Global-CW:AlarmMonitorUsage)
- **RDS Storage**: 20 GB per month for 12 months (Global-RDS:StorageUsage)
- **Amazon EC2 Elastic Block Store (EBS)**: 30 GB per month for 12 months (Global-EBS:VolumeUsage)
- **Amazon Simple Storage Service (S3)**: 2,000 requests per month for 12 months (Global-Requests-Tier1)

**Estimated Cost for AWS Deployment**:
- **First Year**: 18-20 AUD per month due to potential small costs such as public IPv4 addresses and data transfer exceeding free limits.
- **Main Cost Source**: The primary cost for AWS deployment comes from **$0.005 per In-use public IPv4 address per hour** when the free allocation is exceeded.

### 2. Custom Domain Name
- **Provider**: GoDaddy (Domain Names, Websites, Hosting & Online Marketing Tools - GoDaddy AU)
- **Estimated Cost**: Around 16 AUD per year for the first 3 years.

---

This plan outlines the AWS Free Tier services that will significantly reduce deployment costs during the first year, with an estimated monthly budget of 18-20 AUD, and includes the projected cost for a custom domain over three years.