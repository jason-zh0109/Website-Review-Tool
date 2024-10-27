We have successfully implemented an auto-deployment pipeline for our website review tool using a combination of **AWS CodePipeline**, **Elastic Beanstalk (EB)**, and **RDS (MySQL)**. **AWS CodePipeline** automates the deployment process by pulling the latest code from our GitHub repository, while **AWS Elastic Beanstalk** handles the deployment and management of the application environment. The **RDS (MySQL)** database is integrated to store and manage data for the application. With this setup, our tool is automatically deployed whenever new commits are made to the designated branch, streamlining the deployment process. A detailed explanation of the steps involved in setting up this pipeline is provided below.

## 🏗️ Setups for EB, RDS and IAM

- **Reference**: <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.rolling-version-deploy.html> 

#### 1. **Preparation**

- **Ensure Environment Variables**: 

  Before deployment, confirm that all necessary environment variables, such as database credentials, AWS keys, and other sensitive information, are properly configured. Use AWS EB's console or `eb setenv` to set these variables securely.

- **Set Up AWS RDS (MySQL)**:

  Make sure your MySQL database is up and running on AWS RDS.

  Configure RDS security groups to allow inbound connections from your EB instance.

  Note down the database endpoint, username, password, and database name, as these will be required during deployment.

- ##### Set Up IAM Users

  ##### Create User Groups and Add Permissions

  - **Attach Policies**:

    **AdministratorAccess**

    **AdministratorAccess-AWSElasticBeanstalk**

    **AmazonEC2FullAccess**

    **AmazonS3FullAccess**
  - **Create Inline Policies**:

    **Elastic Beanstalk Service**:
    - **Action**: `CreateApplication`

    **S3 Service**:
    - **Action**: `GetBucketOwnershipControls`

  ##### Create Users and Add Users to the User Group

  ##### **Create Users:**

  Create users and add them to the user group with **AdministratorAccess** for the user you created.

  **Create Access Keys**:

  Create access keys for users under **Security credentials**.

  **Download CSV File**:

  Download the CSV file that would be used for accessing the EB console.

#### 2. **Create a Database in RDS (If Not Already Done)**

- **Create RDS Instance**:

  Launch an RDS instance with MySQL as the DB engine.

  Ensure you configure the VPC and security group to allow Elastic Beanstalk to communicate 			with your RDS instance.
- **Configure Database**:

  Log in to your RDS instance using a MySQL client and set up the necessary database schema and tables by running migration scripts if needed.

#### 3. **Configure Application for RDS**

In your application configuration, update the database connection details to point to your AWS RDS instance. Make sure to set up the following:
- **Host**: RDS endpoint
- **User**: Database username
- **Password**: Database password
- **DB Name**: The name of your database
- **Port**: Default MySQL port (3306)

#### 4. **Prepare Elastic Beanstalk Configuration**

- **Initialize Elastic Beanstalk**:

  Run the command pip install awsebcli to enable execution of eb commands in console

  If it's your first deployment, run eb init to configure your Elastic Beanstalk environment. This command will guide you through setting up the region, platform, and other necessary configurations.

  Select the appropriate environment (e.g., Python, Node.js) for your project.

- **Update the EB Configuration**:

  If needed, modify the .elasticbeanstalk/config.yml to ensure your instance type, environment, and deployment policies are correct for production use.

#### 5. **Deploy Application to AWS Elastic Beanstalk**

- **Push Code to GitHub**:

  Make sure your code is committed and pushed to GitHub, following the branching strategy mentioned previously.
- **Run Deployment**:

  Once the code is prepared, run eb create <environment-name> for the first deployment or eb deploy for subsequent deployments.

  Elastic Beanstalk will automatically handle the provisioning of resources, including creating the EC2 instances, configuring load balancers, and setting up the application environment.
- **Monitor Deployment**:

  You can monitor the deployment logs and status using eb logs or by accessing the AWS Management Console.

  Check the EB environment health to ensure everything is functioning properly.

#### **6. Enabling HTTPS for AWS Deployment** 

- **Obtain an SSL Certificate**:

  Log in to the AWS Management Console.

  Navigate to AWS Certificate Manager (ACM).

  Request a public certificate. You need to provide your domain name (e.g., `example.com` and `*.example.com`).

  Complete the validation process (usually via DNS validation).

- **Configure Elastic Load Balancer (ELB)**:

  Navigate to the EC2 Console.

  Select your load balancer.

  In the "Listeners" tab, add a new HTTPS listener.

  Select the SSL certificate you created in ACM.

  Configure ELB to forward HTTPS requests to your application instances.

- **Update DNS Records**:

  Navigate to your DNS provider (e.g., Route 53).

  Update your domain records to point to the ELB's DNS name.

#### 7. **Post-Deployment Steps**

- **Database Migrations**:

  If there are any new migrations required after deployment, run them on your RDS instance via SSH or a MySQL client.
- **Environment Validation**:

  Once deployed, ensure that the application can connect to RDS and verify that the application is stable and fully functional.

#### 8. **Scaling and Monitoring**

- **Auto-scaling**:

  AWS Elastic Beanstalk can auto-scale the application based on load. Configure the auto-scaling policies in the EB environment settings.
- **Logging and Monitoring**:

  Use AWS CloudWatch and EB logs to monitor the application’s performance and resource usage. Set up alerts if necessary.

#### 9. **Rollback Strategy**

- **In Case of Failure**:

  If a deployment fails or issues are detected, you can roll back to the previous stable version using the eb restore command or by manually deploying the previous version from your GitHub repository.
- **Database Backups**:

  Regularly back up the RDS database using automated snapshots or manual backups in case data restoration is required.



## 🏗️ Setups for AWS CodePipeline

**Reference**: <https://faun.pub/how-to-create-cicd-using-github-as-source-and-elastic-beanstalk-244319a2a350> 

1. **Create a New Pipeline**:

   Navigate to the AWS Management Console and click on **Services**.

   In the search bar, type **CodePipeline** and select it from the results.

   Click **Create a New Pipeline** to begin the setup.
2. **Configure Source Provider**:

   For the **Source Provider**, choose **GitHub**.

   Click **Connect to GitHub** and follow the instructions to link your GitHub account. This connection will use webhooks to automatically trigger the pipeline whenever new commits are pushed.

   Select the appropriate GitHub repository and branch (e.g., master or stable) from which the pipeline should fetch the latest code.
3. **Skip Build Stage (Optional)**:

   On the next screen, click **Skip Build** if you're not integrating unit tests or linting in this pipeline.

   If you want to add a testing stage, use **CodeBuild**, which checks for a buildspec.yml file in the root folder of your repository. For now, we are skipping this step.
4. **Deploy Stage Configuration**:

   For the **Deploy Stage**, select **AWS Elastic Beanstalk**.

   In the **Application Name** dropdown, select the Beanstalk application you previously created.

   In the **Environment Name**, select the environment associated with your application (e.g., Production or Development).
5. **Review and Create Pipeline**:

   Click **Next**, review the pipeline configuration, and ensure all details are correct.

   Once satisfied, click **Create Pipeline**. If everything is correctly set up, you should see messages indicating the pipeline stages are **SUCCEEDED**.
6. **Verify EC2 Instance**:

   To check the status of your deployed application, return to **Services** in the AWS Console and search for **EC2**.

   Select **EC2** to view the running instances created by Elastic Beanstalk.

   Copy the **Public DNS** of the instance and open it in a browser to verify that your application is live and running.  

## FAQ

- For nginx timeout problem meet during running deployment, please refer to this https://stackoverflow.com/questions/49137188/aws-elastic-beanstalk-504-gateway-timeout
- For error "Command 'pkg-config --exists mysqlclient' returned non-zero exit status 1." reported in eb log, please refer to [mysql python - Mysqlclient cannot install via pip, cannot find pkg-config name in Ubuntu - Stack Overflow](https://stackoverflow.com/questions/76585758/mysqlclient-cannot-install-via-pip-cannot-find-pkg-config-name-in-ubuntu) 
- For error "no such table: auth_user" happened on login, please refer to (https://stackoverflow.com/questions/24682155/user-registration-with-error-no-such-table-auth-user)



