# Testings in this Project

In this project, testing for memory leaks is very important as it is a C extension module, on top of testing the functionalities of the different Python modules.

Testing for memory leaks in C extension modules is essential for ensuring the reliability, performance, security, and maintainability of the software. Proper memory management in C extensions prevents potential issues that could have far-reaching consequences, particularly in large-scale or long-running applications.

## 1. **Resource Management**:
   - **Memory Efficiency**: In C extensions, managing memory manually (e.g., using `malloc`, `calloc`, and `free`) is necessary. Failure to release memory properly leads to memory leaks, which over time can cause an application to consume more and more memory, eventually exhausting the available system memory.
   - **Stability**: If a program keeps leaking memory, it can lead to instability, crashes, and unresponsiveness, particularly in long-running applications or those that handle a large amount of data.

## 2. **Performance**:
   - **System Performance**: Memory leaks can degrade the performance of the system by reducing the available memory for other processes. This can cause the operating system to resort to using swap space, leading to a significant drop in system performance.
   - **Application Performance**: An application that leaks memory might experience reduced performance due to frequent garbage collection or increased memory management overhead.

## 3. **Scalability**:
   - **Long-Running Processes**: Many C extension modules are used in environments where the software must run continuously for long periods (e.g., servers, data processing pipelines). Memory leaks in such scenarios can lead to system crashes or forced reboots, reducing the scalability and reliability of the software.
   - **Large-Scale Applications**: In large-scale applications, memory leaks can significantly affect the overall resource utilization, leading to the need for more hardware or infrastructure to maintain performance.

## 4. **Security**:
   - **Vulnerability Exploitation**: Memory leaks can sometimes lead to security vulnerabilities. Attackers might exploit these leaks to carry out Denial-of-Service (DoS) attacks by consuming all available memory, causing the system to crash or become unresponsive.
   - **Predictability of Behavior**: A program that behaves unpredictably due to memory leaks can be more susceptible to other security flaws. Ensuring memory is properly managed reduces the risk of unexpected behavior that could be exploited.

## 5. **Correctness of the Extension**:
   - **Logical Errors**: Memory leaks often indicate deeper issues in the code, such as improper management of memory allocation and deallocation. These logical errors can lead to incorrect program behavior, crashes, or other types of bugs.
   - **Python Integration**: Since Python relies heavily on garbage collection, improper memory management in C extensions can interfere with Python’s memory management system, leading to crashes or data corruption.

## 6. **Maintainability and Debugging**:
   - **Ease of Maintenance**: Identifying and fixing memory leaks early in the development process makes the codebase easier to maintain. If leaks are not detected, they can accumulate over time, making the code more complex and harder to debug.
   - **Simplified Debugging**: Memory leaks can be difficult to track down once they become widespread. Regular testing helps catch these leaks early, simplifying the debugging process and reducing the time spent on fixing bugs.

## 7. **Compliance and Best Practices**:
   - **Industry Standards**: In many industries, adhering to best practices in resource management, including avoiding memory leaks, is a requirement for compliance with industry standards or certifications.
   - **Professionalism**: Ensuring that a C extension is free of memory leaks reflects a commitment to professional software development practices, which is essential for maintaining a high standard of code quality.


The files used in testing is located under a directory name `tests` for this repository. Below is an elaboration of each file within and the tests that it conducts.

## **1. `conftest.py` File:**

This file contains setup code that is shared across multiple test files using the pytest framework.

### **Key Functions and Decorators:**

- **`limit_leaks(memstring: str)` Decorator:**
  - This decorator is designed to limit memory leaks during testing. It achieves this by running a decorated function (or coroutine) multiple times (`ITERATIONS`), thereby allowing any potential memory leaks to surface.
  - The decorator checks for the presence of the `--enable-leak-tracking` command-line option and ensures that leak tracking is only enabled when necessary. Additionally, it applies a platform check to skip leak tracking on Windows.

- **`pytest_addoption(parser: Any)` Function:**
  - This function adds a custom command-line option `--enable-leak-tracking` to pytest. This option is used to control whether leak tracking is enabled for the tests.

## **2. `test_custom.py` File:**

This file contains tests for the `Custom` class, which appears to be a simple data container with `first`, `last`, and `number` attributes.

### **Tests:**

- **`test_default_initialization()`**
  - Tests the default initialization of a `Custom` object to ensure that the attributes are set to their default values.
  - Verifies that the global variable `CUSTOM_GLOBAL` is correctly set.

- **`test_initialization_with_values()`**
  - Tests the initialization of a `Custom` object with specific values.
  - Ensures that the attributes are correctly assigned when passed during initialization.

- **`test_initialization_with_partial_values()`**
  - Tests the initialization of a `Custom` object with only a subset of the possible values.
  - Verifies that uninitialized attributes are set to their default values.

- **`test_name_method()`**
  - Tests the `name()` method, which presumably returns the full name of the object (i.e., a concatenation of `first` and `last`).

- **`test_name_method_with_empty_last()`**
  - Tests the `name()` method when the `last` attribute is an empty string.
  - Ensures that the method correctly handles the edge case of an empty last name.

- **`test_name_method_with_empty_first()`**
  - Tests the `name()` method when the `first` attribute is an empty string.

- **`test_name_method_with_both_empty()`**
  - Tests the `name()` method when both `first` and `last` attributes are empty.

- **`test_number_attribute()`**
  - Tests the assignment and retrieval of the `number` attribute.

- **`test_first_attribute_setter()` and `test_last_attribute_setter()`**
  - Tests the setters for the `first` and `last` attributes, ensuring that they correctly update the attributes.

These tests are straightforward and focus on ensuring that the `Custom` class behaves as expected under various scenarios, including edge cases.

## **3. `test_lib.py` File:**

This file contains tests for the `NRIC` class and its derived classes. `NRIC` is a subclass of `NewType` with additional methods for validation and string representation.

### **Tests:**

- **`test_nric()`**
  - Tests the `NRIC` class by creating instances with different values.
  - Verifies the `__str__` method, ensuring that it returns the correct string representation.
  - Checks that the custom attributes (`hello`, `_prefix`, `_digits`, `_suffix`) are correctly set and retrieved.
  - Ensures that certain operations, like replacing or concatenating the NRIC string, raise exceptions.

- **`test_goodmannric()`**
  - Tests the `GoodManNRIC` subclass of `NRIC`.
  - Similar to `test_nric()`, but includes an additional attribute `bye` and its corresponding checks.
  - Ensures that the `prefix` property works as intended.

- **`test_add()`**
  - Tests the `add()` function to ensure it correctly adds two numbers.

- **`test_foo()`**
  - Tests the `Foo` class, specifically ensuring that the `counter` attribute increments correctly with each call.

- **`test_ethereum_address()`**
  - Tests the `EthereumAddress` class, which represents a blockchain address.
  - Ensures that the address is correctly validated and stored, and that the `is_checksum` property is correctly handled.

- **`test_positive_int()` and `test_bounded_positive_int()`**
  - Tests the `PositiveInt` and `BoundedPositiveInt` classes.
  - These classes enforce that the integer value is positive, with `BoundedPositiveInt` further enforcing upper and lower bounds.
  - The tests ensure that the attributes are correctly set and that operations that violate the bounds raise exceptions.

- **`test_my_dataframe()`**
  - Tests the `MyDataFrame` class, a subclass of `pd.DataFrame` with additional attributes (`a`, `b`, `c`).
  - Ensures that the DataFrame operations do not violate the class's invariants and that the additional attributes are correctly preserved.
