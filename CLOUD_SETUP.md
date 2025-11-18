# Cloud Setup Guide - Free 24/7 Monitoring

This guide shows you how to run your Hobbiton checker 24/7 for **FREE** using cloud services.

## ⭐ Option 1: GitHub Actions (Easiest - 5 Minutes)

GitHub Actions will run your checker every hour automatically.

### Steps:

1. **Create a GitHub account** (if you don't have one):
   - Go to https://github.com/signup
   - It's free!

2. **Create a new repository**:
   ```bash
   cd ~/hobbiton-checker
   git init
   git add .
   git commit -m "Initial commit - Hobbiton checker"
   ```

3. **Push to GitHub**:
   ```bash
   # Create a new repo on GitHub first (https://github.com/new)
   # Name it: hobbiton-checker
   # Then:
   git remote add origin https://github.com/YOUR_USERNAME/hobbiton-checker.git
   git branch -M main
   git push -u origin main
   ```

4. **Add your email secrets**:
   - Go to your repo on GitHub
   - Click **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Add these three secrets:
     - Name: `SENDER_EMAIL`, Value: your-email@gmail.com
     - Name: `SENDER_PASSWORD`, Value: your-app-password
     - Name: `RECIPIENT_EMAIL`, Value: your-email@gmail.com

5. **Enable Actions**:
   - Go to **Actions** tab in your repo
   - Click "I understand my workflows, go ahead and enable them"

6. **Done!** 🎉
   - The checker will run automatically every hour
   - You'll get email notifications when slots are found
   - View logs in the Actions tab

### Pros:
✅ Completely free
✅ No server management
✅ Easy to set up
✅ View logs in GitHub

### Cons:
❌ No desktop notifications (only email)
❌ Runs on GitHub's schedule (not 100% guaranteed timing)

---

## Option 2: Oracle Cloud Always Free (Best for Full Control)

Oracle Cloud has a truly **free forever** tier with a VM instance.

### Steps:

1. **Sign up for Oracle Cloud**:
   - Go to https://www.oracle.com/cloud/free/
   - Sign up (requires credit card for verification but won't charge)
   - Get free VM: 1/8 OCPU + 1GB RAM (ARM or AMD)

2. **Create a VM instance**:
   - Choose "Create a VM instance"
   - Select "Always Free Eligible" option
   - Choose Ubuntu 22.04
   - Download SSH key

3. **Connect to your VM**:
   ```bash
   ssh -i ~/path-to-key.pem ubuntu@YOUR_VM_IP
   ```

4. **Install Python and dependencies**:
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip git
   git clone https://github.com/YOUR_USERNAME/hobbiton-checker.git
   cd hobbiton-checker
   pip3 install -r requirements.txt
   ```

5. **Set up environment variables**:
   ```bash
   echo 'export SENDER_EMAIL="your@gmail.com"' >> ~/.bashrc
   echo 'export SENDER_PASSWORD="your-app-password"' >> ~/.bashrc
   echo 'export RECIPIENT_EMAIL="your@gmail.com"' >> ~/.bashrc
   source ~/.bashrc
   ```

6. **Run as a service**:
   ```bash
   # Create systemd service
   sudo nano /etc/systemd/system/hobbiton-checker.service
   ```

   Paste this:
   ```ini
   [Unit]
   Description=Hobbiton Availability Checker
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/hobbiton-checker
   Environment="SENDER_EMAIL=your@gmail.com"
   Environment="SENDER_PASSWORD=your-app-password"
   Environment="RECIPIENT_EMAIL=your@gmail.com"
   ExecStart=/usr/bin/python3 /home/ubuntu/hobbiton-checker/check_availability.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Then:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable hobbiton-checker
   sudo systemctl start hobbiton-checker
   sudo systemctl status hobbiton-checker
   ```

7. **Done!** Your checker runs 24/7 on a free cloud server.

### Pros:
✅ Truly free forever
✅ Full control
✅ Runs 24/7
✅ Can run other things too

### Cons:
❌ Requires server management
❌ More complex setup
❌ Need to keep it updated

---

## Option 3: Google Cloud Free Tier

Similar to Oracle Cloud but with Google's infrastructure.

1. **Sign up**: https://cloud.google.com/free
2. **Create e2-micro instance** (free tier)
3. **Follow similar steps as Oracle Cloud**

---

## Comparison:

| Feature | GitHub Actions | Oracle Cloud | Google Cloud |
|---------|---------------|--------------|--------------|
| **Cost** | Free | Free Forever | Free (with limits) |
| **Setup** | 5 minutes | 15 minutes | 15 minutes |
| **Reliability** | High | Very High | Very High |
| **Control** | Low | Full | Full |
| **Best For** | Quick setup | Full control | Google ecosystem |

---

## Recommendation:

**Start with GitHub Actions** (easiest, takes 5 minutes)

If you need more control later, migrate to Oracle Cloud.

Both options will send you email notifications when Hobbiton tour slots become available! 📧✅

