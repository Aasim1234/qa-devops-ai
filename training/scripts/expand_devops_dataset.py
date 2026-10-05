from pathlib import Path
import json

OUTPUT = Path(
    r"S:\qa-devops-ai\data\external\devops_expanded.jsonl"
)

DATA = []


def add(category, difficulty, question, answer):
    DATA.append({
        "category": category,
        "difficulty": difficulty,
        "question": question,
        "answer": answer
    })


# =========================================================
# DEVOPS
# =========================================================

devops = [
    ("What is DevOps?", "DevOps combines development and operations practices with automation, collaboration, continuous delivery, infrastructure as code, monitoring, and feedback."),
    ("Why is DevOps important?", "DevOps helps teams automate delivery, reduce manual work, improve feedback, increase deployment consistency, and operate software more reliably."),
    ("What is continuous integration?", "Continuous integration means frequently integrating code changes and automatically building and testing them."),
    ("What is continuous delivery?", "Continuous delivery keeps software in a releasable state through automated build, test, and delivery processes."),
    ("What is continuous deployment?", "Continuous deployment automatically releases validated changes to production without a separate manual deployment step."),
    ("What is infrastructure as code?", "Infrastructure as code manages infrastructure through version-controlled configuration instead of relying primarily on manual configuration."),
    ("What is configuration management?", "Configuration management keeps systems in a known desired state through repeatable automation and controlled configuration."),
    ("What is immutable infrastructure?", "Immutable infrastructure replaces an existing instance with a new version rather than modifying the instance in place."),
    ("What is a deployment strategy?", "A deployment strategy defines how a new software version is introduced to infrastructure or users."),
    ("What is blue-green deployment?", "Blue-green deployment uses separate old and new environments and switches traffic after the new environment has been validated."),
    ("What is canary deployment?", "Canary deployment exposes a new version to a small portion of traffic before expanding the rollout."),
    ("What is rolling deployment?", "Rolling deployment gradually replaces instances running the old version with instances running the new version."),
    ("What is a rollback?", "A rollback returns a deployment to a previously known working version when the new version causes unacceptable problems."),
    ("What is idempotency?", "An idempotent operation can be repeated while converging on the same intended final state."),
    ("What is automation in DevOps?", "Automation uses software and repeatable workflows to perform tasks such as testing, provisioning, configuration, deployment, and monitoring."),
]

for q, a in devops:
    add("devops", "easy", q, a)


# =========================================================
# LINUX
# =========================================================

linux = [
    ("How do you check disk space?", "Use df -h to inspect filesystem space usage."),
    ("How do you check inode usage?", "Use df -i to inspect inode consumption."),
    ("How do you find large files?", "Use commands such as du and find to identify large files and directories."),
    ("How do you check memory?", "Use free -h, top, or ps to inspect memory usage."),
    ("How do you check CPU usage?", "Use top, htop, ps, or other system monitoring tools to identify CPU-consuming processes."),
    ("How do you find a process using a port?", "Use ss -lntp or lsof -i to identify processes associated with network ports."),
    ("What does chmod do?", "chmod changes file and directory permission bits."),
    ("What does chown do?", "chown changes file or directory ownership."),
    ("What does systemctl do?", "systemctl is used to manage systemd services and related units."),
    ("How do you restart a service?", "Use systemctl restart followed by the service name when you have the required privileges."),
    ("How do you check service status?", "Use systemctl status followed by the service name."),
    ("How do you view Linux logs?", "Use tools such as journalctl and inspect application-specific log files."),
    ("What is a symbolic link?", "A symbolic link is a filesystem entry that points to another file or directory."),
    ("What is an environment variable?", "An environment variable is a named value made available to processes through the operating-system environment."),
    ("How do you find a process?", "Use ps, pgrep, pidof, or top depending on the information required."),
]

for q, a in linux:
    add("linux", "easy", q, a)


# =========================================================
# GIT
# =========================================================

git = [
    ("What is Git?", "Git is a distributed version-control system for tracking changes and collaborating on source code."),
    ("What is a Git branch?", "A branch is a movable reference to a line of development."),
    ("What is git clone?", "git clone creates a local copy of a remote repository."),
    ("What is git pull?", "git pull retrieves remote changes and integrates them into the current branch according to the configured pull behavior."),
    ("What is git fetch?", "git fetch retrieves changes from a remote repository without automatically merging them into the current branch."),
    ("What is git merge?", "git merge integrates the history of another branch into the current branch."),
    ("What is git rebase?", "git rebase reapplies commits onto another base and can rewrite the branch history."),
    ("What is a merge conflict?", "A merge conflict occurs when Git cannot automatically reconcile competing changes."),
    ("How do you resolve a merge conflict?", "Inspect conflicted files, decide the correct content, remove conflict markers, stage the resolved files, and complete the merge or rebase."),
    ("What is git revert?", "git revert creates a new commit that reverses the effect of an earlier commit."),
    ("What is git reset?", "git reset moves the current branch reference and can also modify the staging area or working tree depending on the selected mode."),
]

for q, a in git:
    add("git", "easy", q, a)


# =========================================================
# DOCKER
# =========================================================

docker = [
    ("What is Docker?", "Docker is a platform for packaging and running applications in containers."),
    ("What is a Docker image?", "A Docker image is an immutable package used as the template for creating containers."),
    ("What is a Docker container?", "A container is a running instance created from an image."),
    ("What is a Dockerfile?", "A Dockerfile contains instructions used to build a Docker image."),
    ("What is Docker Compose?", "Docker Compose defines and manages multi-container application environments using a declarative configuration file."),
    ("Why does a container exit?", "A container normally stops when its main process exits. The process may exit because of an application error, command configuration, dependency failure, or other runtime problem."),
    ("How do you troubleshoot a stopped container?", "Check docker ps -a, inspect container logs, inspect configuration, verify the command or entrypoint, and check dependencies."),
    ("How do you view Docker logs?", "Use docker logs followed by the container name or ID."),
    ("How do you inspect a container?", "Use docker inspect to view configuration and runtime metadata."),
    ("What is a Docker volume?", "A Docker volume provides persistent storage that is managed separately from a container's writable layer."),
    ("What is a Docker network?", "A Docker network provides connectivity between containers and other network endpoints according to its configuration."),
]

for q, a in docker:
    add("docker", "easy", q, a)


# =========================================================
# KUBERNETES
# =========================================================

kubernetes = [
    ("What is Kubernetes?", "Kubernetes is a container orchestration system that automates deployment, scaling, scheduling, and management of containerized workloads."),
    ("What is a Pod?", "A Pod is the smallest deployable unit in Kubernetes and can contain one or more containers."),
    ("What is a Deployment?", "A Deployment manages replicated Pods and provides declarative updates and rollout management."),
    ("What is a Service?", "A Service provides a stable network endpoint for reaching a set of Pods."),
    ("What is ConfigMap?", "A ConfigMap stores non-sensitive configuration data that can be consumed by workloads."),
    ("What is Secret?", "A Secret is a Kubernetes resource intended for sensitive configuration data, although additional protection and appropriate cluster security are still required."),
    ("What is CrashLoopBackOff?", "CrashLoopBackOff means a container is repeatedly failing and Kubernetes is increasing the delay between restart attempts."),
    ("What is ImagePullBackOff?", "ImagePullBackOff indicates Kubernetes is having trouble pulling a required container image and is backing off before retrying."),
    ("How do you troubleshoot a Pod?", "Check Pod status, events, logs, configuration, probes, resource constraints, scheduling, and dependencies."),
    ("How do you check Pod logs?", "Use kubectl logs with the Pod name and appropriate container options."),
    ("How do you inspect a Pod?", "Use kubectl describe pod to inspect details and events."),
    ("What is a Namespace?", "A Namespace provides a logical boundary for organizing Kubernetes resources within a cluster."),
    ("What is a ReplicaSet?", "A ReplicaSet maintains a specified number of Pod replicas."),
]

for q, a in kubernetes:
    add("kubernetes", "medium", q, a)


# =========================================================
# TERRAFORM
# =========================================================

terraform = [
    ("What is Terraform?", "Terraform is an infrastructure-as-code tool for defining and managing infrastructure using configuration."),
    ("What is Terraform state?", "Terraform state records the mapping between Terraform configuration and managed infrastructure."),
    ("What is terraform init?", "terraform init initializes a Terraform working directory and installs required providers and modules."),
    ("What is terraform plan?", "terraform plan previews the changes Terraform proposes based on configuration, state, and current infrastructure."),
    ("What is terraform apply?", "terraform apply executes the planned infrastructure changes."),
    ("What is terraform destroy?", "terraform destroy plans and applies removal of resources managed by the configuration."),
    ("What is a Terraform provider?", "A provider is a plugin through which Terraform interacts with a specific infrastructure or service API."),
    ("What is a Terraform module?", "A module is a reusable collection of Terraform configuration."),
    ("What is count?", "count creates multiple resource instances using numeric indexes."),
    ("What is for_each?", "for_each creates multiple resource instances based on keys or values from a collection."),
    ("Why use remote state?", "Remote state allows state to be stored centrally and can support collaboration and controlled state access."),
]

for q, a in terraform:
    add("terraform", "medium", q, a)


# =========================================================
# ANSIBLE
# =========================================================

ansible = [
    ("What is Ansible?", "Ansible is an automation and configuration-management platform."),
    ("What is an Ansible playbook?", "A playbook is a YAML document containing automation instructions organized into plays and tasks."),
    ("What is an inventory?", "An Ansible inventory defines the managed hosts and can organize them into groups."),
    ("What is an Ansible role?", "A role provides a reusable structure for organizing tasks, variables, handlers, templates, and related automation files."),
    ("What is an Ansible handler?", "A handler is a task triggered by a notification, commonly used for actions such as restarting a service after configuration changes."),
    ("What is Ansible idempotency?", "Idempotent automation repeatedly converges the managed system toward the same desired state."),
]

for q, a in ansible:
    add("ansible", "medium", q, a)


# =========================================================
# JENKINS / CI-CD
# =========================================================

jenkins = [
    ("What is Jenkins?", "Jenkins is an automation server commonly used for CI/CD pipelines."),
    ("What is a Jenkins pipeline?", "A Jenkins pipeline defines automated stages and steps for software delivery."),
    ("What is a Jenkinsfile?", "A Jenkinsfile stores pipeline-as-code instructions, usually alongside application source code."),
    ("What is a Jenkins agent?", "A Jenkins agent is a machine or execution environment used to run pipeline work."),
    ("How do you troubleshoot a Jenkins build failure?", "Inspect the failed stage and console output, identify the first meaningful error, reproduce the failure where appropriate, inspect dependencies and environment differences, then validate the fix."),
    ("What is a pipeline stage?", "A stage groups related pipeline steps into a meaningful section such as build, test, package, or deploy."),
]

for q, a in jenkins:
    add("jenkins", "medium", q, a)


# =========================================================
# AWS
# =========================================================

aws = [
    ("What is EC2?", "Amazon EC2 provides virtual compute capacity in AWS."),
    ("What is S3?", "Amazon S3 is an object storage service."),
    ("What is VPC?", "Amazon VPC provides an isolated virtual network environment in AWS."),
    ("What is a subnet?", "A subnet is a range of IP addresses within a VPC where resources can be placed."),
    ("What is a security group?", "A security group controls allowed network traffic for associated AWS resources."),
    ("What is an Internet Gateway?", "An Internet Gateway enables communication between a VPC and the public internet for appropriately routed resources."),
    ("What is a NAT Gateway?", "A NAT Gateway allows resources in a private subnet to initiate outbound connections to external networks without accepting unsolicited inbound connections from the internet."),
    ("What is IAM?", "AWS Identity and Access Management controls authentication and authorization for AWS resources."),
    ("What is CloudWatch?", "Amazon CloudWatch provides monitoring and observability capabilities including metrics, logs, alarms, and related operational data."),
    ("What is Route 53?", "Amazon Route 53 is a DNS and domain-management service with routing capabilities."),
]

for q, a in aws:
    add("aws", "medium", q, a)


# =========================================================
# MONITORING / OBSERVABILITY
# =========================================================

observability = [
    ("What is monitoring?", "Monitoring collects and presents measurements or events so teams can detect and respond to operational conditions."),
    ("What is observability?", "Observability is the ability to understand system behavior from externally available signals such as metrics, logs, and traces."),
    ("What are metrics?", "Metrics are numerical measurements collected over time."),
    ("What are logs?", "Logs are timestamped records of events or messages produced by systems and applications."),
    ("What are traces?", "Traces represent the path of a request through distributed components."),
    ("What are the golden signals?", "The four golden signals are latency, traffic, errors, and saturation."),
    ("What is Prometheus?", "Prometheus is a monitoring and alerting system designed around time-series metrics and a dimensional data model."),
    ("What is Grafana?", "Grafana is a visualization and observability platform commonly used to create dashboards from monitoring data."),
    ("What is an alert?", "An alert is a notification generated when a defined operational condition or threshold requires attention."),
]

for q, a in observability:
    add("observability", "medium", q, a)


# =========================================================
# SRE
# =========================================================

sre = [
    ("What is SRE?", "Site Reliability Engineering applies software engineering practices to operations and reliability."),
    ("What is SLI?", "A Service Level Indicator is a measurement representing a service characteristic such as availability, latency, or correctness."),
    ("What is SLO?", "A Service Level Objective is a target level for an SLI over a defined period."),
    ("What is SLA?", "A Service Level Agreement is an agreement defining service expectations and often associated commitments between parties."),
    ("What is an error budget?", "An error budget represents the allowed amount of unreliability implied by an SLO over a defined period."),
    ("What is toil?", "Toil is repetitive, manual, automatable operational work that does not provide lasting service improvement."),
]

for q, a in sre:
    add("sre", "medium", q, a)


# =========================================================
# TROUBLESHOOTING
# =========================================================

troubleshooting = [
    (
        "A production API returns HTTP 503. What do you do?",
        "First clarify the scope and confirm whether the issue affects all users or a subset. Check backend health, load balancer or proxy status, service discovery, connectivity, application logs, resource usage, and recent changes. Apply the safest mitigation, validate recovery, and document prevention actions."
    ),
    (
        "A production API returns HTTP 502. What do you investigate?",
        "Investigate the communication between the proxy or gateway and its upstream backend. Check backend availability, connectivity, ports, application logs, proxy configuration, timeouts, and recent changes."
    ),
    (
        "A server has 100 percent disk usage. What do you do?",
        "Confirm filesystem and inode usage, identify large files and directories, inspect logs and temporary data, check for deleted files still held open by processes, free space safely, and validate application recovery."
    ),
    (
        "CPU suddenly reaches 100 percent in production. What is your approach?",
        "Confirm scope and duration, identify the consuming process, correlate system and application metrics with logs and recent changes, mitigate safely, validate recovery, and investigate the underlying cause."
    ),
    (
        "Memory usage continuously increases. What do you investigate?",
        "Identify the process consuming memory, inspect memory trends and application behavior, correlate with logs and workload changes, check for OOM events or abnormal growth, mitigate safely, and continue monitoring."
    ),
    (
        "A deployment succeeded but the application is unhealthy. What do you check?",
        "Check application health, logs, dependencies, configuration, networking, probes, resource usage, and recent changes. Determine whether rollback or another mitigation is appropriate, then validate the service after the change."
    ),
    (
        "A Kubernetes Pod keeps restarting. What do you check?",
        "Check Pod status, events, container logs, command and arguments, configuration, probes, resource limits, dependencies, and recent changes."
    ),
]

for q, a in troubleshooting:
    add("troubleshooting", "hard", q, a)


# =========================================================
# QA / AUTOMATION
# =========================================================

qa = [
    ("What is STLC?", "Software Testing Life Cycle is a structured testing process that commonly includes requirements analysis, test planning, test design, environment setup, execution, defect reporting, and closure activities."),
    ("What is regression testing?", "Regression testing verifies that existing functionality continues to work after changes."),
    ("What is smoke testing?", "Smoke testing performs a small set of critical checks to determine whether a build is suitable for further testing."),
    ("What is sanity testing?", "Sanity testing is a focused check of specific changed functionality to determine whether it behaves as expected before broader testing."),
    ("What is an API test?", "An API test validates API behavior such as status codes, response data, headers, authentication, error handling, and response time."),
    ("What is Selenium?", "Selenium is a browser automation framework commonly used for web application testing."),
    ("What is Playwright?", "Playwright is a browser automation framework supporting modern web application testing and automation."),
    ("Why use API automation?", "API automation provides fast, repeatable validation of backend behavior and can test services independently of the user interface."),
]

for q, a in qa:
    add("qa_testing", "medium", q, a)


# =========================================================
# BUILD DATASET
# =========================================================

def main():

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT.open(
        "w",
        encoding="utf-8"
    ) as f:

        for i, item in enumerate(DATA, 1):

            record = {
                "id": f"external-{i:05d}",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a professional "
                            "DevOps, SRE and QA interview assistant. "
                            "Answer accurately and concisely."
                        )
                    },
                    {
                        "role": "user",
                        "content": item["question"]
                    },
                    {
                        "role": "assistant",
                        "content": item["answer"]
                    }
                ],
                "category": item["category"],
                "difficulty": item["difficulty"],
                "source": "general_devops_knowledge"
            }

            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                ) + "\n"
            )

    print(
        f"Created {len(DATA)} external records."
    )

    print(
        f"Output: {OUTPUT}"
    )


if __name__ == "__main__":
    main()