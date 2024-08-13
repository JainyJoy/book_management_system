import asyncio
def run_async(func):
    """Utility to run an async function in a sync context."""
    return asyncio.run(func)