# Amazon Inventory Lockers

Below is one example of a Low Level Design (LLD) in Python for a **Delivery & Locker Management System** that meets the requirements. The design follows the SOLID principles and is broken into several files, each handling a specific responsibility. In this system:

- A **Delivery Agent** brings the package, scans the QR code (using a simulated QR scanner) to retrieve product information, and then the system finds an appropriate locker for the product.
- A **Product Listing** exists so that new products can be added (with recommended storage type).
- There are three types of storage (lockers): **Small**, **Medium**, and **Large**. (A small product can go in small, medium, or large lockers; similarly, medium products can go in medium or large lockers, etc.)
- The system chooses the proper locker based on product requirements and the locker’s distance from the system.
- The system can also empty (remove) a locker.
- A user can check for a product in the system to know in which locker it is stored.

## Directory Structure

```
deliverysystem/
├── __init__.py
├── locker.py
├── locker_type.py
├── product.py
├── item.py
├── delivery_system.py
├── delivery_agent.py
├── qr_scanner.py
├── storage_strategy.py
└── delivery_system_demo.py
```

### Summary of the Design

1. **Clarify Requirements & Identify Use Cases:**  
   - A delivery agent scans a package’s QR code to retrieve product information.  
   - New products are listed, and their instances (items) are onboarded into the system.  
   - Based on product size and available storage (lockers), an optimal locker is chosen (taking distance into account).  
   - Lockers can be emptied, and a lookup is available to locate a product.

2. **Identify Key Entities:**  
   - **Product:** Represents the product listing with recommended locker type.  
   - **Item:** An instance of a product (a package).  
   - **Locker:** Represents a storage unit with type and distance attributes.  
   - **DeliverySystem:** The central system coordinating products, lockers, and item onboarding.  
   - **DeliveryAgent:** The actor who scans QR codes and onboards packages.  
   - **QRScanner:** A helper class simulating QR scanning.  
   - **StorageStrategy:** Encapsulates the algorithm to choose the optimal locker.

3. **SOLID Principles Applied:**  
   - **SRP:** Each module/class is responsible for one aspect (e.g., Locker handles storage, Product handles product data).  
   - **OCP:** New storage strategies or locker selection rules can be added by extending `StorageStrategy` without changing the system code.  
   - **LSP:** The delivery system and agent interact with items and lockers via well-defined interfaces.  
   - **ISP:** Classes expose only the necessary methods to clients (for example, the DeliveryAgent uses only the QRScanner interface).  
   - **DIP:** The high-level `DeliverySystem` depends on abstractions (such as a storage strategy) rather than concrete implementations.