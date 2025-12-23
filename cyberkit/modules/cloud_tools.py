"""
Cloud Security Tools - AWS/Azure/GCP Enumeration
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *
from utils.helpers import *

class CloudTools:
    def __init__(self):
        self.output_dir = create_output_dir("output/cloud")
    
    def show_menu(self):
        while True:
            clear_screen()
            print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                  CLOUD SECURITY TOOLS                        ║
╠══════════════════════════════════════════════════════════════╣{Colors.END}
║   {Colors.CYAN}[1]{Colors.END}  S3 Bucket Scanner                                  ║
║   {Colors.CYAN}[2]{Colors.END}  S3 Bucket Bruteforce                               ║
║   {Colors.CYAN}[3]{Colors.END}  Azure Blob Enumeration                             ║
║   {Colors.CYAN}[4]{Colors.END}  GCP Bucket Enumeration                             ║
║   {Colors.CYAN}[5]{Colors.END}  Subdomain to Cloud Check                           ║
║   {Colors.CYAN}[6]{Colors.END}  Cloud Metadata Check                               ║
║   {Colors.CYAN}[7]{Colors.END}  AWS CLI Enumerate                                  ║
║   {Colors.CYAN}[8]{Colors.END}  Cloud Credential Checker                           ║
║   {Colors.RED}[0]{Colors.END}  Back                                               ║
{Colors.CYAN}╚══════════════════════════════════════════════════════════════╝{Colors.END}
            """)
            choice = get_input("  Select")
            if choice == "0": break
            elif choice == "1": self.s3_scanner()
            elif choice == "2": self.s3_bruteforce()
            elif choice == "3": self.azure_blob()
            elif choice == "4": self.gcp_bucket()
            elif choice == "5": self.subdomain_cloud()
            elif choice == "6": self.metadata_check()
            elif choice == "7": self.aws_enum()
            elif choice == "8": self.cred_checker()

    def s3_scanner(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  S3 BUCKET SCANNER{Colors.END}\n")
        bucket = get_input("  Bucket name")
        if not bucket: return
        
        urls = [
            f"https://{bucket}.s3.amazonaws.com",
            f"https://s3.amazonaws.com/{bucket}",
            f"https://{bucket}.s3-us-west-2.amazonaws.com",
        ]
        
        for url in urls:
            print_info(f"  Checking: {url}")
            stdout, _, rc = run_command(f"curl -s -I {url}")
            if "200 OK" in stdout:
                print_success(f"    PUBLIC ACCESS!")
            elif "403" in stdout:
                print_warning(f"    Exists but forbidden")
            elif "404" in stdout:
                print_error(f"    Not found")
        
        # Try listing
        print_info(f"\n  Trying to list contents...")
        stdout, _, _ = run_command(f"curl -s https://{bucket}.s3.amazonaws.com")
        if "<Contents>" in stdout or "<Key>" in stdout:
            print_success("  Bucket is LISTABLE!")
            print(stdout[:500])
        
        input("\n  Press Enter...")

    def s3_bruteforce(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  S3 BUCKET BRUTEFORCE{Colors.END}\n")
        company = get_input("  Company/keyword")
        if not company: return
        
        permutations = [
            company, f"{company}-backup", f"{company}-dev", f"{company}-prod",
            f"{company}-staging", f"{company}-test", f"{company}-data",
            f"{company}-files", f"{company}-assets", f"{company}-media",
            f"{company}-logs", f"{company}-db", f"{company}-database",
            f"backup-{company}", f"dev-{company}", f"prod-{company}",
        ]
        
        print(f"\n  Testing {len(permutations)} bucket names...\n")
        found = []
        
        for bucket in permutations:
            url = f"https://{bucket}.s3.amazonaws.com"
            stdout, _, _ = run_command(f"curl -s -o /dev/null -w '%{{http_code}}' {url}")
            code = stdout.strip()
            
            if code == "200":
                print_success(f"  {bucket} - PUBLIC!")
                found.append((bucket, "PUBLIC"))
            elif code == "403":
                print_warning(f"  {bucket} - EXISTS (forbidden)")
                found.append((bucket, "EXISTS"))
            else:
                print(f"  {Colors.GRAY}{bucket} - not found{Colors.END}")
        
        if found:
            outfile = f"{self.output_dir}/s3_{company}_{get_timestamp()}.txt"
            with open(outfile, 'w') as f:
                for b, s in found: f.write(f"{b},{s}\n")
            print_success(f"\n  Saved: {outfile}")
        
        input("\n  Press Enter...")

    def azure_blob(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  AZURE BLOB ENUMERATION{Colors.END}\n")
        storage = get_input("  Storage account name")
        if not storage: return
        
        containers = ["data", "files", "backup", "logs", "assets", "public", "media", "images"]
        
        print(f"\n  Testing containers on {storage}...\n")
        
        for container in containers:
            url = f"https://{storage}.blob.core.windows.net/{container}?restype=container&comp=list"
            stdout, _, _ = run_command(f"curl -s -o /dev/null -w '%{{http_code}}' {url}")
            
            if stdout.strip() == "200":
                print_success(f"  {container} - PUBLIC!")
            elif stdout.strip() == "404":
                print(f"  {Colors.GRAY}{container} - not found{Colors.END}")
            else:
                print_warning(f"  {container} - exists (code: {stdout.strip()})")
        
        input("\n  Press Enter...")

    def gcp_bucket(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  GCP BUCKET ENUMERATION{Colors.END}\n")
        bucket = get_input("  Bucket name")
        if not bucket: return
        
        url = f"https://storage.googleapis.com/{bucket}"
        print_info(f"  Checking: {url}")
        
        stdout, _, _ = run_command(f"curl -s {url}")
        if "NoSuchBucket" in stdout:
            print_error("  Bucket not found")
        elif "AccessDenied" in stdout:
            print_warning("  Exists but access denied")
        else:
            print_success("  Bucket accessible!")
            print(stdout[:500])
        
        input("\n  Press Enter...")

    def subdomain_cloud(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  SUBDOMAIN CLOUD CHECK{Colors.END}\n")
        domain = get_input("  Domain")
        if not domain: return
        
        print_info("  Checking CNAME records for cloud services...")
        
        stdout, _, _ = run_command(f"dig {domain} CNAME +short")
        if stdout.strip():
            cname = stdout.strip()
            print(f"  CNAME: {cname}")
            
            if "s3" in cname or "amazonaws" in cname:
                print_success("  → AWS S3 detected!")
            elif "blob.core.windows" in cname:
                print_success("  → Azure Blob detected!")
            elif "storage.googleapis" in cname:
                print_success("  → GCP Storage detected!")
            elif "cloudfront" in cname:
                print_success("  → AWS CloudFront detected!")
            elif "azurewebsites" in cname:
                print_success("  → Azure Web App detected!")
        else:
            print_info("  No CNAME found")
        
        input("\n  Press Enter...")

    def metadata_check(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  CLOUD METADATA CHECK{Colors.END}\n")
        print_warning("  Use this on a compromised cloud instance\n")
        
        endpoints = [
            ("AWS", "http://169.254.169.254/latest/meta-data/"),
            ("AWS IAM", "http://169.254.169.254/latest/meta-data/iam/security-credentials/"),
            ("GCP", "http://metadata.google.internal/computeMetadata/v1/"),
            ("Azure", "http://169.254.169.254/metadata/instance?api-version=2021-02-01"),
            ("DigitalOcean", "http://169.254.169.254/metadata/v1/"),
        ]
        
        print(f"  {Colors.BOLD}Metadata Endpoints:{Colors.END}\n")
        for name, url in endpoints:
            print(f"  {Colors.CYAN}{name}:{Colors.END}")
            print(f"    {url}\n")
        
        if confirm("\n  Try to reach AWS metadata?"):
            stdout, _, _ = run_command("curl -s --max-time 3 http://169.254.169.254/latest/meta-data/")
            if stdout:
                print_success("\n  AWS Metadata accessible!")
                print(stdout)
            else:
                print_error("\n  Not on AWS or metadata blocked")
        
        input("\n  Press Enter...")

    def aws_enum(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  AWS CLI ENUMERATION{Colors.END}\n")
        
        if not check_tool("aws"):
            print_error("  AWS CLI not installed!")
            print_info("  apt install awscli")
            input("\n  Enter..."); return
        
        print(f"  [1] List S3 buckets")
        print(f"  [2] List EC2 instances")
        print(f"  [3] List IAM users")
        print(f"  [4] Get caller identity")
        choice = get_input("\n  Select", "4")
        
        cmds = {
            "1": "aws s3 ls",
            "2": "aws ec2 describe-instances",
            "3": "aws iam list-users",
            "4": "aws sts get-caller-identity"
        }
        
        if choice in cmds:
            run_command_live(cmds[choice])
        
        input("\n  Press Enter...")

    def cred_checker(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  CLOUD CREDENTIAL CHECKER{Colors.END}\n")
        
        print_info("  Checking for credential files...\n")
        
        paths = [
            ("AWS Credentials", "~/.aws/credentials"),
            ("AWS Config", "~/.aws/config"),
            ("GCP Credentials", "~/.config/gcloud/credentials.db"),
            ("Azure CLI", "~/.azure/"),
        ]
        
        for name, path in paths:
            expanded = os.path.expanduser(path)
            if os.path.exists(expanded):
                print_success(f"  {name}: {path} - EXISTS")
            else:
                print(f"  {Colors.GRAY}{name}: {path} - not found{Colors.END}")
        
        # Check env vars
        print(f"\n  {Colors.BOLD}Environment Variables:{Colors.END}")
        env_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "GOOGLE_APPLICATION_CREDENTIALS", "AZURE_TENANT_ID"]
        for var in env_vars:
            val = os.environ.get(var)
            if val:
                print_success(f"  {var} = {val[:20]}...")
            else:
                print(f"  {Colors.GRAY}{var} - not set{Colors.END}")
        
        input("\n  Press Enter...")
