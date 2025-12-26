# Custom Domain Setup for Static Hosting Template

## Overview

The static hosting SAM template now supports custom domain configuration for CloudFront distributions. This allows you to serve your static website through your own domain name instead of the default CloudFront domain.

## Required Parameters for Custom Domain

To enable custom domain support, you need to provide the following parameters:

1. **hostedZoneId** - The Route 53 hosted zone ID where your domain is managed
2. **domainName** - Your domain name (e.g., "example.com")
3. **recordName** - The subdomain/record name (e.g., "www" for www.example.com)
4. **certificateArn** - SSL certificate ARN from AWS Certificate Manager (must be in us-east-1 region)

## Example Usage

### With Custom Domain
```bash
sam deploy \
  --parameter-overrides \
    client=mycompany \
    websiteName=mysite \
    hostedZoneId=Z1234567890ABC \
    domainName=example.com \
    recordName=www \
    certificateArn=arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012
```

This will create:
- CloudFront distribution with alias: `www.example.com`
- Route 53 A record: `www.example.com` → CloudFront distribution
- SSL certificate configured for HTTPS

### Without Custom Domain
```bash
sam deploy \
  --parameter-overrides \
    client=mycompany \
    websiteName=mysite
```

This will create:
- CloudFront distribution with default CloudFront domain only
- No DNS records created
- Default CloudFront SSL certificate

## Key Features Implemented

1. **Conditional Domain Configuration**: Custom domain features are only enabled when all required parameters are provided
2. **SSL Certificate Support**: Automatic HTTPS configuration with your SSL certificate
3. **DNS Integration**: Automatic Route 53 record creation pointing to CloudFront
4. **Flexible Naming**: Support for any subdomain + domain combination
5. **Output Values**: Template outputs the custom domain URL when configured

## Conditions Logic

The template uses the following conditions:
- `HasHostedZone`: Checks if hostedZoneId is provided
- `HasCertificate`: Checks if certificateArn is provided  
- `HasDomainName`: Checks if domainName is provided
- `HasCustomDomain`: All three conditions must be true

## Outputs

When custom domain is configured, the template provides:
- `CustomDomainUrl`: The full HTTPS URL (e.g., https://www.example.com)
- `DistributionDomainName`: The CloudFront domain (always available)
- `DistributionId`: For cache invalidation operations

## Prerequisites

1. **Domain in Route 53**: Your domain must be managed by Route 53
2. **SSL Certificate**: Must be created in AWS Certificate Manager in us-east-1 region
3. **Certificate Validation**: Certificate must be validated and issued before deployment

## Validation

Run the included validation script to verify the template configuration:
```bash
python validate-template.py
```

This validates that all custom domain configuration is properly set up in the template.