# Install
- CloudFormation provided by Databricks: [`AWS Cloudformation yaml`](attachments/aws-create-stack-databricks.yaml)
    - https://dbricks.co/AWSQuickStartHelp

AWS CloudFormation

<img src="attachments/databricks-create-workspace-aws-cloudformation.png" alt="drawing" width="1200"/>

Finish the setup on the AWS

<img src="attachments/databricks-finish-workspace-setup-aws.png" alt="drawing" width="1200"/>

Workspace created

<img src="attachments/databricks-first-workspace.png" alt="drawing" width="1200"/>

- [Manage your subscription and billing](https://docs.databricks.com/aws/en/admin/account-settings/account)

Workspace create without payment methods

<img src="attachments/databricks-account-settings-firts-no-pay.png" alt="drawing" width="1200"/> 

Add compute without credit card

<img src="attachments/databricks-add-compute-without-credit-card.png" alt="drawing" width="1200"/>

Adding credit card

<img src="attachments/databricks-add-credit-card.png" alt="drawing" width="1200"/>

Selecting the Free Personal account and work account

<img src="attachments/databricks-login-2-accounts.png" alt="drawing"/>

# Create a personal Databricks compute
```shell
databricks clusters list
```

```shell
databricks ssh setup --name low-cost --cluster 0626-121515-spu2v7yo  --auto-start-cluster=false
```

# Configure a customer-manage VPC
 - [Customer managed VPC](https://docs.databricks.com/aws/en/security/network/classic/customer-managed-vpc)
	 - [Security groups](https://docs.databricks.com/aws/en/security/network/classic/customer-managed-vpc#security-groups)

<img src="attachments/databricks-setup-change-network-configuration.png" alt="drawing"/>
