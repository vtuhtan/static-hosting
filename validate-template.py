#!/usr/bin/env python3
"""
Simple validation script for the static hosting SAM template.
Tests the CloudFront custom domain configuration by checking the raw template structure.
"""

import re
import sys
from typing import List

def load_template_text(template_path: str) -> str:
    """Load the template as raw text."""
    with open(template_path, 'r') as f:
        return f.read()

def validate_custom_domain_configuration(template_text: str) -> List[str]:
    """Validate custom domain configuration in the template."""
    errors = []
    
    # Check for required parameters
    required_params = ['domainName:', 'recordName:', 'certificateArn:', 'hostedZoneId:']
    for param in required_params:
        if param not in template_text:
            errors.append(f"Missing parameter: {param}")
    
    # Check for HasDomainName condition
    if 'HasDomainName:' not in template_text:
        errors.append("Missing HasDomainName condition")
    
    # Check that HasCustomDomain uses all three conditions
    if 'HasCustomDomain:' in template_text:
        # Look for the HasCustomDomain condition block
        has_custom_domain_match = re.search(r'HasCustomDomain:.*?(?=\n\w|\nGlobals|\nResources)', template_text, re.DOTALL)
        if has_custom_domain_match:
            condition_block = has_custom_domain_match.group(0)
            required_conditions = ['HasHostedZone', 'HasCertificate', 'HasDomainName']
            for condition in required_conditions:
                if condition not in condition_block:
                    errors.append(f"HasCustomDomain condition missing reference to {condition}")
    
    # Check CloudFront Aliases use domainName
    if 'Aliases:' in template_text:
        aliases_match = re.search(r'Aliases:.*?(?=\n        \w)', template_text, re.DOTALL)
        if aliases_match:
            aliases_block = aliases_match.group(0)
            if '${recordName}.${domainName}' not in aliases_block:
                errors.append("CloudFront Aliases should use ${recordName}.${domainName}")
    
    # Check DNS Record uses domainName
    if 'DNSRecord:' in template_text:
        dns_match = re.search(r'DNSRecord:.*?(?=\n  \w|\nOutputs)', template_text, re.DOTALL)
        if dns_match:
            dns_block = dns_match.group(0)
            if '${recordName}.${domainName}' not in dns_block:
                errors.append("DNS Record Name should use ${recordName}.${domainName}")
    
    # Check for CustomDomainUrl output
    if 'CustomDomainUrl:' not in template_text:
        errors.append("Missing CustomDomainUrl output")
    else:
        # Check that it's conditional
        custom_domain_url_match = re.search(r'CustomDomainUrl:.*?(?=\n  \w|\n$)', template_text, re.DOTALL)
        if custom_domain_url_match:
            output_block = custom_domain_url_match.group(0)
            if 'Condition: HasCustomDomain' not in output_block:
                errors.append("CustomDomainUrl output should have Condition: HasCustomDomain")
            if 'https://${recordName}.${domainName}' not in output_block:
                errors.append("CustomDomainUrl should use https://${recordName}.${domainName}")
    
    return errors

def main():
    """Main validation function."""
    template_path = 'template.yaml'
    
    try:
        template_text = load_template_text(template_path)
    except Exception as e:
        print(f"Error loading template: {e}")
        sys.exit(1)
    
    errors = validate_custom_domain_configuration(template_text)
    
    if errors:
        print("❌ Validation errors found:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("✅ Template validation passed - CloudFront custom domain configuration is correct")
        print("✅ Key features validated:")
        print("  - domainName parameter added")
        print("  - HasDomainName condition added")
        print("  - HasCustomDomain condition updated to include all requirements")
        print("  - CloudFront Aliases use recordName.domainName format")
        print("  - DNS Record uses recordName.domainName format")
        print("  - CustomDomainUrl output added with proper condition")
        sys.exit(0)

if __name__ == '__main__':
    main()