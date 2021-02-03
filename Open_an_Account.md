# Opening an AWS account
Obviously you will need an AWS account. AWS has a [free tier](https://aws.amazon.com/free/) including 1 million free lambda requests per month. Though it's free, you'll still need a credit card to sign up and will need to go through the verification process to open your account.

Steps:
- Ensure you have a password manager! [Bitwarden](https://bitwarden.com/download/) is recommended if you don't have one.
- Ensure you have a two factor authentication app on your phone (google authenticator, authy, duo are all good places to start)
- Ensure you can receive a phone call. AWS will call you and require you to type in a verification code during the process.
- Follow the [SANS guide](https://www.sans.org/media/security-training/laptop/Creating_your_SEC545_AWS_Account.pdf) to open your [AWS account]( https://portal.aws.amazon.com/billing/signup)

Modifications from the SANS guide:
- Have your password manager create and store all credentials
- Don't follow the 'close your account' process unless you'd actually like to close your account (don't know why that's listed as one of the first sections)
- Use whatever username you'd like (instead of the SANS SEC545 user from the class)
- Keep in mind your AWS account name (created at during the "Create an AWS Account" step) is not your AWS alias (optional to create during the "Create an AWS User" step by customizing your IAM users sign-in link)
- Don't worry about installing VMware (listed on the last page)

At the end you'll have:
- A dedicated AWS account
- A root user and an IAM user in your password manager
- MFA enabled for all users


## References
AWS Documentation:
https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/

Video:
https://youtu.be/v3WLJ_0hnOU
