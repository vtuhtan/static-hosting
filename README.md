# Static Hosting SAM Template

A reusable SAM (Serverless Application Model) template for deploying static websites with CloudFront distribution, S3 bucket storage, and optional Route 53 DNS integration.

## Features

- S3 bucket configured for static website hosting
- CloudFront distribution for global content delivery
- Optional Route 53 DNS integration with SSL certificate support
- Secure access controls with Origin Access Control
- Cost-optimized caching strategies with separate behaviors for assets
- Consistent resource tagging across all components
- Security headers and content compression
- Custom error pages and HTTPS enforcement

## Resource Tagging

All resources are automatically tagged with:
- **Client**: Value from the `client` parameter
- **WebsiteName**: Value from the `websiteName` parameter  
- **Purpose**: StaticHosting
- **ManagedBy**: SAMTemplate
- **Environment**: Production

These tags help with cost allocation, resource management, and compliance tracking.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `client` | String | Yes | - | Client identifier for resource tagging and naming (1-50 chars, alphanumeric and hyphens only) |
| `websiteName` | String | Yes | - | Website name used for resource naming and subdomain (1-50 chars, alphanumeric and hyphens only) |
| `hostedZoneId` | String | No | "" | Route 53 hosted zone ID for DNS integration (leave empty to skip DNS setup) |
| `recordName` | String | No | "www" | Subdomain name for the website (e.g., 'www' for www.example.com) |
| `domainName` | String | No | "" | Domain name for custom domain (e.g., 'example.com' - required when using DNS integration) |
| `certificateArn` | String | No | "" | SSL certificate ARN for custom domain (must be in us-east-1 region - required when using DNS integration) |

### Parameter Dependencies

For **DNS integration**, you need to provide all three DNS-related parameters:
- `hostedZoneId`: Your Route 53 hosted zone ID
- `domainName`: Your domain name (e.g., 'example.com')
- `certificateArn`: SSL certificate ARN from AWS Certificate Manager (must be in us-east-1 region for CloudFront)

**Without DNS integration**, you can omit all DNS parameters or leave them empty.

## Usage

### Deploy without DNS integration
```bash
sam deploy --parameter-overrides client=mycompany websiteName=mysite
```

### Deploy with DNS integration
```bash
sam deploy --parameter-overrides \
  client=mycompany \
  websiteName=mysite \
  hostedZoneId=Z1234567890ABC \
  domainName=example.com \
  certificateArn=arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012
```

### Deploy with custom subdomain
```bash
sam deploy --parameter-overrides \
  client=mycompany \
  websiteName=mysite \
  recordName=blog \
  hostedZoneId=Z1234567890ABC \
  domainName=example.com \
  certificateArn=arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012
```

### Prerequisites for DNS Integration

Before deploying with DNS integration, ensure you have:

1. **Route 53 Hosted Zone**: A hosted zone for your domain in Route 53
2. **SSL Certificate**: An SSL certificate issued by AWS Certificate Manager in the **us-east-1** region (required for CloudFront)
3. **Domain Ownership**: Verified ownership of the domain

To create an SSL certificate:
```bash
aws acm request-certificate \
  --domain-name example.com \
  --subject-alternative-names "*.example.com" \
  --validation-method DNS \
  --region us-east-1
```

## Outputs

The template provides the following outputs:

| Output | Description | When Available |
|--------|-------------|----------------|
| `BucketName` | S3 bucket name for deployment | Always |
| `DistributionDomainName` | CloudFront distribution domain name | Always |
| `DistributionId` | CloudFront distribution ID for cache invalidation | Always |
| `CustomDomainUrl` | Custom domain URL (e.g., https://www.example.com) | Only when DNS integration is enabled |

### Using Outputs

After deployment, you can reference these outputs in other stacks or retrieve them using:

```bash
# Get all outputs
aws cloudformation describe-stacks --stack-name your-stack-name --query 'Stacks[0].Outputs'

# Get specific output
aws cloudformation describe-stacks --stack-name your-stack-name --query 'Stacks[0].Outputs[?OutputKey==`BucketName`].OutputValue' --output text
```

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Route 53      │    │   CloudFront     │    │   S3 Bucket     │
│   (Optional)    │───▶│   Distribution   │───▶│   Static Files  │
│   DNS Record    │    │   CDN + Cache    │    │   + Assets/     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Troubleshooting

### Common Issues

**Certificate not found error**
- Ensure the SSL certificate is created in the `us-east-1` region (required for CloudFront)
- Verify the certificate ARN format is correct
- Make sure the certificate is validated and issued

**DNS record creation fails**
- Verify the hosted zone ID is correct
- Ensure you have permissions to modify the Route 53 hosted zone
- Check that the domain name matches the hosted zone

**S3 bucket name conflicts**
- S3 bucket names are globally unique
- The template uses `{client}-{websiteName}-static-hosting-{AccountId}` format
- Try different client or websiteName values if conflicts occur

**CloudFront distribution takes time to deploy**
- CloudFront distributions typically take 15-20 minutes to deploy
- Wait for the distribution status to change from "In Progress" to "Deployed"

### Cache Invalidation

After updating your website content, you may need to invalidate the CloudFront cache:

```bash
aws cloudfront create-invalidation \
  --distribution-id YOUR_DISTRIBUTION_ID \
  --paths "/*"
```

Use the `DistributionId` output from the stack for the distribution ID.

## License

MIT License