# Bug Fix 1: 

2025-12-25 18:08:19,015 - server_module - ERROR - Error storing search query: 'Beta' object has no attribute 'vector_stores'

# Bug Fix 2:

2025-12-25 18:44:27,278 - server_module - ERROR - Error storing search query: Files.create() missing 1 required keyword-only argument: 'purpose'

# Bug Fix 3:

Limit the file filtering to avoid quota limit

Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}