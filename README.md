# Static Hosting SAM Template

A reusable SAM (Serverless Application Model) template for deploying static websites with CloudFront distribution, S3 bucket storage, and optional Route 53 DNS integration.

## Features

- S3 bucket configured for static website hosting
- CloudFront distribution for global content delivery
- Optional Route 53 DNS integration
- Secure access controls with Origin Access Control
- Cost-optimized caching strategies
- Consistent resource tagging

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `client` | String | Yes | Client identifier for resource tagging and naming |
| `websiteName` | String | Yes | Website name used for resource naming and subdomain |
| `hostedZoneId` | String | No | Route 53 hosted zone ID for DNS integration (leave empty to skip DNS) |
| `recordName` | String | No | Custom domain name for the website (defaults to "www") |

## Usage

### Deploy without DNS integration
```bash
sam deploy --parameter-overrides client=mycompany websiteName=mysite
```

### Deploy with DNS integration
```bash
sam deploy --parameter-overrides client=mycompany websiteName=mysite hostedZoneId=Z1234567890ABC
```

## Outputs

The template provides the following outputs:
- S3 bucket name for deployment
- CloudFront distribution domain name
- CloudFront distribution ID for cache invalidation
- Custom domain URL (when DNS is enabled)

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Route 53      │    │   CloudFront     │    │   S3 Bucket     │
│   (Optional)    │───▶│   Distribution   │───▶│   Static Files  │
│   DNS Record    │    │   CDN + Cache    │    │   + Assets/     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## License

MIT License