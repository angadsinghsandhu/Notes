```markdown
# Design Patterns in Python

This document provides an overview of several important design patterns with Python code examples and notes. The following patterns are covered:

- Factory Pattern
- Singleton Pattern
- Specification Pattern
- Observer Pattern
- Strategy Pattern (Additional Example)

---

## 1. Factory Pattern

The Factory Pattern provides an interface for creating objects without specifying the exact class of object that will be created. It helps in abstracting the instantiation process, making it easier to manage and extend code.

### Example: Shape Factory

```python
from abc import ABC, abstractmethod

# Product Interface
class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass

# Concrete Products
class Circle(Shape):
    def draw(self):
        return "Drawing a Circle"

class Square(Shape):
    def draw(self):
        return "Drawing a Square"

# Factory Class
class ShapeFactory:
    @staticmethod
    def get_shape(shape_type: str) -> Shape:
        if shape_type.lower() == 'circle':
            return Circle()
        elif shape_type.lower() == 'square':
            return Square()
        else:
            raise ValueError("Unknown shape type")

# Usage Example
if __name__ == "__main__":
    shape = ShapeFactory.get_shape("circle")
    print(shape.draw())  # Output: Drawing a Circle
```

**Notes:**
- **Encapsulation of Object Creation:** The client code doesn't need to know the details of how the objects are created.
- **Ease of Extension:** Adding new types (e.g., Triangle) requires minimal changes to the factory.

---

## 2. Singleton Pattern

The Singleton Pattern ensures that a class has only one instance and provides a global point of access to it. This is particularly useful for shared resources such as configuration objects or logging systems.

### Example: Singleton Logger

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=SingletonMeta):
    def __init__(self):
        self.log = []

    def write(self, message):
        self.log.append(message)

    def read(self):
        return self.log

# Usage Example
if __name__ == "__main__":
    logger1 = Logger()
    logger2 = Logger()
    logger1.write("Singleton pattern in action!")
    print(logger2.read())  # Output: ['Singleton pattern in action!']
    print(logger1 is logger2)  # Output: True
```

**Notes:**
- **Single Instance:** Only one instance of `Logger` exists during runtime.
- **Global Access:** The instance is globally accessible, making it ideal for shared resources.

---

## 3. Specification Pattern

The Specification Pattern allows you to combine business rules or criteria in a flexible way. It is useful for filtering objects or determining whether objects meet certain criteria.

### Example: Product Specification

```python
from abc import ABC, abstractmethod

# Specification Interface
class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, candidate) -> bool:
        pass

    # Combine specifications with logical AND
    def __and__(self, other):
        return AndSpecification(self, other)

class AndSpecification(Specification):
    def __init__(self, spec1, spec2):
        self.spec1 = spec1
        self.spec2 = spec2

    def is_satisfied_by(self, candidate) -> bool:
        return self.spec1.is_satisfied_by(candidate) and self.spec2.is_satisfied_by(candidate)

# Concrete Specifications
class ColorSpecification(Specification):
    def __init__(self, color):
        self.color = color

    def is_satisfied_by(self, candidate) -> bool:
        return candidate.get("color") == self.color

class SizeSpecification(Specification):
    def __init__(self, size):
        self.size = size

    def is_satisfied_by(self, candidate) -> bool:
        return candidate.get("size") == self.size

# Usage Example
if __name__ == "__main__":
    product = {"name": "T-shirt", "color": "red", "size": "M"}
    red_spec = ColorSpecification("red")
    medium_spec = SizeSpecification("M")

    combined_spec = red_spec & medium_spec
    print(combined_spec.is_satisfied_by(product))  # Output: True
```

**Notes:**
- **Flexible Business Rules:** Easily combine multiple specifications to filter or validate objects.
- **Reusability:** Each specification is a reusable unit that encapsulates a single criterion.

---

## 4. Observer Pattern

The Observer Pattern defines a one-to-many dependency between objects so that when one object (the subject) changes state, all its dependents (observers) are notified and updated automatically.

### Example: Event Notifier

```python
from abc import ABC, abstractmethod

# Observer Interface
class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

# Subject (Observable) Class
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)

# Concrete Observers
class EmailNotifier(Observer):
    def update(self, message: str):
        print(f"EmailNotifier: {message}")

class SMSNotifier(Observer):
    def update(self, message: str):
        print(f"SMSNotifier: {message}")

# Usage Example
if __name__ == "__main__":
    subject = Subject()
    email_notifier = EmailNotifier()
    sms_notifier = SMSNotifier()

    subject.attach(email_notifier)
    subject.attach(sms_notifier)

    subject.notify("The system has been updated!")
    # Output:
    # EmailNotifier: The system has been updated!
    # SMSNotifier: The system has been updated!
```

**Notes:**
- **Loose Coupling:** The subject doesn't need to know details about the observers.
- **Dynamic Subscription:** Observers can subscribe or unsubscribe at runtime.

---

## 5. Strategy Pattern (Additional Example)

The Strategy Pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. This pattern enables the algorithm to vary independently from clients that use it.

### Example: Payment Strategy

```python
from abc import ABC, abstractmethod

# Strategy Interface
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass

# Concrete Strategies
class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number):
        self.card_number = card_number

    def pay(self, amount: float):
        return f"Paid {amount} using Credit Card {self.card_number}"

class PaypalPayment(PaymentStrategy):
    def __init__(self, email):
        self.email = email

    def pay(self, amount: float):
        return f"Paid {amount} using PayPal account {self.email}"

# Context Class
class ShoppingCart:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy
        self.items = []

    def add_item(self, item, price: float):
        self.items.append((item, price))

    def checkout(self):
        total = sum(price for _, price in self.items)
        return self.strategy.pay(total)

# Usage Example
if __name__ == "__main__":
    # Using Credit Card Payment
    cart = ShoppingCart(CreditCardPayment("1234-5678-9012-3456"))
    cart.add_item("Book", 12.99)
    cart.add_item("Pen", 1.99)
    print(cart.checkout())  # Output: Paid 14.98 using Credit Card 1234-5678-9012-3456

    # Using PayPal Payment
    cart.strategy = PaypalPayment("user@example.com")
    print(cart.checkout())  # Output will depend on the new strategy and items in the cart
```

**Notes:**
- **Interchangeable Algorithms:** The payment method can be changed at runtime without altering the shopping cart code.
- **Separation of Concerns:** The shopping cart class is not burdened with payment processing logic.

---

## Conclusion

Design patterns such as the Factory, Singleton, Specification, Observer, and Strategy patterns provide reusable solutions to common problems in software design. By understanding and applying these patterns in Python, you can create scalable, maintainable, and flexible applications.