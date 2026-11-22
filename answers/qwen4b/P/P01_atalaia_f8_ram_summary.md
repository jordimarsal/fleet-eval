FILES  
src/atalaia/api.py  
src/atalaia/models.py  
web/app.js  

TASKS  
T1: Implement `/api/system` endpoint to read `MemAvailable` from `/proc/meminfo` and return free RAM in MB  
    depends_on: (none)  
    refs: R1, R2, R5  
T2: Update UI logic to fetch and display sum of `ram_mb` from `up` entries and free RAM from `/api/system` on poll  
    depends_on: T1  
    refs: R3, R4  
T3: Ensure all values are rendered as `—` when unavailable in UI  
    depends_on: T2  
    refs: R4  

GATES  
- Unit test coverage for `/api/system` endpoint passes (covers R1, R2, R5)  
- UI rendering behavior verified with mock data showing `—` for missing values (covers R3, R4)  
- Manual validation that system summary does not require subprocess or Docker calls (covers R5)