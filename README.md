# 🎵 Cloud-Native Video to MP3 Conversion Platform

[![Kubernetes](https://img.shields.io/badge/kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![RabbitMQ](https://img.shields.io/badge/rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)](https://www.rabbitmq.com/)
[![MongoDB](https://img.shields.io/badge/mongodb-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)

> A production-grade, event-driven microservices system that converts video files to MP3 audio format using asynchronous processing, distributed storage, and Kubernetes orchestration.

**Built to demonstrate:** Microservices Architecture • Event-Driven Systems • Kubernetes • Distributed Computing • Cloud-Native Development

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [System Components](#-system-components)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Scaling & Performance](#-scaling--performance)
- [Security Considerations](#-security-considerations)
- [Future Roadmap](#-future-roadmap)
- [Contributing](#-contributing)

---

## 🎯 Overview

This project implements a **scalable, fault-tolerant media conversion system** designed to handle high-volume video processing workloads. Users upload video files through a secure API gateway, which triggers an asynchronous conversion pipeline. Once processing completes, users receive email notifications with download links.

### Why This Project Matters

- **Real-World Application**: Solves actual business problems faced by content platforms, social media apps, and media processing services
- **Production-Ready Patterns**: Implements industry-standard practices for building reliable distributed systems
- **Cloud-Native Design**: Leverages Kubernetes for orchestration, scaling, and high availability
- **Learning Showcase**: Demonstrates deep understanding of backend engineering, system design, and DevOps practices

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT APPLICATION                       │
└────────────────────┬────────────────────────────────────────────┘
                     │ HTTP + JWT Auth
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    🌐 GATEWAY SERVICE (API)                      │
│  • Validates JWT tokens via Auth Service                        │
│  • Stores uploaded videos in MongoDB GridFS                     │
│  • Publishes job messages to RabbitMQ                           │
└────────────────────┬────────────────────────────────────────────┘
                     │ Publish Message
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                   📨 RABBITMQ (Message Broker)                   │
│  • Queue: video (incoming jobs)                                  │
│  • Queue: mp3 (completed conversions)                            │
│  • Ensures message durability & delivery guarantees              │
└────────────┬───────────────────────────────────┬─────────────────┘
             │                                   │
             ▼                                   ▼
┌──────────────────────────────┐  ┌─────────────────────────────┐
│  🎬 CONVERTER SERVICE         │  │  📧 NOTIFICATION SERVICE    │
│  • Consumes video jobs        │  │  • Consumes mp3 events      │
│  • Downloads from GridFS      │  │  • Sends email to users     │
│  • Converts video → MP3       │  │  • Includes download link   │
│  • Stores MP3 in GridFS       │  │                             │
│  • Publishes completion event │  │                             │
└──────────────────────────────┘  └─────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│            🗄️ MONGODB + GRIDFS (Distributed Storage)            │
│  • Database: videos (video file chunks)                          │
│  • Database: mp3s (audio file chunks)                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                  🔐 AUTH SERVICE (MySQL)                         │
│  • User authentication & credential validation                   │
│  • JWT token generation & validation                             │
│  • Admin role management                                         │
└─────────────────────────────────────────────────────────────────┘
```

### Architecture Highlights

- **Loose Coupling**: Services communicate via message queues, not direct HTTP calls
- **Fault Isolation**: Failures in one service don't cascade to others
- **Horizontal Scalability**: Each service can scale independently based on load
- **Asynchronous Processing**: Long-running conversions don't block the API
- **Message Durability**: RabbitMQ persistence ensures no job loss during failures

---

## ✨ Key Features

| Feature | Description | Business Value |
|---------|-------------|----------------|
| **JWT Authentication** | Secure token-based auth with role management | Protects sensitive operations, enables multi-tenancy |
| **Async Processing** | Non-blocking video conversion via message queues | Handles traffic spikes, improves user experience |
| **Distributed Storage** | MongoDB GridFS for large file management | Scalable storage, handles files >16MB |
| **Event-Driven Design** | RabbitMQ pub/sub for service communication | Decouples services, enables easy feature additions |
| **Auto-Scaling** | Kubernetes HPA for dynamic resource allocation | Cost optimization, handles variable workloads |
| **Email Notifications** | SMTP integration for user alerts | Keeps users informed, reduces support tickets |
| **Persistent Queues** | Durable message storage in RabbitMQ | Guarantees job completion even after crashes |
| **Health Monitoring** | Kubernetes liveness/readiness probes | Automatic recovery, high availability |

---

## 🛠️ Technology Stack

### Backend & Services
- **Python 3.10** - Core application logic
- **Flask** - REST API framework
- **Pika** - RabbitMQ client library
- **MoviePy** - Video/audio processing
- **PyMongo** - MongoDB driver
- **PyJWT** - Token authentication

### Infrastructure & DevOps
- **Kubernetes** - Container orchestration
- **Docker** - Containerization
- **Minikube** - Local Kubernetes cluster
- **NGINX Ingress** - Load balancing & routing

### Data & Messaging
- **RabbitMQ** - Message broker (AMQP)
- **MongoDB + GridFS** - Distributed file storage
- **MySQL** - User credential storage

### CI/CD & Tools
- **Docker Hub** - Container registry
- **kubectl** - Kubernetes CLI
- **SMTP (Gmail)** - Email delivery

---

## 🧩 System Components

### 1️⃣ **Auth Service**
- **Responsibility**: User authentication and authorization
- **Tech**: Flask + MySQL + JWT
- **Endpoints**:
  - `POST /login` - Issues JWT tokens
  - `POST /validate` - Validates existing tokens
- **Scalability**: 2 replicas with rolling updates

### 2️⃣ **Gateway Service**
- **Responsibility**: API entry point and request routing
- **Tech**: Flask + MongoDB GridFS + RabbitMQ
- **Endpoints**:
  - `POST /login` - Proxies to Auth Service
  - `POST /upload` - Accepts video files (requires JWT)
  - `GET /download?fid=<id>` - Retrieves MP3 files
- **Features**: File validation, GridFS storage, message publishing
- **Scalability**: 2 replicas behind NGINX Ingress

### 3️⃣ **Converter Service**
- **Responsibility**: Video-to-audio transformation
- **Tech**: Python + FFmpeg + MoviePy
- **Process**:
  1. Consumes video job from queue
  2. Downloads video from GridFS
  3. Extracts audio using MoviePy
  4. Stores MP3 in GridFS
  5. Publishes completion event
- **Scalability**: 4 replicas (CPU-intensive workload)

### 4️⃣ **Notification Service**
- **Responsibility**: User communication
- **Tech**: Python + SMTP
- **Process**:
  1. Consumes MP3 completion events
  2. Sends email with file ID
  3. Acknowledges message processing
- **Configuration**: Gmail SMTP (supports app passwords)

### 5️⃣ **RabbitMQ**
- **Queues**:
  - `video` - Pending conversion jobs
  - `mp3` - Completed conversions awaiting notification
- **Features**: Message persistence, manual acknowledgments, dead-letter exchanges
- **Deployment**: StatefulSet with persistent volume

### 6️⃣ **MongoDB**
- **Databases**:
  - `videos` - Original uploaded files
  - `mp3s` - Converted audio files
- **Storage**: GridFS for files >16MB
- **Deployment**: Single replica (can be clustered for HA)

---

## 📦 Prerequisites

Ensure you have the following installed on your system:

| Tool | Version | Purpose |
|------|---------|---------|
| **Docker** | 20.10+ | Container runtime |
| **Kubernetes** | 1.24+ | Orchestration |
| **Minikube** | 1.28+ | Local K8s cluster |
| **kubectl** | 1.24+ | K8s CLI |
| **MySQL** | 8.0+ | Auth database |
| **Docker Hub Account** | - | Container registry |
| **Gmail Account** | - | Email notifications |

### System Requirements
- **CPU**: 4+ cores recommended
- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: 20GB free space
- **OS**: Linux, macOS, or Windows (with WSL2)

---

## 🚀 Quick Start

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/video-to-mp3-converter.git
cd video-to-mp3-converter
```

### Step 2: Start Minikube
```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192

# Enable Ingress addon
minikube addons enable ingress

# Verify cluster is running
kubectl cluster-info
```

### Step 3: Set Up MySQL (Local)
```bash
# Install MySQL (if not already installed)
# macOS
brew install mysql
brew services start mysql

# Ubuntu/Debian
sudo apt-get install mysql-server
sudo systemctl start mysql

# Initialize the auth database
mysql -u root -p < auth/init.sql
```

### Step 4: Create Kubernetes Secrets
```bash
# Auth Service Secret
kubectl create secret generic auth-secret \
  --from-literal=MYSQL_PASSWORD=auth123 \
  --from-literal=SECRET_KEY=your-super-secret-key-change-in-production

# Gateway Secret (same JWT secret)
kubectl create secret generic gateway-secret \
  --from-literal=SECRET_KEY=your-super-secret-key-change-in-production

# Converter Secret (if needed)
kubectl create secret generic converter-secret \
  --from-literal=PLACEHOLDER=none

# Notification Secret (Gmail credentials)
kubectl create secret generic notification-secret \
  --from-literal=GMAIL_ADDRESS=your-email@gmail.com \
  --from-literal=GMAIL_PASSWORD=your-app-password

# RabbitMQ Secret
kubectl create secret generic rabbitmq-secret \
  --from-literal=RABBITMQ_DEFAULT_USER=guest \
  --from-literal=RABBITMQ_DEFAULT_PASS=guest
```

**Important**: For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password.

### Step 5: Deploy Infrastructure
```bash
# Deploy RabbitMQ
kubectl apply -f rabbit/manifests/

# Deploy MongoDB
kubectl apply -f gateway/manifests/mongo-deploy.yaml
kubectl apply -f gateway/manifests/mongo-service.yaml

# Wait for pods to be ready
kubectl get pods -w
```

### Step 6: Build and Push Docker Images
```bash
# Set your Docker Hub username
export DOCKER_USER=yourdockerhubusername

# Build Auth Service
cd auth
docker build -t $DOCKER_USER/auth:latest .
docker push $DOCKER_USER/auth:latest

# Build Gateway Service
cd ../gateway
docker build -t $DOCKER_USER/gateway:latest .
docker push $DOCKER_USER/gateway:latest

# Build Converter Service
cd ../converter
docker build -t $DOCKER_USER/converter:latest .
docker push $DOCKER_USER/converter:latest

# Build Notification Service
cd ../notification
docker build -t $DOCKER_USER/notification:latest .
docker push $DOCKER_USER/notification:latest
```

**Note**: Update image names in deployment YAML files to match your Docker Hub username.

### Step 7: Deploy Microservices
```bash
# Deploy Auth Service
kubectl apply -f auth/manifests/

# Deploy Gateway Service
kubectl apply -f gateway/manifests/

# Deploy Converter Service
kubectl apply -f converter/manifest/

# Deploy Notification Service
kubectl apply -f notification/manifest/

# Verify all pods are running
kubectl get pods
```

### Step 8: Configure Ingress
```bash
# Get Minikube IP
minikube ip

# Add to /etc/hosts (Linux/macOS) or C:\Windows\System32\drivers\etc\hosts (Windows)
<MINIKUBE_IP> mp3converter.com
<MINIKUBE_IP> rabbitmq.manager.com
```

Example:
```
192.168.49.2 mp3converter.com
192.168.49.2 rabbitmq.manager.com
```

### Step 9: Verify Deployment
```bash
# Check all services
kubectl get svc

# Check ingress
kubectl get ingress

# View logs of a specific service
kubectl logs -l app=gateway
```

---

## 📖 Usage Guide

### 1. Authenticate & Get JWT Token
```bash
curl -X POST http://mp3converter.com/login \
  -u test@example.com:abc123

# Response
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Store the token for subsequent requests:
```bash
export JWT_TOKEN="your-token-here"
```

### 2. Upload Video File
```bash
curl -X POST http://mp3converter.com/upload \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -F "file=@/path/to/video.mp4"

# Response
{
  "status": "file uploaded"
}
```

### 3. Monitor Processing
```bash
# Check converter logs
kubectl logs -l app=converter --tail=50 -f

# Check RabbitMQ queue status
# Access RabbitMQ Management UI at http://rabbitmq.manager.com
# Default credentials: guest/guest
```

### 4. Receive Email Notification
You'll receive an email with the subject **"Your MP3 file is ready"** containing:
```
mp3 file_id: 507f1f77bcf86cd799439011 is ready for download
```

### 5. Download MP3 File
```bash
curl -X GET "http://mp3converter.com/download?fid=507f1f77bcf86cd799439011" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -o output.mp3
```

---

## 📁 Project Structure

```
video-to-mp3-converter/
├── auth/                          # Authentication Service
│   ├── Dockerfile
│   ├── server.py                  # Flask app with JWT logic
│   ├── init.sql                   # MySQL schema & seed data
│   ├── requirements.txt
│   └── manifests/
│       ├── auth-deploy.yaml       # Deployment config
│       ├── service.yaml           # ClusterIP service
│       ├── configmap.yaml         # MySQL connection details
│       └── secret.yaml            # Credentials (not in repo)
│
├── gateway/                       # API Gateway Service
│   ├── Dockerfile
│   ├── server.py                  # Main Flask app
│   ├── auth/
│   │   └── validate.py            # JWT validation logic
│   ├── auth_svc/
│   │   └── access.py              # Auth service client
│   ├── storage/
│   │   └── util.py                # GridFS upload logic
│   ├── requirements.txt
│   └── manifests/
│       ├── gateway-deploy.yaml
│       ├── service.yaml
│       ├── ingress.yaml           # NGINX ingress rules
│       ├── configmap.yaml
│       ├── mongo-deploy.yaml      # MongoDB deployment
│       └── mongo-service.yaml
│
├── converter/                     # Video Conversion Service
│   ├── Dockerfile
│   ├── consumer.py                # RabbitMQ consumer
│   ├── convert/
│   │   └── to_mp3.py              # Conversion logic (MoviePy)
│   ├── requirements.txt
│   └── manifest/
│       ├── converter-deploy.yaml  # Deployment with 4 replicas
│       └── configmap.yaml
│
├── notification/                  # Email Notification Service
│   ├── Dockerfile
│   ├── consumer.py                # RabbitMQ consumer
│   ├── send/
│   │   └── email.py               # SMTP email sending
│   ├── requirements.txt
│   └── manifest/
│       ├── notification-deploy.yaml
│       └── configmap.yaml
│
├── rabbit/                        # RabbitMQ Infrastructure
│   └── manifests/
│       ├── statefulset.yaml       # StatefulSet for RabbitMQ
│       ├── service.yaml           # Service (ports 5672, 15672)
│       ├── ingress.yaml           # Management UI ingress
│       ├── pvc.yaml               # Persistent volume claim
│       └── configmap.yaml
│
├── .gitignore
└── README.md
```

---

## 🐛 Troubleshooting

### Issue: Pods stuck in `Pending` state
**Solution**:
```bash
# Check resource availability
kubectl describe pod <pod-name>

# If insufficient resources
minikube stop
minikube start --cpus=4 --memory=8192
```

### Issue: `Queue is None` error in converter
**Cause**: ConfigMap not mounted or environment variables missing

**Solution**:
```bash
# Verify ConfigMap exists
kubectl get configmap converter-configmap -o yaml

# Check environment variables inside pod
kubectl exec -it <converter-pod> -- printenv | grep QUEUE

# If missing, ensure deployment has:
envFrom:
  - configMapRef:
      name: converter-configmap
```

### Issue: MongoDB connection refused
**Cause**: Using `host.minikube.internal` instead of Kubernetes service name

**Solution**:
- Use `mongo` (service name) instead of `host.minikube.internal`
- Update `gateway/server.py` and `converter/consumer.py`

### Issue: RabbitMQ not receiving messages
**Solution**:
```bash
# Check RabbitMQ is running
kubectl get pods -l app=rabbitmq

# Access RabbitMQ Management UI
# Navigate to http://rabbitmq.manager.com
# Login: guest/guest
# Check if queues 'video' and 'mp3' exist

# If queues missing, check converter/gateway logs for errors
kubectl logs -l app=converter
kubectl logs -l app=gateway
```

### Issue: Email notifications not sent
**Solution**:
1. Verify Gmail credentials in secret:
   ```bash
   kubectl get secret notification-secret -o yaml
   ```
2. Ensure using [App Password](https://support.google.com/accounts/answer/185833), not regular password
3. Check notification service logs:
   ```bash
   kubectl logs -l app=notification
   ```

### Issue: 403 Forbidden on upload
**Cause**: JWT token doesn't have `admin: true`

**Solution**:
- Check auth service `create_jwt()` function
- Ensure `admin` parameter is `True` when generating token

---

## 📈 Scaling & Performance

### Horizontal Pod Autoscaling
```bash
# Scale converter based on CPU usage
kubectl autoscale deployment converter \
  --cpu-percent=70 \
  --min=2 \
  --max=10

# Scale gateway for high traffic
kubectl autoscale deployment gateway \
  --cpu-percent=60 \
  --min=2 \
  --max=8
```

### Manual Scaling
```bash
# Scale converter to 8 replicas
kubectl scale deployment converter --replicas=8

# Scale gateway to 5 replicas
kubectl scale deployment gateway --replicas=5
```


## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Add unit tests for new features
- Update documentation for API changes
- Use meaningful commit messages

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Nishanth R**

Passionate about building scalable distributed systems, cloud-native applications, and AI-powered solutions.

- 💼 [LinkedIn]([https://linkedin.com/in/yourprofile](https://www.linkedin.com/in/r-nishanth-/)])
- 🐙 [PF]([https://github.com/yourusername](https://nishanth-nishu.github.io/my_protfolio/)])
- 📧 Email: nishanth0962333@gmail.com

---

## 🙏 Acknowledgments

- **RabbitMQ** for reliable message queuing
- **Kubernetes** for powerful orchestration
- **Flask** for lightweight web framework
- **MoviePy** for video processing capabilities

---

## ⭐ Show Your Support

If you found this project useful, please consider:
- ⭐ Starring the repository
- 🍴 Forking for your own projects
- 📢 Sharing with others
- 💬 Providing feedback or suggestions

---

**Built with ❤️ using Python, Kubernetes, and RabbitMQ**
