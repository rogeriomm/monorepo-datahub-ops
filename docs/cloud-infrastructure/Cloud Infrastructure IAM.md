

| User          | ARN                                                | Group          |
| ------------- | -------------------------------------------------- | -------------- |
| star          | *arn:aws:iam::586117210061:user/star*              | Development    |
| administrator | *arn:aws:iam::586117210061:user/administrator*<br> | Administrators |


| Group          | ARN  | IAM policy                                                   |
| -------------- | ---- | ------------------------------------------------------------ |
| Developers     |      | *mfa*                                                        |
| Administrators | <br> | *mfa*, *AdministratorAccess*, <br>*AWSBillingReadOnlyAccess* |
|                |      |                                                              |




 - Create a IAM policy named *mfa*
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListMFAInformation",
      "Effect": "Allow",
      "Action": [
        "iam:ListMFADevices",
        "iam:ListVirtualMFADevices"
      ],
      "Resource": "*"
    },
    {
      "Sid": "CreateOwnVirtualMFADevice",
      "Effect": "Allow",
      "Action": [
        "iam:CreateVirtualMFADevice"
      ],
      "Resource": "arn:aws:iam::*:mfa/${aws:username}"
    },
    {
      "Sid": "ManageOwnMFADevice",
      "Effect": "Allow",
      "Action": [
        "iam:EnableMFADevice",
        "iam:ResyncMFADevice",
        "iam:DeactivateMFADevice"
      ],
      "Resource": "arn:aws:iam::*:user/${aws:username}"
    },
    {
      "Sid": "DeleteOwnVirtualMFADevice",
      "Effect": "Allow",
      "Action": [
        "iam:DeleteVirtualMFADevice"
      ],
      "Resource": "arn:aws:iam::*:mfa/${aws:username}"
    }
  ]
}
```


![[Pasted image 20260728170732.png|1363]]
![[Pasted image 20260728170854.png|1361]]
![[Pasted image 20260728170949.png|1363]]