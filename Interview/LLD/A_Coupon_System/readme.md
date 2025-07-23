# Coupon System

## Proposed Directory Structure

```
couponvouchermanagement/
├── promotion_status.py
├── rule_types.py
├── token.py
├── coupon.py
├── voucher.py
├── rule.py
├── age_limit_rule.py
├── transaction_value_rule.py
├── promotion_service.py
├── account.py
├── admin.py
├── user.py
├── system.py
└── coupon_voucher_demo.py
```

## **Key Design Considerations and SOLID Principles:**
> 
> - **Single Responsibility:**  
>   Each class has one focused responsibility. For example, the abstract `Token` class defines common properties for both coupons and vouchers, while each concrete rule (such as `AgeLimitRule`) encapsulates a single validation.
> 
> - **Open/Closed:**  
>   The system is open for extension—for example, you can add new rule types without modifying the existing classes.
> 
> - **Liskov Substitution:**  
>   Subtypes (e.g. `Coupon` and `Voucher` as subtypes of `Token`) can replace the abstract type without breaking client code.
> 
> - **Interface Segregation:**  
>   The clients (for example, promotion services and APIs) depend only on the interfaces they need (e.g. a Promotion CRUD interface) rather than a “fat” interface.
> 
> - **Dependency Inversion:**  
>   High-level modules (like Admin or Promotion Service) depend on abstractions (such as the `Token` or `Rule` abstract classes) instead of concrete classes.
> 
> Additionally, we use a **Singleton** for the central system repository and a **Factory/Strategy** pattern for creating/applying rules.

### Summary

1. **Clarify Requirements & Identify Use Cases:**  
   - Admins create/update/delete coupons and vouchers with rules (e.g., age and cart value limits).  
   - Users view available promotions and apply them during transactions.

2. **Identify Key Entities:**  
   - **Token (abstract)**: Common base for Coupon and Voucher.  
   - **Coupon:** Has rules and utilization limits.  
   - **Voucher:** May be unassigned or pre-assigned to a user.  
   - **Rule:** Abstract rule with concrete implementations such as AgeLimitRule and TransactionValueRule.  
   - **System:** A Singleton repository managing promotions.  
   - **PromotionService (interface):** Defines CRUD and apply operations (implemented via System).

3. **Design Classes & Their Responsibilities:**  
   - Each file is responsible for a single concept (e.g., `coupon.py` for coupon logic).
   - Admin and User classes interact with the System to manage and apply promotions.

4. **Core Methods & Interactions:**  
   - `can_apply_coupon(user, transaction)` in Coupon delegates to each rule.
   - The System class provides APIs for adding/updating/deleting and retrieving active promotions.
   - APIs (e.g. in `coupon_voucher_demo.py`) simulate end-to-end usage.

5. **SOLID Principles in Action:**  
   - **SRP:** Every class has one clear responsibility.  
   - **OCP:** New rule types can be added without changing the existing code.  
   - **LSP:** Coupon and Voucher can be used interchangeably when handling Tokens.  
   - **ISP:** Clients (Admin, User) only interact with the necessary methods.  
   - **DIP:** High-level modules (System, Promotion Service) depend on abstract tokens and rules.