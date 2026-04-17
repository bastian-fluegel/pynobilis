# pynobilis - General Documentation 

## Introduction 

pynobilis is a "noble", native macOS UI framework built with Python. It leverages `pyobjc` to interface directly with Apple's AppKit framework, providing a truly native experience with Retina support and system-standard behavior. 

---

## Core Component: The Application (`core/app.py`) 

The `App` class serves as the entry point and manager for the macOS application lifecycle. 

### Initialization 

When an `App` instance is created, it performs two critical tasks: 

1. **NSApplication Acquisition**: It retrieves the shared `NSApplication` instance. 
2. **Activation Policy**: It sets the activation policy to `NSApplicationActivationPolicyRegular`. This ensures the application appears in the Dock, can have menus, and can own windows that take focus. 

### The App Delegate 

`NobilisAppDelegate` is a helper class inheriting from `AppKit.NSObject`. It handles system-level events. Currently, it implements: 

* **`applicationShouldTerminateAfterLastWindowClosed_`**: Returns `True`, ensuring the application exits cleanly when the user closes the last UI window. 

### Execution Loop 

* **`run()`**: This method invokes `AppHelper.runEventLoop()`, which hands over control to the macOS event system. It includes a `try-except` block to catch `KeyboardInterrupt` (Ctrl+C) for graceful shutdowns from the terminal. 
* **`stop()`**: Manually terminates the application via `terminate_` and exits the Python process. 

---

## References 

1. [core/app.py](uploaded:bastian-fluegel/pynobilis/pynobilis-a98a6d8500ba1679c3a1940b98c885026b8bf28c/core/app.py) 
2. [pyproject.toml](uploaded:bastian-fluegel/pynobilis/pynobilis-a98a6d8500ba1679c3a1940b98c885026b8bf28c/pyproject.toml)