# Project Instructions & Overview  

## How to Run  

1. Start the services:  
   ```bash
   docker-compose up --build
   ```  
2. Run the backend:  
   ```bash
   uvicorn backend.asgi:application --reload
   ```  
3. Open your browser and visit:  
   [http://127.0.0.1:8000](http://127.0.0.1:8000)  

---

## Features  

### Messaging Portal  
Chat with existing users via private message, or create groups to talk with multiple people.  
- Implemented using Redis pub/sub for live-message delivery.  

### File System  
Upload, download, or delete files with the built-in file manager.  
- Implemented using MinIO for S3-compatible storage.  

### User Permissions  
Users can have one of four roles: admin, moderator, user, or guest.  
- Files can only be deleted by their owner or the superuser.  
- Admins can delete files shared with them.  
- Users can only download files shared with them.  
- All roles can upload files.  

---

## Test Logins  

Logins are listed in the format `username : password (role)`  

1. `jason : amivaplus (superuser)`  
2. `admintest : amivaplus (admin)`  
3. `modtest : amivaplus (moderator)`  
4. `usertest : amivaplus (user)`  

Example: A test file has been shared with both **admintest** and **usertest** by *jason*.  
- admintest → can delete & view it  
- usertest → can only view it  

---

## Optimizations / Fixes  

### 1. Real-Time Messaging  
**Problem:** Chat window required manual refresh, since messages were only stored in the database. This blocked real-time updates and risked performance bottlenecks from constant DB reads/writes.  
**Fix:** Integrated Redis pub/sub channels for real-time messaging. Messages now deliver instantly, while reducing DB load by decoupling persistence from delivery.  

### 2. Scalable File Storage  
**Problem:** Files were stored locally, which broke scaling horizontally (each server would need its own copy). It also risked file I/O bottlenecks on the app server.  
**Fix:** Switched to MinIO, an S3-compatible object store. Enables scalability, reliability, and cloud-native compatibility.  