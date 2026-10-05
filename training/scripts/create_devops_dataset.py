from pathlib import Path
import json


OUTPUT = Path(
    r"S:\qa-devops-ai\data\external\devops_master.jsonl"
)


DATA = [

    # =========================
    # DEVOPS FUNDAMENTALS
    # =========================

    {
        "question": "What is DevOps?",
        "answer": "DevOps is a set of practices that brings development and operations closer together through automation, collaboration, continuous integration, continuous delivery, infrastructure as code, monitoring, and feedback.",
        "category": "devops",
        "difficulty": "easy"
    },

    {
        "question": "What are the benefits of DevOps?",
        "answer": "DevOps can improve delivery speed, deployment consistency, collaboration, automation, feedback, reliability, and the ability to recover from failures.",
        "category": "devops",
        "difficulty": "easy"
    },

    {
        "question": "What is CI?",
        "answer": "Continuous Integration is the practice of frequently integrating code changes into a shared repository and automatically building and testing those changes.",
        "category": "cicd",
        "difficulty": "easy"
    },

    {
        "question": "What is CD?",
        "answer": "Continuous Delivery or Continuous Deployment automates the process of moving validated software changes toward release or deployment.",
        "category": "cicd",
        "difficulty": "easy"
    },

    {
        "question": "What is Infrastructure as Code?",
        "answer": "Infrastructure as Code is the practice of defining and managing infrastructure through version-controlled configuration rather than relying primarily on manual changes.",
        "category": "devops",
        "difficulty": "easy"
    },

    {
        "question": "What is idempotency?",
        "answer": "An operation is idempotent when applying it repeatedly produces the same intended end state rather than continuously changing the resource.",
        "category": "devops",
        "difficulty": "medium"
    },

    {
        "question": "What is immutable infrastructure?",
        "answer": "Immutable infrastructure means replacing infrastructure with a new version instead of modifying the existing instance in place.",
        "category": "devops",
        "difficulty": "medium"
    },

    {
        "question": "What is blue-green deployment?",
        "answer": "Blue-green deployment maintains two environments. Traffic can be switched from the existing environment to the new environment after validation, allowing a controlled release and easier rollback.",
        "category": "deployment",
        "difficulty": "medium"
    },

    {
        "question": "What is a rolling deployment?",
        "answer": "A rolling deployment gradually replaces instances of an existing version with the new version while keeping part of the service available.",
        "category": "deployment",
        "difficulty": "easy"
    },

    {
        "question": "What is canary deployment?",
        "answer": "Canary deployment releases a new version to a small portion of users or infrastructure first, allowing the team to observe behavior before expanding the rollout.",
        "category": "deployment",
        "difficulty": "medium"
    },

    # =========================
    # LINUX
    # =========================

    {
        "question": "How do you check disk usage in Linux?",
        "answer": "Use df -h to view filesystem space usage. Use du -sh to inspect the size of directories or files.",
        "category": "linux",
        "difficulty": "easy"
    },

    {
        "question": "How do you check inode usage?",
        "answer": "Use df -i to check inode consumption on Linux filesystems.",
        "category": "linux",
        "difficulty": "easy"
    },

    {
        "question": "How do you find a process using a port?",
        "answer": "Commands such as ss -lntp or lsof -i can be used to identify processes associated with listening network ports.",
        "category": "linux",
        "difficulty": "easy"
    },

    {
        "question": "How do you check memory usage in Linux?",
        "answer": "Use commands such as free -h, top, or ps to inspect memory consumption. For deeper investigation, correlate process usage with system metrics and logs.",
        "category": "linux",
        "difficulty": "easy"
    },

    {
        "question": "What is systemd?",
        "answer": "systemd is a Linux system and service manager responsible for starting and managing services and other system resources.",
        "category": "linux",
        "difficulty": "easy"
    },

    # =========================
    # GIT
    # =========================

    {
        "question": "What is Git?",
        "answer": "Git is a distributed version control system used to track changes to source code and collaborate across development workflows.",
        "category": "git",
        "difficulty": "easy"
    },

    {
        "question": "What is Git merge?",
        "answer": "Git merge combines changes from one branch into another and may create a merge commit when the histories cannot be fast-forwarded.",
        "category": "git",
        "difficulty": "easy"
    },

    {
        "question": "What is Git rebase?",
        "answer": "Git rebase reapplies commits from one branch on top of another base commit, producing a different commit history.",
        "category": "git",
        "difficulty": "medium"
    },

    {
        "question": "What is the difference between merge and rebase?",
        "answer": "Merge combines histories and can preserve their branching structure, while rebase rewrites the branch history by replaying commits onto another base.",
        "category": "git",
        "difficulty": "medium"
    },

    # =========================
    # DOCKER
    # =========================

    {
        "question": "What is Docker?",
        "answer": "Docker is a platform for packaging and running applications in containers.",
        "category": "docker",
        "difficulty": "easy"
    },

    {
        "question": "What is a Docker image?",
        "answer": "A Docker image is a packaged, immutable template containing the filesystem and metadata needed to create a container.",
        "category": "docker",
        "difficulty": "easy"
    },

    {
        "question": "What is a Docker container?",
        "answer": "A Docker container is a running instance created from a container image.",
        "category": "docker",
        "difficulty": "easy"
    },

    {
        "question": "Why does a Docker container exit immediately?",
        "answer": "A container normally remains running while its main process is running. If that process exits because of a command, configuration, dependency, or application failure, the container can stop.",
        "category": "docker",
        "difficulty": "medium"
    },

    {
        "question": "How do you troubleshoot a Docker container?",
        "answer": "Check the container status, inspect logs, inspect the container configuration, verify the command or entrypoint, check networking and dependencies, and reproduce the issue interactively when appropriate.",
        "category": "docker",
        "difficulty": "medium"
    },

    # =========================
    # KUBERNETES
    # =========================

    {
        "question": "What is Kubernetes?",
        "answer": "Kubernetes is a container orchestration platform used to automate deployment, scaling, scheduling, and management of containerized workloads.",
        "category": "kubernetes",
        "difficulty": "easy"
    },

    {
        "question": "What is a Kubernetes Pod?",
        "answer": "A Pod is the smallest deployable unit in Kubernetes and can contain one or more containers that share networking and storage resources.",
        "category": "kubernetes",
        "difficulty": "easy"
    },

    {
        "question": "What is a Kubernetes Deployment?",
        "answer": "A Deployment manages a set of replicated Pods and provides declarative updates and controlled rollout behavior.",
        "category": "kubernetes",
        "difficulty": "medium"
    },

    {
        "question": "What is CrashLoopBackOff?",
        "answer": "CrashLoopBackOff indicates that a container repeatedly starts and exits, and Kubernetes is backing off before restarting it again.",
        "category": "kubernetes",
        "difficulty": "medium"
    },

    {
        "question": "How do you troubleshoot a Kubernetes Pod?",
        "answer": "Check Pod status and events, inspect logs, describe the Pod, verify configuration and probes, check resource limits, inspect dependencies, and confirm scheduling and networking.",
        "category": "kubernetes",
        "difficulty": "medium"
    },

    # =========================
    # TERRAFORM
    # =========================

    {
        "question": "What is Terraform?",
        "answer": "Terraform is an infrastructure as code tool that uses configuration files to define and manage infrastructure resources.",
        "category": "terraform",
        "difficulty": "easy"
    },

    {
        "question": "What is Terraform state?",
        "answer": "Terraform state records information Terraform uses to map configuration to managed infrastructure and determine changes during planning.",
        "category": "terraform",
        "difficulty": "medium"
    },

    {
        "question": "What is terraform plan?",
        "answer": "terraform plan previews the changes Terraform intends to make based on the configuration, state, and current infrastructure.",
        "category": "terraform",
        "difficulty": "easy"
    },

    {
        "question": "What is terraform apply?",
        "answer": "terraform apply executes the proposed Terraform changes after the plan has been reviewed or otherwise approved according to the workflow.",
        "category": "terraform",
        "difficulty": "easy"
    },

    {
        "question": "What is the difference between count and for_each in Terraform?",
        "answer": "Both can create multiple resources. count uses numeric indexes, while for_each works with a collection of keys or values and can provide more stable resource addressing for keyed resources.",
        "category": "terraform",
        "difficulty": "medium"
    },

    # =========================
    # ANSIBLE
    # =========================

    {
        "question": "What is Ansible?",
        "answer": "Ansible is an automation and configuration-management tool used to execute repeatable tasks across systems.",
        "category": "ansible",
        "difficulty": "easy"
    },

    {
        "question": "What is an Ansible playbook?",
        "answer": "An Ansible playbook is a YAML document that defines plays, hosts, tasks, variables, and other automation instructions.",
        "category": "ansible",
        "difficulty": "easy"
    },

    {
        "question": "What is Ansible idempotency?",
        "answer": "An idempotent Ansible task can be executed repeatedly while converging the managed system toward the same desired state.",
        "category": "ansible",
        "difficulty": "medium"
    },

    # =========================
    # JENKINS
    # =========================

    {
        "question": "What is Jenkins?",
        "answer": "Jenkins is an automation server commonly used to implement build, test, delivery, and deployment pipelines.",
        "category": "jenkins",
        "difficulty": "easy"
    },

    {
        "question": "What is a Jenkins pipeline?",
        "answer": "A Jenkins pipeline defines automated stages and steps used to build, test, package, and deploy software.",
        "category": "jenkins",
        "difficulty": "easy"
    },

    {
        "question": "What is Jenkinsfile?",
        "answer": "A Jenkinsfile is a file stored with the source code that defines the Jenkins pipeline as code.",
        "category": "jenkins",
        "difficulty": "easy"
    },

    # =========================
    # AWS
    # =========================

    {
        "question": "What is Amazon EC2?",
        "answer": "Amazon EC2 provides resizable compute capacity in the AWS cloud through virtual server instances.",
        "category": "aws",
        "difficulty": "easy"
    },

    {
        "question": "What is an AWS VPC?",
        "answer": "Amazon VPC provides a logically isolated virtual network in AWS where resources can be placed into subnets and controlled through networking components.",
        "category": "aws",
        "difficulty": "easy"
    },

    {
        "question": "What is a security group in AWS?",
        "answer": "An AWS security group acts as a virtual firewall controlling allowed inbound and outbound traffic for associated resources.",
        "category": "aws",
        "difficulty": "easy"
    },

    {
        "question": "What is an S3 bucket?",
        "answer": "An Amazon S3 bucket is a container for storing objects in Amazon S3.",
        "category": "aws",
        "difficulty": "easy"
    },

    # =========================
    # OBSERVABILITY
    # =========================

    {
        "question": "What is observability?",
        "answer": "Observability is the ability to understand the internal state and behavior of a system from its external outputs, commonly using metrics, logs, and traces.",
        "category": "observability",
        "difficulty": "easy"
    },

    {
        "question": "What are the three pillars of observability?",
        "answer": "The commonly referenced three pillars are metrics, logs, and traces.",
        "category": "observability",
        "difficulty": "easy"
    },

    {
        "question": "What are the four golden signals?",
        "answer": "The four golden signals are latency, traffic, errors, and saturation.",
        "category": "observability",
        "difficulty": "easy"
    },

    # =========================
    # TROUBLESHOOTING
    # =========================

    {
        "question": "How would you troubleshoot HTTP 503?",
        "answer": "First determine the scope and confirm whether the backend service is healthy. Then inspect load balancer or proxy status, backend health, service discovery, networking, application logs, resource usage, and recent changes. After mitigation, validate recovery and document prevention actions.",
        "category": "troubleshooting",
        "difficulty": "hard"
    },

    {
        "question": "How would you troubleshoot HTTP 502?",
        "answer": "Investigate the relationship between the proxy or gateway and its upstream backend. Check backend availability, connectivity, ports, application logs, proxy configuration, timeouts, and recent changes.",
        "category": "troubleshooting",
        "difficulty": "hard"
    },

    {
        "question": "How would you troubleshoot a production disk-full incident?",
        "answer": "Confirm filesystem usage with df -h and inode usage with df -i. Identify large files or directories with du, check logs and temporary files, investigate deleted files still held open by processes, free space safely, and then verify application recovery.",
        "category": "troubleshooting",
        "difficulty": "hard"
    },

    {
        "question": "How would you troubleshoot high CPU usage?",
        "answer": "Confirm the scope and duration of the CPU spike, identify the consuming process, inspect application and system metrics and logs, correlate with recent deployments or workload changes, mitigate safely, and validate recovery.",
        "category": "troubleshooting",
        "difficulty": "hard"
    },

    {
        "question": "How would you troubleshoot high memory usage?",
        "answer": "Confirm available and used memory, identify processes consuming memory, inspect application behavior and logs, determine whether the growth is expected or abnormal, check for OOM events, mitigate safely, and continue monitoring after the change.",
        "category": "troubleshooting",
        "difficulty": "hard"
    },

    # =========================
    # SRE
    # =========================

    {
        "question": "What is SRE?",
        "answer": "Site Reliability Engineering applies software engineering practices to operations and reliability, using automation, monitoring, service-level objectives, and systematic incident management.",
        "category": "sre",
        "difficulty": "medium"
    },

    {
        "question": "What is an SLO?",
        "answer": "A Service Level Objective is a target for a service-level indicator, such as availability or latency, over a defined period.",
        "category": "sre",
        "difficulty": "medium"
    },

    {
        "question": "What is an error budget?",
        "answer": "An error budget represents the amount of unreliability allowed by an SLO over a defined period and can help balance reliability work against release velocity.",
        "category": "sre",
        "difficulty": "medium"
    },

]


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
                "id": f"external-{i:04d}",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a professional "
                            "DevOps interview assistant."
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
                "source": "general_devops_seed"
            }

            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                ) + "\n"
            )

    print(
        f"Created {len(DATA)} DevOps training records."
    )

    print(
        f"Output: {OUTPUT}"
    )


if __name__ == "__main__":
    main()