# Win32 and Asyncio Dual-Thread Collaboration Design

## Architecture Diagram

```mermaid
graph TB
    subgraph "UI Thread (Win32)"
        A[Win32 Message Loop] --> B[Handle GUI Events]
        B --> C[Execute asyncio Tasks]
        C --> D[Release Semaphore]
        
        M[TRIO_MSG/ASYNCIO_MSG Handler] --> N[Process Task Queue]
        N --> O[Run asyncio.run_once]
        O --> P[Release Semaphore]
    end
    
    subgraph "Backend Thread (Asyncio)"
        E[Wait for Semaphore] --> F[Call epoll.poll]
        F --> G[Detect Events]
        G --> H[Request UI Processing]
        H --> E
    end
    
    subgraph "Coordination Mechanisms"
        I[Semaphore/Lock]
        J[Asyncio Ready Task Queue]
        K[Wake Pipe]
    end
    
    D --> I
    I --> E
    P --> I
    C --- J --- H
    
    subgraph "Timer Events"
        L[asyncio.call_later] --> Q[wake_backend_4_timer]
        Q --> R[Write to Wake Pipe]
        R --> S[Wake Up Backend Thread]
        S --> T[Process Timer Event]
    end
    
    R --> K --> F
```

## Core Design Principles

### 1. Dual-Thread Model

- **UI Thread**: Responsible for Win32 message loop and GUI event handling
- **Backend Thread**: Responsible for monitoring events in the asyncio event loop

This separation allows the GUI to remain responsive while asynchronous operations run in the background.

### 2. Thread Coordination Mechanisms

```mermaid
flowchart LR
    A[UI Thread] -->|releases| B[Semaphore]
    B -->|acquired by| C[Backend Thread]
    C -->|monitors events| D[epoll]
    D -->|events occur| E[Task Queue]
    E -->|processed by| A
    F[Timer Events] -->|writes to| G[Wake Pipe]
    G -->|wakes up| D
```

1. **Semaphore**: Ensures the two threads execute alternately, preventing race conditions
2. **Task Queue**: Thread-safe queue for passing functions that need to be executed on the UI thread
3. **Wake Pipe**: Allows the backend thread to be awakened when new events (like timers) occur

### 3. Message Passing Mechanisms

```mermaid
sequenceDiagram
    participant B as Backend Thread
    participant Q as Task Queue
    participant M as Message Window
    participant U as UI Thread
    
    B->>Q: Add function to queue
    B->>M: PostMessage(TRIO_MSG/ASYNCIO_MSG)
    M->>U: Process message
    U->>Q: Get and execute tasks
    U->>U: Run asyncio.run_once()
```

1. **TRIO_MSG/ASYNCIO_MSG**: Custom Win32 message used to trigger asyncio task processing in the UI thread
2. **PostMessage**: Safely sends messages from the backend thread to the UI thread
3. **run_sync_soon_threadsafe**: Adds functions to the queue and notifies the UI thread to execute them

## Key Event Flows

### 1. Initialization Process

```mermaid
sequenceDiagram
    participant U as UI Thread
    participant S as Semaphore
    participant B as Backend Thread
    
    U->>U: Create coordination mechanisms
    U->>B: Start thread
    B->>S: Wait for semaphore
    U->>U: run_events_on_ui_thread()
    U->>S: Release semaphore
    S->>B: Semaphore acquired
    B->>B: Begin monitoring
```

### 2. Normal Event Loop

```mermaid
sequenceDiagram
    participant U as UI Thread
    participant Q as Task Queue
    participant S as Semaphore
    participant B as Backend Thread
    
    U->>S: Release semaphore
    S->>B: Acquire semaphore
    B->>B: Call epoll.poll(timeout)
    Note over B: Event occurs
    B->>Q: Add task to queue
    B->>U: Send TRIO_MSG/ASYNCIO_MSG
    U->>Q: Process all tasks
    U->>U: Run asyncio.run_once()
    U->>S: Release semaphore
    S->>B: Acquire semaphore (loop continues)
```

### 3. New Timer Event Flow

```mermaid
sequenceDiagram
    participant U as UI Thread
    participant T as Asyncio Timer
    participant W as Wake Pipe
    participant B as Backend Thread
    
    Note over U: loop.call_later() called
    U->>T: Create new timer
    T->>W: Write data to wake pipe
    W->>B: Wake up from epoll.poll()
    B->>U: Request process timer events
    U->>U: Process timer callbacks
```

### 4. Timeout Handling Flow

```mermaid
sequenceDiagram
    participant U as UI Thread
    participant B as Backend Thread
    
    B->>B: Get timeout from loop.get_backend_timeout()
    B->>B: epoll.poll(timeout)
    Note over B: Timeout occurs
    B->>U: Request task processing
    U->>U: Execute expired timer callbacks
```

### 5. Task Completion Flow

```mermaid
sequenceDiagram
    participant AT as Asyncio Task
    participant CB as Completion Callback
    participant U as UI Thread
    
    AT->>AT: Task completes
    AT->>CB: Call on_task_done
    CB->>U: Send result via run_sync_soon_threadsafe
    U->>U: Call done_callback
```

## Implementation Considerations

1. **Error Handling**: Both backend and UI threads need robust exception catching and handling
2. **Resource Cleanup**: Properly close event loop, pipes, and epoll when tasks complete
3. **Compatibility**: Handle API differences between asyncio versions
4. **Deadlock Prevention**: Ensure semaphores are correctly released in all paths
5. **Timer Precision**: Use wake mechanism to ensure timers are processed promptly

## Key Function Descriptions

### asyncio_guest_run

Main entry function responsible for setting up the dual-thread environment and starting the asyncio task.

### run_events_on_ui_thread

Executes one cycle of the asyncio event loop on the UI thread, handling ready callbacks and I/O events.

### backend_thread_loop

Main loop of the backend thread, responsible for monitoring file descriptor events and timer timeouts.

### wake_backend_4_timer

Wakes up the backend thread when new timers are created, ensuring timer events are processed promptly.

## Summary

This design coordinates the Win32 message loop and asyncio event loop through careful orchestration, enabling the use of Python's asynchronous programming in GUI applications. Semaphores ensure synchronization between threads, while wake mechanisms and message queues provide efficient communication channels, solving the limitations of the traditional single-threaded asyncio model in GUI environments.
