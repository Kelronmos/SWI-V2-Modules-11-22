"""Platform labels for educational package (demo only)."""
SUPPORTED = ("android", "linux", "macos", "windows")

def normalize_platform(name: str) -> str:
    n = (name or "").strip().lower()
    if n not in SUPPORTED:
        raise ValueError(f"Unsupported platform: {name}")
    return n

def platform_notes(platform: str) -> str:
    return {
        "android": "Termux / Android demo path",
        "linux": "Unix demo path",
        "macos": "macOS demo path",
        "windows": "Windows demo path",
    }.get(normalize_platform(platform), "unknown")
