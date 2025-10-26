# Step 1: Use Ubuntu as base
FROM ubuntu:22.04

# Step 2: Install dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    openjdk-17-jdk \
    curl \
    gnupg2 \
    lsb-release \
    sudo \
    tini \
    unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Step 3: Add Jenkins repository and key
RUN curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | tee /etc/apt/sources.list.d/jenkins.list > /dev/null

# Step 4: Install Jenkins
RUN apt-get update && apt-get install -y jenkins && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Step 5: Expose Jenkins port
EXPOSE 8080

# Step 6: Set Jenkins home
ENV JENKINS_HOME=/var/lib/jenkins

# Step 7: Use tini as init and start Jenkins in foreground
ENTRYPOINT ["/usr/bin/tini", "--", "/usr/bin/java", "-jar", "/usr/share/java/jenkins.war"]
