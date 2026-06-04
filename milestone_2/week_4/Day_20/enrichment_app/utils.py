# utils.py
# Helper functions (if needed in future)

def format_metadata(metadata):
    """Pretty format metadata for display"""
    return {k: v for k, v in metadata.items() if not k.startswith("_")}