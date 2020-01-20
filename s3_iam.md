# S3 and IAM Assessment

1. 
[!log1](https://raw.githubusercontent.com/adityaprakash-bobby/q_pre_assessment/master/images/log_1.png)
[!log2](https://raw.githubusercontent.com/adityaprakash-bobby/q_pre_assessment/master/images/log_2.png)
[!log3](https://raw.githubusercontent.com/adityaprakash-bobby/q_pre_assessment/master/images/log_3.png)
[!log4](https://raw.githubusercontent.com/adityaprakash-bobby/q_pre_assessment/master/images/log_4.png)

2. 
```xml
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="https://static-audi.s3.amazonaws.com/">
<CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>PUT</AllowedMethod>
    <AllowedMethod>POST</AllowedMethod>
    <AllowedMethod>HEAD</AllowedMethod>
    <AllowedMethod>DELETE</AllowedMethod>
    <MaxAgeSeconds>3000</MaxAgeSeconds>
    <ExposeHeader>x-amz-server-side-encryption</ExposeHeader>
    <ExposeHeader>x-amz-request-id</ExposeHeader>
    <ExposeHeader>x-amz-id-2</ExposeHeader>
    <AllowedHeader>*</AllowedHeader>
</CORSRule>
</CORSConfiguration>
```
3.
[!lambda](https://raw.githubusercontent.com/adityaprakash-bobby/q_pre_assessment/master/images/s3_trigger_lambda.png)
